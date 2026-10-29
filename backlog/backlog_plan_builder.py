"""Build the LAB-5 issue plan from the YAML sources: Japanese breakdown + Vietnamese text + milestones + sprints."""
import pathlib

import yaml

from backlog_issue_bodies import epic_body, issue_title, story_body, task_body
from backlog_qa_tasks import add_story_qa_tasks
from backlog_sprint_planner import plan_sprints

HERE = pathlib.Path(__file__).parent
CONSTRAINT = "constraint:driver-hours-2024"


def load_backlog():
    """Merge Vietnamese text, number tasks T-001.., add story QA tasks, sum hours, resolve milestones, plan sprints.

    Returns the parsed breakdown dict with an extra 'overloads' list from the sprint planner.
    """
    data = yaml.safe_load((HERE / "backlog-breakdown.yaml").read_text(encoding="utf-8"))
    vi = yaml.safe_load((HERE / "backlog-translations-vi.yaml").read_text(encoding="utf-8"))
    milestones = data["milestones"]
    milestone_of = {scope: m["key"] for m in milestones for scope in m["scope"]}
    if len(milestone_of) != sum(len(m["scope"]) for m in milestones):
        raise ValueError("an epic/story ID appears in more than one milestone scope")
    order = [m["key"] for m in milestones]
    seq = 0
    for e in data["epics"]:
        e["title_vi"] = vi[e["id"]]
        for s in e["stories"]:
            s["title_vi"] = vi[s["id"]]
            s["milestone"] = milestone_of.get(s["id"]) or milestone_of[e["id"]]
            for t in s["tasks"]:
                if "tid" not in t:  # tasks added after the first sync carry a fixed tid (T-167..), so no ID moves
                    seq += 1
                    t["tid"] = f"T-{seq:03d}"
                t["title_vi"], t["ac_vi"] = vi[t["tid"]]["title"], vi[t["tid"]]["ac"]
                if len(t["ac_vi"]) != len(t["ac"]):
                    raise ValueError(f"{t['tid']}: Vietnamese ac count differs from Japanese")
    add_story_qa_tasks(data["epics"], seq)
    for e in data["epics"]:
        for s in e["stories"]:
            s["hours"] = sum(t["hours"] for t in s["tasks"])
        e["milestone"] = max((s["milestone"] for s in e["stories"]), key=order.index)  # epic closes at its last UAT
        e["hours"] = sum(s["hours"] for s in e["stories"])
    data["overloads"] = plan_sprints(data["epics"], data["sprints"], data["sprint_capacity_hours"])
    return data


def build_plan(epics):
    """Ordered issue specs; epics and stories first so every parent number exists before its children."""
    plan = []
    for e in epics:
        extra = [CONSTRAINT] if e.get("constraint") else []
        plan.append(dict(key=e["id"], kind="EPIC", title=issue_title("EPIC", e["id"], e["title"], e["title_vi"]),
                         labels=["type:epic", *extra], hours=e["hours"], pic="PL", parent=None,
                         milestone=e["milestone"], body=lambda m, e=e: epic_body(e)))
        for s in e["stories"]:
            plan.append(dict(key=s["id"], kind="STORY", title=issue_title("STORY", s["id"], s["title"], s["title_vi"]),
                             labels=["type:story", *extra], hours=s["hours"], parent=e["id"],
                             pic=max(s["tasks"], key=lambda t: t["hours"])["pic"],  # owner of the largest task
                             milestone=s["milestone"], body=lambda m, s=s, e=e: story_body(s, m[e["id"]]["number"])))
    for e in epics:
        extra = [CONSTRAINT] if e.get("constraint") else []
        for s in e["stories"]:
            for t in s["tasks"]:
                labels = ["type:task", "development", f"layer:{t['layer']}", *extra]
                labels += ["priority:P0"] if t.get("priority") == "P0" else []
                plan.append(dict(key=t["tid"], kind="TASK", title=issue_title("TASK", t["tid"], t["title"], t["title_vi"]),
                                 labels=labels, hours=t["hours"], pic=t["pic"], parent=s["id"], sprint=t["sprint"],
                                 milestone=s["milestone"], layer=t["layer"], p0=t.get("priority") == "P0",
                                 body=lambda m, s=s, t=t: task_body(s, t, m[s["id"]]["number"],
                                                                    {k: v["number"] for k, v in m.items() if "number" in v})))
    return plan
