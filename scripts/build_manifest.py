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
TTS = os.path.join(ROOT, "tts")


def audio_for(module_id, n):
    """Wire a section's narration: return ``audio/<stem>.wav`` for the section at
    1-based notebook order ``n``, or ``None`` when its ``.tts`` is silent (the
    intro-overview opener and recap closer are intentionally skipped, leaving gaps
    in the ``NN-SS`` numbering). Matched by the ``NN-SS`` prefix only — never by the
    slug — so a heading edit can't break the audio wiring. The ``.wav`` itself is
    generated separately (``scripts/colab_generate_audio.ipynb``); this references it
    by the `.tts` that is the source of truth for "this section is narrated"."""
    prefix = f"{module_id[:2]}-{n:02d}-"
    for f in sorted(os.listdir(TTS)):
        if f.startswith(prefix) and f.endswith(".tts"):
            return f"audio/{f[:-4]}.wav"
    return None


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
    # Modules 07, 08, 11–14 have no dedicated scene yet, so each rides the most
    # topically related existing scene as a BACKDROP: full-strength (no highlight/
    # focus, since the scene's node ids don't match this module's content), every
    # section on the spine, the first section the hook. `backdrop=True` drives that
    # default in the section loop below. Give a module its own scene later by adding
    # the scene in graphl-ux and replacing the entry here with a real overlay map.
    dict(
        id="03-compute-core-ec2-elb-autoscaling",
        title="Compute Core — EC2, ELB & Auto Scaling",
        notebook="notebooks/03-compute-core-ec2-elb-autoscaling.ipynb",
        scene="aws-vpc",
        backdrop=True,
        overlay={},
    ),
    dict(
        id="04-serverless-and-containers",
        title="Serverless & Containers",
        notebook="notebooks/04-serverless-and-containers.ipynb",
        scene="aws-global",
        backdrop=True,
        overlay={},
    ),
    dict(
        id="05-storage-s3-ebs-efs-fsx",
        title="Storage — S3, EBS, EFS & FSx",
        notebook="notebooks/05-storage-s3-ebs-efs-fsx.ipynb",
        scene="aws-data-engineering",
        backdrop=True,
        overlay={},
    ),
    dict(
        id="07-dns-cdn-and-edge",
        title="DNS, CDN & Edge",
        notebook="notebooks/07-dns-cdn-and-edge.ipynb",
        scene="aws-global",
        backdrop=True,
        overlay={},
    ),
    dict(
        id="08-relational-databases-and-caching",
        title="Relational Databases & Caching",
        notebook="notebooks/08-relational-databases-and-caching.ipynb",
        scene="aws-data-engineering",
        backdrop=True,
        overlay={},
    ),
    dict(
        id="11-security-services",
        title="Security Services",
        notebook="notebooks/11-security-services.ipynb",
        scene="aws-iam",
        backdrop=True,
        overlay={},
    ),
    dict(
        id="12-observability-and-governance",
        title="Observability & Governance",
        notebook="notebooks/12-observability-and-governance.ipynb",
        scene="aws-iam",
        backdrop=True,
        overlay={},
    ),
    dict(
        id="13-ha-dr-cost-and-migration",
        title="HA/DR, Cost & Migration",
        notebook="notebooks/13-ha-dr-cost-and-migration.ipynb",
        scene="aws-global",
        backdrop=True,
        overlay={},
    ),
    dict(
        id="14-well-architected-and-saa-exam-prep",
        title="Well-Architected & SAA Exam Prep",
        notebook="notebooks/14-well-architected-and-saa-exam-prep.ipynb",
        scene="aws-global",
        backdrop=True,
        overlay={},
    ),
]

presentations = []
for m in MODULES:
    secs = []
    backdrop = m.get("backdrop", False)
    for i, h in enumerate(headings(os.path.basename(m["notebook"]))):
        o = m["overlay"].get(h, {})
        # A backdrop module defaults every section onto the spine and makes the
        # first section the hook; an overlaid module takes its flags from the map.
        spine = True if backdrop else bool(o.get("spine", False))
        sec = {"heading": h, "scene": m["scene"], "spine": spine}
        role = o.get("role") or ("hook" if backdrop and i == 0 else None)
        if role:
            sec["role"] = role
        if o.get("highlight"):
            sec["highlight"] = o["highlight"]
        if o.get("focus"):
            sec["focus"] = o["focus"]
        audio = audio_for(m["id"], i + 1)
        if audio:
            sec["audio"] = audio
        secs.append(sec)
    presentations.append({
        "id": m["id"],
        "title": m["title"],
        "notebook": m["notebook"],
        "defaultScene": m["scene"],
        "sections": secs,
    })

# Keep the course in module order regardless of how MODULES is listed, since the
# app flattens presentations into one continuous page list in array order.
presentations.sort(key=lambda p: p["id"])

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
