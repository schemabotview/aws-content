#!/usr/bin/env python3
"""Generate aws-content/manifest.json — wire each module's notebook `## ` sections
to its scene + per-section overlay (spine / role / highlight / focus).

The notebook is the source of truth for prose; this only *wires*. Headings are read
straight from the notebooks so the manifest can never drift from the actual `## `
text. Re-run after editing a heading. Only the five modules that have a dedicated
scene are wired today (01 global · 02 iam · 06 vpc · 09/10 data-engineering); the
other nine notebooks ship in notebooks/ but are not yet wired.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.join(ROOT, "notebooks")


def headings(nb_file):
    nb = json.load(open(os.path.join(NB, nb_file)))
    out = []
    for c in nb["cells"]:
        if c["cell_type"] != "markdown":
            continue
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        for line in src.splitlines():
            if line.startswith("## "):
                out.append(line[3:].strip())
    return out


# overlay[heading] = dict(spine?, role?, highlight=[...], focus=str|[...])
MODULES = [
    dict(
        id="01-cloud-and-aws-foundations",
        title="Cloud & AWS Foundations",
        notebook="notebooks/01-cloud-and-aws-foundations.ipynb",
        scene="aws-global",
        overlay={
            "What cloud actually means": dict(spine=True, role="hook", focus="awsf-service-models", highlight=["awsf-service-models"]),
            "Traditional IT vs. Cloud": dict(spine=True, focus="awsf-service-models", highlight=["awsf-svc-you", "awsf-service-models"]),
            "Three Service Models": dict(spine=True, focus="awsf-service-models", highlight=["awsf-svc-saas", "awsf-svc-paas", "awsf-svc-iaas"]),
            "Deployment Models": dict(spine=True, focus="awsf-deployment-models", highlight=["awsf-deployment-models"]),
            "AWS Global Infrastructure": dict(spine=True, focus="awsf-global-infra", highlight=["awsf-global-infra"]),
            "Regions": dict(spine=True, focus="awsf-region", highlight=["awsf-region"]),
            "Availability Zones (AZs)": dict(spine=True, focus="awsf-region", highlight=["awsf-az-a", "awsf-az-b", "awsf-az-c"]),
            "Edge Locations": dict(focus="awsf-global-infra", highlight=["awsf-global-infra"]),
            "Beyond Regions: Local Zones, Wavelength, Outposts": dict(focus="awsf-dep-private", highlight=["awsf-dep-private", "awsf-priv-onprem"]),
            "How You Talk to AWS": dict(spine=True, focus="awsf-connecting", highlight=["awsf-connecting"]),
            "Shared Responsibility — Primer": dict(focus="awsf-connecting", highlight=["awsf-conn-apis"]),
            "Choosing a Region": dict(focus="awsf-region", highlight=["awsf-region"]),
        },
    ),
    dict(
        id="02-iam-organizations-and-account-security",
        title="IAM, Organizations & Account Security",
        notebook="notebooks/02-iam-organizations-and-account-security.ipynb",
        scene="aws-iam",
        overlay={
            "The Root User": dict(spine=True, role="hook", focus="anatomy-banner", highlight=["anat-root"]),
            "What IAM is": dict(spine=True, focus="anatomy-banner", highlight=["anatomy-banner"]),
            "Three Identity Types": dict(spine=True, focus="anatomy-banner", highlight=["anat-users", "anat-roles", "anat-policies"]),
            "Role Assumption — Three Policies, Two Sides": dict(spine=True, focus="handshake", highlight=["handshake"]),
            "Policies — Shape and Types": dict(focus="anatomy-banner", highlight=["anat-policies"]),
            "The Five Policy Slots": dict(focus="eval-col", highlight=["eval-col"]),
            "Policy Evaluation Order": dict(spine=True, focus="eval-col", highlight=["eval-scp", "eval-boundary", "eval-identity", "eval-resource", "eval-session", "eval-deny"]),
            "Permission Boundaries — Delegated Administration": dict(focus="eval-col", highlight=["eval-boundary"]),
            "STS — Security Token Service": dict(spine=True, focus="handshake", highlight=["sts", "sts-assume"]),
            "Cross-Account Access — Two Patterns": dict(focus="handshake", highlight=["deployer-role", "role-side"]),
            "Identity Federation": dict(spine=True, focus="story", highlight=["corp-idp", "idc"]),
            "AWS Organizations": dict(spine=True, focus="org", highlight=["org"]),
            "Service Control Policies (SCPs)": dict(focus="org", highlight=["org-scps"]),
            "IAM Access Analyzer": dict(focus="anatomy-banner", highlight=["anat-policies"]),
            "ABAC — Tag-Based Access Control": dict(focus="eval-col", highlight=["eval-identity", "eval-resource"]),
            "Useful Condition Keys": dict(focus="eval-col", highlight=["eval-col"]),
            "Multi-Factor Authentication (MFA)": dict(focus="workload-acct", highlight=["breakglass-role"]),
        },
    ),
    dict(
        id="06-vpc-and-connectivity",
        title="VPC & Connectivity",
        notebook="notebooks/06-vpc-and-connectivity.ipynb",
        scene="aws-vpc",
        overlay={
            "What a VPC is": dict(spine=True, role="hook", focus="ans-vpc", highlight=["ans-vpc"]),
            "VPC and CIDR": dict(spine=True, focus="ans-vpc", highlight=["ans-vpc"]),
            "Subnets": dict(spine=True, focus="ans-vpc", highlight=["ans-public-subnet", "ans-private-a", "ans-private-b"]),
            "Internet Gateway and Route Tables": dict(spine=True, focus="ans-aws-cloud", highlight=["ans-igw"]),
            "NAT Gateway": dict(focus="ans-vpc", highlight=["ans-private-a"]),
            "Security Groups": dict(spine=True, focus="ans-vpc", highlight=["ans-sg-alb", "ans-sg-ec2-a", "ans-sg-ec2-b"]),
            "Network ACLs": dict(spine=True, focus="ans-vpc", highlight=["ans-nacl-public", "ans-nacl-a", "ans-nacl-b"]),
            "Elastic IPs": dict(focus="ans-aws-cloud", highlight=["ans-igw"]),
            "DNS Inside the VPC": dict(focus="ans-vpc", highlight=["ans-vpc"]),
            "VPC Flow Logs": dict(focus="ans-vpc", highlight=["ans-vpc"]),
            "Reaching Private Instances": dict(focus="ans-private-a", highlight=["ans-private-a", "ans-asg-a"]),
            "VPC Peering": dict(focus="ans-vpc", highlight=["ans-vpc"]),
            "VPC Endpoints": dict(focus="ans-vpc", highlight=["ans-vpc"]),
            "PrivateLink for Your Own Services": dict(focus="ans-public-subnet", highlight=["ans-nlb"]),
            "Transit Gateway": dict(focus="ans-aws-cloud", highlight=["ans-aws-cloud"]),
            "Site-to-Site VPN": dict(focus="ans-aws-cloud", highlight=["ans-igw"]),
            "Direct Connect": dict(focus="ans-aws-cloud", highlight=["ans-igw"]),
        },
    ),
    dict(
        id="09-nosql-and-analytics",
        title="NoSQL & Analytics",
        notebook="notebooks/09-nosql-and-analytics.ipynb",
        scene="aws-data-engineering",
        overlay={
            "The database zoo at a glance": dict(spine=True, role="hook"),
            "Redshift — Data Warehouse for OLAP": dict(spine=True, focus="query", highlight=["redshift"]),
            "Redshift Architecture": dict(focus="query", highlight=["redshift"]),
            "Loading Data — COPY and Spectrum": dict(focus="query", highlight=["redshift", "s3-serving"]),
            "Distribution and Sort Keys": dict(focus="query", highlight=["redshift"]),
            "Around Redshift — Athena, Glue, EMR, OpenSearch": dict(spine=True, focus="process", highlight=["athena", "glue", "emr", "opensearch"]),
        },
    ),
    dict(
        id="10-integration-and-streaming",
        title="Integration & Streaming",
        notebook="notebooks/10-integration-and-streaming.ipynb",
        scene="aws-data-engineering",
        overlay={
            "Five services, one question": dict(spine=True, role="hook"),
            "Kinesis Data Streams": dict(spine=True, focus="ingest", highlight=["kinesis-streams"]),
            "Consumers — Standard vs Enhanced Fan-Out": dict(focus="ingest", highlight=["kinesis-streams"]),
            "Kinesis Data Firehose": dict(spine=True, focus="ingest", highlight=["firehose"]),
            "Data Analytics on Streams, and MSK": dict(focus="ingest", highlight=["msk", "emr"]),
            "Step Functions — Workflow Orchestration": dict(spine=True, focus="process", highlight=["stepfn-b"]),
            "Retry, Catch, and Failure Modes": dict(focus="process", highlight=["stepfn-b"]),
            "Standard vs Express Workflows": dict(focus="process", highlight=["stepfn-b"]),
        },
    ),
]

presentations = []
for m in MODULES:
    secs = []
    for h in headings(os.path.basename(m["notebook"])):
        o = m["overlay"].get(h, {})
        sec = {"heading": h, "scene": m["scene"], "spine": bool(o.get("spine", False))}
        if o.get("role"):
            sec["role"] = o["role"]
        if o.get("highlight"):
            sec["highlight"] = o["highlight"]
        if o.get("focus"):
            sec["focus"] = o["focus"]
        secs.append(sec)
    presentations.append({
        "id": m["id"],
        "title": m["title"],
        "notebook": m["notebook"],
        "defaultScene": m["scene"],
        "sections": secs,
    })

manifest = {
    "concept": "AWS",
    "design": "DESIGN.md",
    "scenes": [
        {"id": "aws-global", "title": "AWS Foundations — the cloud, end to end", "status": "built"},
        {"id": "aws-iam", "title": "AWS IAM — identities, roles & policy evaluation", "status": "built"},
        {"id": "aws-vpc", "title": "AWS VPC — traffic flow (SG vs NACL)", "status": "built"},
        {"id": "aws-data-engineering", "title": "AWS Data Engineering — the lake-house pipeline", "status": "built"},
    ],
    "presentations": presentations,
}

out = os.path.join(ROOT, "manifest.json")
with open(out, "w") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"wrote {out}: {len(presentations)} modules, {sum(len(p['sections']) for p in presentations)} sections")
