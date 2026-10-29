"""Add the extra Project fields and the two table views modelled on framgia/projects/281 (views 32 and 15).

Mapping from the reference project: Target Version -> Iteration, Phase -> Milestone (UAT 1st/2nd/3rd),
Estimated time -> Estimate (h). Công đoạn / Priority / dates / spent time / progress are created here.
Idempotent: a field or view is created only when none with the same name exists. The Iteration field's
sprints are set from backlog-breakdown.yaml (existing sprints keep their IDs, so item assignments survive).
Run before sync-github-backlog-issues.py, which fills Công đoạn / Priority / Due Date.
Usage: python setup-github-project-fields-and-views.py
"""
import pathlib

import yaml

from backlog_github_api import gh, graphql
from backlog_project_fields import PIC_OPTIONS, PRIORITY_OPTIONS, STAGE_OPTIONS

OWNER = "tinhd-3628"
PROJECT_NO = 1
NEW_FIELDS = [("Công đoạn", "SINGLE_SELECT", STAGE_OPTIONS), ("Priority", "SINGLE_SELECT", PRIORITY_OPTIONS),
              ("Start Date", "DATE", None), ("Due Date", "DATE", None),
              ("Spent time (h)", "NUMBER", None), ("Progress (%)", "NUMBER", None)]
VIEWS = [
    {"name": "Project Overall", "filter": "-is:closed label:type:epic",
     "fields": ["Title", "Assignees", "Iteration", "Status", "Milestone", "Sub-issues progress", "Due Date",
                "Estimate (h)", "SWP"],
     "group_by": "Milestone", "sort_by": None},
    {"name": "Sprint Detail view", "filter": "-status:Done -label:type:story -label:type:epic",
     "fields": ["Title", "Assignees", "PIC", "Iteration", "Status", "Labels", "Milestone", "Estimate (h)",
                "Spent time (h)", "Start Date", "Due Date", "Priority", "Progress (%)", "SWP", "Công đoạn"],
     "group_by": "Công đoạn", "sort_by": ("Priority", "desc")},
]
CREATE_FIELD = """mutation($p:ID!,$n:String!,$t:ProjectV2CustomFieldType!,$o:[ProjectV2SingleSelectFieldOptionInput!]){
 createProjectV2Field(input:{projectId:$p,name:$n,dataType:$t,singleSelectOptions:$o}){projectV2Field{... on ProjectV2FieldCommon{id}}}}"""
PROJECT_QUERY = """query($login:String!,$n:Int!){user(login:$login){projectV2(number:$n){id
 views(first:50){nodes{name}}
 field(name:"Iteration"){... on ProjectV2IterationField{id configuration{iterations{id title}}}}}}}"""
UPDATE_ITERATIONS = """mutation($f:ID!,$c:ProjectV2IterationFieldConfigurationInput!){
 updateProjectV2Field(input:{fieldId:$f,iterationConfiguration:$c}){projectV2Field{... on ProjectV2FieldCommon{id}}}}"""
PIC_QUERY = """query($login:String!,$n:Int!){user(login:$login){projectV2(number:$n){
 field(name:"PIC"){... on ProjectV2SingleSelectField{id options{id name color description}}}}}}"""
UPDATE_OPTIONS = """mutation($f:ID!,$o:[ProjectV2SingleSelectFieldOptionInput!]){
 updateProjectV2Field(input:{fieldId:$f,singleSelectOptions:$o}){projectV2Field{... on ProjectV2FieldCommon{id}}}}"""


def ensure_pic_options():
    """Add missing PIC options. Existing options are resent with their ids, which keeps item values."""
    field = graphql(PIC_QUERY, login=OWNER, n=PROJECT_NO)["user"]["projectV2"]["field"]
    have = {o["name"] for o in field["options"]}
    missing = [n for n in PIC_OPTIONS if n not in have]
    if missing:
        options = field["options"] + [{"name": n, "color": "GRAY", "description": ""} for n in missing]
        graphql(UPDATE_OPTIONS, f=field["id"], o=options)
    print(f"PIC options added: {missing or 'none'}")


def sync_sprints(iteration_field):
    """Make the Iteration field hold exactly the sprints in backlog-breakdown.yaml (2-week, with breaks)."""
    data = yaml.safe_load((pathlib.Path(__file__).parent / "backlog-breakdown.yaml").read_text(encoding="utf-8"))
    days = data["sprint_duration_days"]
    ids = {i["title"]: i["id"] for i in iteration_field["configuration"]["iterations"]}
    iterations = [{"title": sp["title"], "startDate": str(sp["start"]), "duration": days,
                   **({"id": ids[sp["title"]]} if sp["title"] in ids else {})} for sp in data["sprints"]]
    config = {"startDate": iterations[0]["startDate"], "duration": days, "iterations": iterations}
    graphql(UPDATE_ITERATIONS, f=iteration_field["id"], c=config)
    print("sprints: " + ", ".join(f"{i['title']} {i['startDate']}" for i in iterations))


def rest_fields():
    """{name: numeric field id} — the views REST API takes numeric ids, not GraphQL node ids."""
    return {f["name"]: f["id"] for f in gh(["api", f"users/{OWNER}/projectsV2/{PROJECT_NO}/fields?per_page=100"])}


def main():
    project = graphql(PROJECT_QUERY, login=OWNER, n=PROJECT_NO)["user"]["projectV2"]
    existing = rest_fields()
    for name, data_type, options in NEW_FIELDS:
        if name in existing:
            print(f"field exists: {name}")
            continue
        opts = [{"name": o, "color": "GRAY", "description": ""} for o in options] if options else None
        graphql(CREATE_FIELD, p=project["id"], n=name, t=data_type, o=opts)
        print(f"field created: {name}")
    ensure_pic_options()
    sync_sprints(project["field"])
    field_ids = rest_fields()
    view_names = {v["name"] for v in project["views"]["nodes"]}
    for view in VIEWS:
        if view["name"] in view_names:
            print(f"view exists: {view['name']}")
        else:
            payload = {"name": view["name"], "layout": "table", "filter": view["filter"],
                       "visible_fields": [field_ids[f] for f in view["fields"]],
                       "group_by": [field_ids[view["group_by"]]]}
            if view["sort_by"]:
                payload["sort_by"] = [[field_ids[view["sort_by"][0]], view["sort_by"][1]]]
            # The docs name the path parameter user_id, but the endpoint resolves the login (numeric id -> 404).
            created = gh(["api", f"users/{OWNER}/projectsV2/{PROJECT_NO}/views", "--method", "POST",
                          "--input", "-"], payload)
            print(f"view created: {view['name']} (#{created.get('number')})")


if __name__ == "__main__":
    main()
