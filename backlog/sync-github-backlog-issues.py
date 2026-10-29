"""Sync the LAB-5 backlog (Epic -> Story -> Task sub-issues), UAT milestones and sprint fields to GitHub.

Sources: see backlog_plan_builder.py. Issue numbers are cached in github-issue-map.json: a rerun creates
only what is missing and PATCHes an issue only when its title / body / milestone changed (content_sha).
Project fields remember the value last written (fields_written) and are pushed again only when the
planned value changes, so edits the team makes on the board (Status, a moved sprint) are left alone.
SWP comes from backlog-swp-reviewed.json: tasks scored by tkm:sun-estimate and reviewed by the PL
(report under reports/), stories / epics = sum of their tasks.
Run setup-github-project-fields-and-views.py first (fields, views, sprints).
Usage: python sync-github-backlog-issues.py [--dry-run]
"""
import collections
import hashlib
import json
import pathlib
import subprocess
import sys
import time

from backlog_github_api import gh, graphql, project_with_fields, set_field
from backlog_plan_builder import CONSTRAINT, build_plan, load_backlog
from backlog_project_fields import wanted_fields

REPO = "tinhd-3628/ycl-coldchain-backlog"
OWNER = "tinhd-3628"
PROJECT_NO = 1
ASSIGNEE = "tinhd-3628"
MAP_FILE = pathlib.Path(__file__).parent / "github-issue-map.json"
SWP_FILE = pathlib.Path(__file__).parent / "backlog-swp-reviewed.json"
LABELS = {"type:epic": "3e4b9e", "type:story": "0e8a16", "type:task": "c5def5", "development": "5319e7",
          "priority:P0": "b60205", CONSTRAINT: "d93f0b", "layer:db": "fbca04", "layer:api": "f9d0c4",
          "layer:ui": "bfdadc", "layer:batch": "d4c5f9", "layer:test": "e99695"}
ADD_ITEM = "mutation($p:ID!,$c:ID!){addProjectV2ItemById(input:{projectId:$p,contentId:$c}){item{id}}}"
ITEM_OF_ISSUE = "query($c:ID!){node(id:$c){... on Issue{projectItems(first:20){nodes{id project{id}}}}}}"


def project_item_id(project_id, node_id):
    """Add the issue to the Project; if a Project workflow already auto-added it, reuse that item."""
    try:
        return graphql(ADD_ITEM, p=project_id, c=node_id)["addProjectV2ItemById"]["item"]["id"]
    except RuntimeError as err:
        if "already exists" not in str(err):
            raise
        items = graphql(ITEM_OF_ISSUE, c=node_id)["node"]["projectItems"]["nodes"]
        return next(i["id"] for i in items if i["project"]["id"] == project_id)


def ensure_milestones(milestones):
    """Create or update the UAT milestones by title; return {key: milestone number}."""
    existing = {m["title"]: m["number"] for m in gh(["api", f"repos/{REPO}/milestones?state=all&per_page=100"])}
    numbers = {}
    for m in milestones:
        payload = {"title": m["title"], "description": m["description"].strip(), "due_on": f"{m['due']}T08:00:00Z"}
        if m["title"] in existing:
            gh(["api", f"repos/{REPO}/milestones/{existing[m['title']]}", "--method", "PATCH", "--input", "-"], payload)
            numbers[m["key"]] = existing[m["title"]]
        else:
            numbers[m["key"]] = gh(["api", f"repos/{REPO}/milestones", "--method", "POST", "--input", "-"], payload)["number"]
    return numbers


def save(mapping):
    MAP_FILE.write_text(json.dumps(mapping, ensure_ascii=False, indent=1), encoding="utf-8")


def print_dry_run(data, plan):
    fake = {item["key"]: {"number": i + 1} for i, item in enumerate(plan)}
    for item in plan[:2] + plan[-1:]:
        print(f"--- {item['title']} | {item['milestone']} | PIC={item['pic']}\n{item['body'](fake)}")
    load = collections.defaultdict(int)
    for item in plan:
        if item["kind"] == "TASK":
            load[(item["sprint"], item["pic"])] += item["hours"]
    for sp in data["sprints"]:
        row = {pic: h for (s, pic), h in sorted(load.items()) if s == sp["title"]}
        print(f"{sp['title']} ({sp['milestone']}): {sum(row.values())}h {row}")
    print("overloads:", data["overloads"] or "none")
    print(f"total issues: {len(plan)}, longest title: {max(len(i['title']) for i in plan)} chars")


def main(dry_run):
    data = load_backlog()
    plan = build_plan(data["epics"])
    if dry_run:
        print_dry_run(data, plan)
        return
    mapping = json.loads(MAP_FILE.read_text(encoding="utf-8")) if MAP_FILE.exists() else {}
    for name, color in LABELS.items():
        subprocess.run(["gh", "label", "create", name, "--color", color, "--repo", REPO, "--force"], capture_output=True)
    ms_numbers = ensure_milestones(data["milestones"])
    milestone_due = {m["key"]: str(m["due"]) for m in data["milestones"]}
    swp = json.loads(SWP_FILE.read_text(encoding="utf-8"))["swp"] if SWP_FILE.exists() else {}
    project_id, fields = project_with_fields(OWNER, PROJECT_NO)
    for item in plan:
        rec = mapping.setdefault(item["key"], {})
        content = {"title": item["title"], "body": item["body"](mapping), "milestone": ms_numbers[item["milestone"]]}
        sha = hashlib.sha256(json.dumps(content, ensure_ascii=False).encode("utf-8")).hexdigest()
        if "number" not in rec:
            issue = gh(["api", f"repos/{REPO}/issues", "--method", "POST", "--input", "-"],
                       {**content, "labels": item["labels"], "assignees": [ASSIGNEE]})
            rec.update(number=issue["number"], id=issue["id"], node_id=issue["node_id"], content_sha=sha)
            save(mapping)
            time.sleep(1)  # stay under GitHub's secondary rate limit for content creation
        elif rec.get("content_sha") != sha:
            gh(["api", f"repos/{REPO}/issues/{rec['number']}", "--method", "PATCH", "--input", "-"], content)
            rec["content_sha"] = sha
            save(mapping)
            time.sleep(1)
        if item["parent"] and not rec.get("linked"):
            gh(["api", f"repos/{REPO}/issues/{mapping[item['parent']]['number']}/sub_issues", "--method", "POST",
                "--input", "-"], {"sub_issue_id": rec["id"]})
            rec["linked"] = True
            save(mapping)
        if not rec.get("item_id"):
            rec["item_id"] = project_item_id(project_id, rec["node_id"])
            save(mapping)
        written = rec.setdefault("fields_written", {})
        for name, (kind, value) in wanted_fields(item, milestone_due, swp).items():
            if written.get(name) != value:
                set_field(project_id, rec["item_id"], fields[name], kind, value)
                written[name] = value
                save(mapping)
        print(f"{item['key']} -> #{rec['number']}", flush=True)


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
