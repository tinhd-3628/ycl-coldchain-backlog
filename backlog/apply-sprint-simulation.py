"""Apply a simulated sprint run (sprint-1-simulation.yaml) to the GitHub Project — LAB-5 exercise data.

Per task: Status (Done / In Progress / Todo), Spent time (h), Progress (%), Start Date (actual start)
and Due Date (planned end). Done issues are closed as completed; a task that is late or blocked gets
one bilingual comment with the reason (edited in place when the note changes). Values already written
are remembered in github-issue-map.json (sim_written / sim_state / sim_comment_id / sim_comment_sha),
so a rerun only pushes what changed in the YAML.
Usage: python apply-sprint-simulation.py [sprint-1-simulation.yaml] [--dry-run]
"""
import hashlib
import json
import pathlib
import sys

import yaml

from backlog_github_api import gh, project_with_fields, set_field

REPO = "tinhd-3628/ycl-coldchain-backlog"
OWNER = "tinhd-3628"
PROJECT_NO = 1
HERE = pathlib.Path(__file__).parent
MAP_FILE = HERE / "github-issue-map.json"


def status_of(task):
    if task["done"]:
        return "Done"
    return "In Progress" if task["start"] else "Todo"


def wanted(task, days):
    values = {"Status": ("select", status_of(task)), "Spent time (h)": ("number", task["spent"]),
              "Progress (%)": ("number", task["progress"]), "Due Date": ("date", str(days[task["planned"][1] - 1]))}
    if task["start"]:
        values["Start Date"] = ("date", str(days[task["start"] - 1]))
    return values


def comment_body(tid, sim, task):
    days = sim["days"]
    head = f"**{sim['sprint']} 振り返り / Nhìn lại {sim['sprint']}** ({days[0]} – {days[-1]}, 演習用の仮想データ / dữ liệu giả lập)"
    return (f"{head}\n\n- 状態 / Trạng thái: {status_of(task)} · 進捗 / Tiến độ: {task['progress']}% · "
            f"消化 / Đã dùng: {task['spent']}h\n\n{task['note']['ja']}\n\n{task['note']['vi']}\n")


def upsert_comment(rec, body):
    """Post the sprint comment once; when the note text changes, edit that same comment instead of adding one."""
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    if rec.get("sim_comment_sha") == digest:
        return
    cid = rec.get("sim_comment_id")
    if cid is None and rec.pop("sim_commented", False):  # posted before ids were kept: find it by its marker
        comments = gh(["api", f"repos/{REPO}/issues/{rec['number']}/comments"])
        cid = next(c["id"] for c in comments if "演習用の仮想データ" in c["body"])
    if cid:
        gh(["api", f"repos/{REPO}/issues/comments/{cid}", "--method", "PATCH", "--input", "-"], {"body": body})
    else:
        cid = gh(["api", f"repos/{REPO}/issues/{rec['number']}/comments", "--method", "POST", "--input", "-"],
                 {"body": body})["id"]
    rec["sim_comment_id"], rec["sim_comment_sha"] = cid, digest


def main(path, dry_run):
    sim = yaml.safe_load(path.read_text(encoding="utf-8"))
    mapping = json.loads(MAP_FILE.read_text(encoding="utf-8"))
    project_id, fields = (None, {}) if dry_run else project_with_fields(OWNER, PROJECT_NO)
    for tid, task in sim["tasks"].items():
        rec = mapping[tid]
        written = rec.setdefault("sim_written", {})
        changes = {k: v for k, v in wanted(task, sim["days"]).items() if written.get(k) != v[1]}
        if dry_run:
            print(f"{tid} #{rec['number']} {status_of(task)}: {sorted(changes)}")
            continue
        for name, (kind, value) in changes.items():
            set_field(project_id, rec["item_id"], fields[name], kind, value)
            written[name] = value
        state = "closed" if task["done"] else "open"
        if rec.get("sim_state", "open") != state:
            gh(["api", f"repos/{REPO}/issues/{rec['number']}", "--method", "PATCH", "--input", "-"],
               {"state": state, **({"state_reason": "completed"} if state == "closed" else {})})
            rec["sim_state"] = state
        if task.get("note"):
            upsert_comment(rec, comment_body(tid, sim, task))
        MAP_FILE.write_text(json.dumps(mapping, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{tid} -> #{rec['number']} {status_of(task)}", flush=True)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(HERE / (args[0] if args else "sprint-1-simulation.yaml"), "--dry-run" in sys.argv)
