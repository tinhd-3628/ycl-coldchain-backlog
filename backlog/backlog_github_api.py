"""Thin wrappers around the gh CLI shared by the LAB-5 backlog scripts (REST + GraphQL, JSON in/out)."""
import json
import subprocess


def gh(args, payload=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    run = subprocess.run(["gh", *args], input=data, capture_output=True)
    if run.returncode:
        raise RuntimeError(run.stderr.decode("utf-8", "replace"))
    out = run.stdout.decode("utf-8")
    return json.loads(out) if out.strip() else None


def graphql(query, **variables):
    return gh(["api", "graphql", "--input", "-"], {"query": query, "variables": variables})["data"]


PROJECT_QUERY = """query($login:String!,$n:Int!){user(login:$login){projectV2(number:$n){id fields(first:50){nodes{
 ... on ProjectV2Field{id name} ... on ProjectV2SingleSelectField{id name options{id name}}
 ... on ProjectV2IterationField{id name configuration{iterations{id title}}}}}}}}"""
SET_FIELD = """mutation($p:ID!,$i:ID!,$f:ID!,$v:ProjectV2FieldValue!){
 updateProjectV2ItemFieldValue(input:{projectId:$p,itemId:$i,fieldId:$f,value:$v}){projectV2Item{id}}}"""


def project_with_fields(owner, number):
    """(project node id, {field name: field}) for a user-owned Project."""
    project = graphql(PROJECT_QUERY, login=owner, n=number)["user"]["projectV2"]
    return project["id"], {f["name"]: f for f in project["fields"]["nodes"] if f}


def field_value(field, kind, value):
    """GraphQL field value; single-select options and iterations are referenced by their names."""
    if kind == "select":
        return {"singleSelectOptionId": next(o["id"] for o in field["options"] if o["name"] == value)}
    if kind == "iteration":
        return {"iterationId": next(i["id"] for i in field["configuration"]["iterations"] if i["title"] == value)}
    return {kind: value}


def set_field(project_id, item_id, field, kind, value):
    graphql(SET_FIELD, p=project_id, i=item_id, f=field["id"], v=field_value(field, kind, value))
