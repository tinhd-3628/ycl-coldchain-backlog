"""Project field rules for the LAB-5 backlog: assumed PIC, work stage (Công đoạn), priority and due date."""

# Assumed owners (PIC field). Backend by domain, frontend by device family, tests by QA.
BE_PIC = {**dict.fromkeys(["E-06", "E-08", "E-09", "E-17", "E-20", "E-21", "E-23"], "BE-1"),
          **dict.fromkeys(["E-10", "E-11", "E-12", "E-16", "E-19", "E-22"], "BE-2"),
          **dict.fromkeys(["E-02", "E-03", "E-13", "E-14", "E-24"], "BE-3")}
FE2_EPICS = {"E-02", "E-03", "E-10", "E-13", "E-14"}  # dock tablet / driver PWA / HACCP screens
# Công đoạn options mirror the reference project (framgia/projects/281); tasks map from their layer.
STAGE_OPTIONS = ["1. SPEC", "2. BE", "3. FE", "4. QA tạo", "5. QA chạy", "6. Khác"]
STAGE_OF_LAYER = {"db": "2. BE", "api": "2. BE", "batch": "2. BE", "ui": "3. FE", "test": "4. QA tạo"}
PRIORITY_OPTIONS = ["Low", "Normal", "High", "Urgent", "Immediate"]
# QA-2 added with the story QA tasks; PL owns the epics
PIC_OPTIONS = ["BE-1", "BE-2", "BE-3", "FE-1", "FE-2", "QA-1", "QA-2", "PL"]


def task_pic(epic_id, layer):
    if layer == "test":
        return "QA-1"
    if layer == "ui":
        return "FE-2" if epic_id in FE2_EPICS else "FE-1"
    return BE_PIC[epic_id]


def wanted_fields(item, milestone_due, swp):
    """Planned Project field values for one item as {field: (kind, value)}.

    Select / iteration values are option / sprint names. The sync pushes a field only when this
    planned value changes, so Status (always Todo here) is written once and then left to the team.
    swp is the PL-reviewed SWP map from backlog-swp-reviewed.json (tasks scored, parents summed).
    """
    wanted = {"Estimate (h)": ("number", item["hours"]), "Status": ("select", "Todo")}
    if item["key"] in swp:
        wanted["SWP"] = ("number", swp[item["key"]])
    if item["pic"]:
        wanted["PIC"] = ("select", item["pic"])
    if item["kind"] == "TASK":
        wanted["Công đoạn"] = ("select", STAGE_OF_LAYER[item["layer"]])
        wanted["Priority"] = ("select", "High" if item["p0"] else "Normal")
        wanted["Iteration"] = ("iteration", item["sprint"])
    elif item["kind"] == "EPIC":
        wanted["Due Date"] = ("date", milestone_due[item["milestone"]])
    return wanted
