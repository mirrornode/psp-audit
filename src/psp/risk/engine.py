import re
import yaml

RULES = [
    "pull_request_target",
    "unsafe_shell_event_payload",
    "mutable_action_tags",
    "missing_permissions_block",
    "broad_token_write_access",
]


def _mutable_ref(ref):
    sha = re.compile(r"^[0-9a-f]{40}$")
    semver = re.compile(r"^v?[0-9]+(\.[0-9]+)*$")
    return not sha.match(ref) and not semver.match(ref)


def scan_workflow(filename, content):
    findings = []
    try:
        wf = yaml.safe_load(content)
    except yaml.YAMLError:
        return findings
    if not isinstance(wf, dict):
        return findings

    on = wf.get("on", wf.get(True, {}))
    triggers = []
    if isinstance(on, dict):
        triggers = list(on.keys())
    elif isinstance(on, list):
        triggers = on
    elif isinstance(on, str):
        triggers = [on]

    if "pull_request_target" in triggers:
        findings.append({
            "id": "R-001",
            "rule": "pull_request_target",
            "description": "Workflow uses pull_request_target trigger",
            "severity": "High",
            "file": filename,
            "line": 1,
            "remediation": "Replace with pull_request or scope permissions tightly and never checkout untrusted code.",
        })

    jobs = wf.get("jobs", {})
    has_top_perms = "permissions" in wf
    all_jobs_have_perms = all("permissions" in j for j in jobs.values()) if jobs else False
    if not has_top_perms and not all_jobs_have_perms:
        findings.append({
            "id": "R-004",
            "rule": "missing_permissions_block",
            "description": "No permissions block at workflow or job level",
            "severity": "Medium",
            "file": filename,
            "line": 1,
            "remediation": "Add permissions: read-all at workflow level, override per job as needed.",
        })

    perms = wf.get("permissions", {})
    if perms == "write-all" or (isinstance(perms, dict) and perms.get("contents") == "write"):
        findings.append({
            "id": "R-005",
            "rule": "broad_token_write_access",
            "description": "Workflow grants broad write permissions",
            "severity": "High",
            "file": filename,
            "line": 1,
            "remediation": "Scope to minimum required. Prefer contents: read.",
        })

    for job_name, job in jobs.items():
        steps = job.get("steps", []) if isinstance(job, dict) else []
        for i, step in enumerate(steps):
            if not isinstance(step, dict):
                continue
            uses = step.get("uses", "")
            if uses and "@" in uses:
                ref = uses.split("@", 1)[1]
                if _mutable_ref(ref):
                    findings.append({
                        "id": "R-003",
                        "rule": "mutable_action_tags",
                        "description": f"Mutable action ref {uses!r} in job {job_name!r}",
                        "severity": "Medium",
                        "file": filename,
                        "line": i + 1,
                        "remediation": f"Pin to full commit SHA: {uses.split('@')[0]}@<sha>",
                    })
            run = step.get("run", "")
            if run and "${{ github.event." in run:
                findings.append({
                    "id": "R-002",
                    "rule": "unsafe_shell_event_payload",
                    "description": f"Shell step in job {job_name!r} interpolates github.event payload",
                    "severity": "High",
                    "file": filename,
                    "line": i + 1,
                    "remediation": "Pass event data via env vars, never interpolate directly into shell.",
                })

    return findings


def baseline_findings():
    return [{
        "id": "R-001",
        "description": "pull_request_target used in workflow",
        "severity": "High",
        "file": ".github/workflows/ci.yml",
        "line": 12,
        "remediation": "Use safer triggers and least-privilege permissions.",
    }]
