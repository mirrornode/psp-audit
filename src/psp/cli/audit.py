from pathlib import Path
import json
from psp.github_client import GitHubClient
from psp.risk.engine import scan_workflow


def run_audit(owner_repo, snapshot=False, token=None):
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
        workflows_meta.append({
            "name": wf["name"],
            "path": wf["path"],
            "findings": len(findings),
        })

    recoverable = [f for f in all_findings if f["severity"] != "High"]
    changed = [
        {
            "sha": c["sha"][:7],
            "message": c["commit"]["message"].splitlines()[0],
            "author": c["commit"]["author"]["name"],
        }
        for c in commits
    ]

    next_steps = []
    rules_hit = {f["rule"] for f in all_findings}
    if "pull_request_target" in rules_hit:
        next_steps.append("Review pull_request_target workflows immediately — high pwn risk.")
    if "mutable_action_tags" in rules_hit:
        next_steps.append("Pin all action refs to full commit SHAs.")
    if "missing_permissions_block" in rules_hit:
        next_steps.append("Add permissions: read-all to all workflows.")
    if "unsafe_shell_event_payload" in rules_hit:
        next_steps.append("Move github.event.* references into env vars before shell use.")
    if not next_steps:
        next_steps.append("No critical issues detected. Maintain current posture.")

    settings = {}
    if snapshot:
        settings = {
            "default_branch": repo_data.get("default_branch"),
            "private": repo_data.get("private"),
            "has_issues": repo_data.get("has_issues"),
            "has_wiki": repo_data.get("has_wiki"),
        }

    return {
        "schema_version": 1,
        "owner": owner,
        "repo": repo,
        "refs": [r["name"] for r in refs],
        "tags": [t["name"] for t in tags],
        "workflows": workflows_meta,
        "settings_snapshot": settings,
        "Risky": all_findings,
        "Changed": changed,
        "Recoverable": recoverable,
        "NextSteps": next_steps,
    }


def save_audit(payload, out_file="audit.json"):
    path = Path(out_file)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return path
