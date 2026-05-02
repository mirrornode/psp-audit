from datetime import datetime, timezone

def severity_label(score: int) -> str:
    if score >= 80:
        return "critical"
    if score >= 60:
        return "high"
    if score >= 30:
        return "medium"
    if score > 0:
        return "low"
    return "none"

def status_from(score: int) -> str:
    if score >= 80:
        return "blocked"
    if score >= 30:
        return "review"
    return "safe"

def operator_message(status: str) -> str:
    if status == "blocked":
        return "Stop merge-, release-, and deploy-capable agents immediately."
    if status == "review":
        return "Pause sensitive agent actions until repo trust is verified."
    return "Agent execution may proceed under normal policy."

def actor_policy(status: str) -> dict:
    if status == "blocked":
        return {
            "coding_agent": {"allowed_operations": ["read"], "blocked_operations": ["merge", "push", "workflow_dispatch"]},
            "deploy_agent": {"allowed_operations": ["read"], "blocked_operations": ["deploy", "release", "workflow_dispatch"]},
            "release_bot": {"allowed_operations": ["read"], "blocked_operations": ["tag", "release", "publish"]},
            "comment_bot": {"allowed_operations": ["read", "issue_comment"], "blocked_operations": []},
        }
    if status == "review":
        return {
            "coding_agent": {"allowed_operations": ["read", "open_pull_request"], "blocked_operations": ["merge", "push"]},
            "deploy_agent": {"allowed_operations": ["read"], "blocked_operations": ["deploy", "release"]},
            "release_bot": {"allowed_operations": ["read"], "blocked_operations": ["tag", "release", "publish"]},
            "comment_bot": {"allowed_operations": ["read", "issue_comment"], "blocked_operations": []},
        }
    return {
        "coding_agent": {"allowed_operations": ["read", "open_pull_request"], "blocked_operations": []},
        "deploy_agent": {"allowed_operations": ["read", "deploy"], "blocked_operations": []},
        "release_bot": {"allowed_operations": ["read", "tag", "release"], "blocked_operations": []},
        "comment_bot": {"allowed_operations": ["read", "issue_comment"], "blocked_operations": []},
    }

def build_envelope(audit: dict) -> dict:
    findings = audit.get("Risky", [])
    score = 0
    for f in findings:
        sev = str(f.get("severity", "")).lower()
        if sev == "high":
            score += 20
        elif sev == "medium":
            score += 8
        elif sev == "low":
            score += 3
        else:
            score += 1
    score = min(score, 100)
    status = status_from(score)
    return {
        "schema_version": 2,
        "repo": f"{audit.get('owner','unknown')}/{audit.get('repo','unknown')}",
        "status": status,
        "operator_message": operator_message(status),
        "severity_score": score,
        "severity_label": severity_label(score),
        "summary": f"Repository has {len(findings)} findings requiring {status} handling.",
        "findings": findings,
        "trust_drift": {
            "changed": audit.get("Changed", []),
            "summary": f"{len(audit.get('Changed', []))} trust-relevant changes detected."
        },
        "recoverability": {
            "items": audit.get("Recoverable", []),
            "summary": f"{len(audit.get('Recoverable', []))} recoverable items identified."
        },
        "agent_policy": actor_policy(status),
        "next_steps": audit.get("NextSteps", []),
        "generated_at": datetime.now(timezone.utc).isoformat()
    }
