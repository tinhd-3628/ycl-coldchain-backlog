"""Assign every task to a 2-week sprint and rebalance PICs inside the backend (BE-1/2/3) and QA (QA-1/2) pools.

A milestone's tasks go only into the sprints built for it. Order holds at story level (a task
never lands before the tasks of the stories it depends on) and inside a story by layer
(db -> api/batch -> ui -> test). Greedy earliest fit against a per-person capacity: FE keeps its
PIC; a backend / QA task prefers its home PIC (task_pic) and otherwise goes to the least-loaded
member of its pool. A task that fits nowhere lands in the milestone's last sprint as an overload.
A task with not_before (added after a sprint started) is never placed before that sprint.
"""
from collections import defaultdict

from backlog_project_fields import task_pic

BACKEND = ["BE-1", "BE-2", "BE-3"]
QA = ["QA-1", "QA-2"]
LAYER_RANK = {"db": 0, "api": 1, "batch": 1, "ui": 2, "test": 3}


def story_order(stories):
    """Stories in dependency order, keeping YAML order among independent ones."""
    ids = {s["id"] for s in stories}
    deps = {s["id"]: {d for t in s["tasks"] for d in t.get("depends", []) if d in ids} for s in stories}
    ordered, placed = [], set()
    while len(ordered) < len(stories):
        ready = next((s for s in stories if s["id"] not in placed and deps[s["id"]] <= placed), None)
        if ready is None:
            raise ValueError("circular dependency between stories")
        ordered.append(ready)
        placed.add(ready["id"])
    return ordered


def plan_sprints(epics, sprints, capacity):
    """Set t['sprint'] and t['pic'] on every task; return overload messages (empty when the plan fits)."""
    load = defaultdict(int)  # (sprint index, pic) -> planned hours
    story_end = {}  # story id -> index of the last sprint holding one of its tasks
    overloads = []
    epic_of = {s["id"]: e["id"] for e in epics for s in e["stories"]}
    by_milestone = defaultdict(list)
    for e in epics:
        for s in e["stories"]:
            by_milestone[s["milestone"]].append(s)
    for key in dict.fromkeys(sp["milestone"] for sp in sprints):
        slots = [i for i, sp in enumerate(sprints) if sp["milestone"] == key]
        for s in story_order(by_milestone[key]):
            deps = {d for t in s["tasks"] for d in t.get("depends", [])}
            floor = max([slots[0], *(story_end[d] for d in deps)])
            rank_end = defaultdict(int)  # layer rank -> last sprint index used inside this story
            for t in sorted(s["tasks"], key=lambda t: LAYER_RANK[t["layer"]]):
                rank = LAYER_RANK[t["layer"]]
                earliest = max([floor, *(i for r, i in rank_end.items() if r < rank),
                                *(i for i, sp in enumerate(sprints) if sp["title"] == t.get("not_before"))])
                home = task_pic(epic_of[s["id"]], t["layer"])
                team = next((g for g in (BACKEND, QA) if home in g), [home])
                pool = [home, *sorted((p for p in team if p != home), key=lambda p: load[(earliest, p)])]
                slot, pic = next(((i, p) for i in slots if i >= earliest for p in pool
                                  if load[(i, p)] + t["hours"] <= capacity), (None, None))
                if slot is None:
                    slot = slots[-1]
                    pic = min(pool, key=lambda p: load[(slot, p)])
                    overloads.append(f"{t['tid']} ({t['hours']}h) -> {sprints[slot]['title']} {pic} over capacity")
                load[(slot, pic)] += t["hours"]
                t["sprint"], t["pic"] = sprints[slot]["title"], pic
                rank_end[rank] = max(rank_end[rank], slot)
                story_end[s["id"]] = max(story_end.get(s["id"], slot), slot)
    return overloads
