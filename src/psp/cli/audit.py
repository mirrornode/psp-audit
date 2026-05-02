from pathlib import Path
from datetime import datetime, timezone
import json
from psp.github_client import GitHubClient
from psp.risk.engine import scan_workflow


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _verdict(findings):
    severities = {f["severity"] for f in findings}
    if "High" in severities:
        return "blocked"
    if "Medium" in severities:
        return "review"
    return "safe"


def _executor_class(verdict):
    return {"blocked": "none", "review": "restricted", "safe": "any"}[verdict]


def _operator_message(owner, repo, verdict, findings):
    ref = f"{owner}/{repo}"
    if verdict == "safe":
        return f"{ref} is safe for agent execution."
    if verdict == "review":
        return f"{ref} requires review before agent execution."
    high = [f for f in findings if f["severity"] == "High"]
    primary = high[0]["description"] if high else "High severity finding detected."
    return f"{ref} is blocked. {primary}."


def _recoverability(findings):
    severity_order = {"High": 0, "Medium": 1, "Low": 2}
    sorted_findings = sorted(findings, key=lambda f: severity_order.get(f["severity"], 2))
    seen_rules = set()
    steps = []
    for f in sorted_findings:
        rule = f.get("rule", f["id"])
        if rule not in seen_rules:
            steps.append(f["remediation"])
            seen_rules.add(rule)
    unique_files = {f.get("file", "") for f in findings}
    blocking_count = sum(1 for f in findings if f["severity"] == "High")
    return {"steps": steps, "estimated_files": len(unique_files), "blocking_count": blocking_count}


def _trust_drift(findings, baseline=None):
    if baseline is None:
        return {"snapshot_date": None, "new_findings": [], "resolved_findings": [], "drift_direction": "no_baseline"}
    current_ids = {f["id"] for f in findings}
    baseline_ids = {f["id"] for f in baseline.get("findings", [])}
    new = list(current_ids - baseline_ids)
    resolved = list(baseline_ids - current_ids)
    if not new and not resolved:
        direction = "stable"
    elif len(resolved) > len(new):
        direction = "improving"
    elif len(new) > len(resolved):
        direction = "degrading"
    else:
        direction = "stable"
    return {"snapshot_date": baseline.get("audited_at"), "new_findings": new, "resolved_findings": resolved, "drift_direction": direction}


def run_audit(owner_repo, snapshot=False, token=None, baseline=None):
    if owner_repo.count("/") != 1:
        raise ValueError("owner/repo required")
    owner, repo = owner_repo.split("/", 1)
    client = GitHubClient(token=token)
    repo_data = client.get_repo(owner, repo)
    refs = client.get_refs(owner, repo)
    tags = client.get_tags(owner, repo)
    workflow_files = client.get_workflow_files(owner, repo)
    commits = client.get_commits(owner, repo, per_page=20)
    all_findings = []
    workflows_meta = []
    for wf in workflow_files:
        content = client.get_file_content(owner, repo, wf["path"])
        findings = scan_workflow(wf["path"], content)
        all_findings.extend(findings)
        workflows_meta.append({"name": wf["name"], "path": wf["path"], "findings": len(findings)})
    verdict = _verdict(all_findings)
    blocking_ids = [f["id"] for f in all_findings if f["severity"] == "High"]
    review_ids = [f["id"] for f in all_findings if f["severity"] == "Medium"]
    changed = [{"sha": c["sha"][:7], "message": c["commit"]["message"].splitlines()[0], "author": c["commit"]["author"]["name"]} for c in commits]
    settings = {}
    if snapshot:
        settings = {"default_branch": repo_data.get("default_branch"), "private": repo_data.get("private"), "has_issues": repo_data.get("has_issues"), "has_wiki": repo_data.get("has_wiki")}
    recovery = _recoverability(all_findings)
    return {
        "schema_version": 2,
        "owner": owner,
        "repo": repo,
        "audited_at": _now(),
        "refs": [r["name"] for r in refs],
        "tags": [t["name"] for t in tags],
        "workflows": workflows_meta,
        "settings_snapshot": settings,
        "findings": all_findings,
        "Risky": all_findings,
        "Changed": changed,
        "Recoverable": [f for f in all_findings if f["severity"] != "High"],
        "NextSteps": recovery["steps"],
        "operator_message": _operator_message(owner, repo, verdict, all_findings),
        "trust_drift": _trust_drift(all_findings, baseline),
        "agent_policy": {"verdict": verdict, "blocking_rule_ids": blocking_ids, "review_rule_ids": review_ids, "executor_class": _executor_class(verdict)},
        "recoverability": recovery,
    }


def save_audit(payload, out_file="audit.json"):
    path = Path(out_file)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return path
