import json

def render_markdown(envelope: dict) -> str:
    lines = [
        f"# PSP Incident Report: `{envelope['repo']}`",
        "",
        f"**Status:** {envelope['status'].upper()}",
        f"**Operator message:** {envelope['operator_message']}",
        f"**Severity score:** {envelope['severity_score']} ({envelope['severity_label']})",
        "",
        "## Summary",
        envelope["summary"],
        "",
        "## Trust Drift",
        envelope["trust_drift"]["summary"],
        "",
        "## Findings",
    ]
    for f in envelope["findings"]:
        lines += [
            f"### `{f.get('id','UNKNOWN')}` - {f.get('description', f.get('title','Finding'))}",
            f"- **Severity:** {f.get('severity','Info')}",
            f"- **File:** {f.get('file','n/a')}",
            f"- **Line:** {f.get('line','n/a')}",
            f"- **Remediation:** {f.get('remediation','n/a')}",
            ""
        ]
    lines += [
        "## Recoverability",
        envelope["recoverability"]["summary"],
        "",
        "## Agent Policy",
    ]
    for actor, policy in envelope["agent_policy"].items():
        lines += [
            f"### {actor}",
            f"- Allowed: {', '.join(policy['allowed_operations']) or 'none'}",
            f"- Blocked: {', '.join(policy['blocked_operations']) or 'none'}",
            ""
        ]
    lines += [
        "## Next Steps",
    ]
    for i, step in enumerate(envelope["next_steps"], 1):
        lines.append(f"{i}. {step}")
    return "\n".join(lines)

def render_text(envelope: dict) -> str:
    return "\n".join([
        f"Repo: {envelope['repo']}",
        f"Status: {envelope['status']}",
        f"Operator: {envelope['operator_message']}",
        f"Severity: {envelope['severity_score']} ({envelope['severity_label']})",
        f"Findings: {len(envelope['findings'])}",
    ])

def render_json(envelope: dict) -> str:
    return json.dumps(envelope, indent=2)
