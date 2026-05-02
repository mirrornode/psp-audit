import json
from datetime import datetime, timezone
from pathlib import Path

SEVERITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}

def _timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def _group_findings(findings):
    grouped = {}
    for f in findings:
        rule = f.get("rule", f.get("id", "unknown"))
        grouped.setdefault(rule, []).append(f)
    return grouped

def render_txt(data):
    repo = f"{data.get('owner')}/{data.get('repo')}"
    risky = sorted(data.get("Risky", []), key=lambda f: SEVERITY_ORDER.get(f.get("severity", "Low"), 2))
    recoverable = data.get("Recoverable", [])
    changed = data.get("Changed", [])
    next_steps = data.get("NextSteps", [])
    workflows = data.get("workflows", [])
    high = [f for f in risky if f.get("severity") == "High"]
    medium = [f for f in risky if f.get("severity") == "Medium"]

    lines = [
        "=" * 60,
        "  PSP INCIDENT REPORT",
        f"  {repo}",
        f"  Generated: {_timestamp()}",
        "=" * 60, "",
        "SUMMARY", "-" * 40,
        f"  Workflows scanned : {len(workflows)}",
        f"  Total findings    : {len(risky)}",
        f"  High severity     : {len(high)}",
        f"  Medium severity   : {len(medium)}",
        f"  Recoverable       : {len(recoverable)}",
        f"  Recent commits    : {len(changed)}", "",
    ]
    if high:
        lines += ["HIGH SEVERITY", "-" * 40]
        for f in high:
            lines += [f"  [{f['id']}] {f['description']}", f"  File: {f.get('file','')}", f"  Fix:  {f.get('remediation','')}", ""]
    if medium:
        lines += ["MEDIUM SEVERITY", "-" * 40]
        for rule, findings in _group_findings(medium).items():
            lines += [f"  [{findings[0]['id']}] {findings[0]['description']}", f"  Affects {len(findings)} workflow(s)", f"  Fix: {findings[0].get('remediation','')}", ""]
    if next_steps:
        lines += ["NEXT STEPS", "-" * 40]
        for i, s in enumerate(next_steps, 1):
            lines.append(f"  {i}. {s}")
        lines.append("")
    if changed:
        lines += ["RECENT COMMITS", "-" * 40]
        for c in changed[:10]:
            lines.append(f"  {c['sha']}  {c['author'][:20]:<20}  {c['message'][:50]}")
        lines.append("")
    lines += ["=" * 60, "  END OF REPORT", "=" * 60]
    return "\n".join(lines)

def render_markdown(data):
    repo = f"{data.get('owner')}/{data.get('repo')}"
    risky = sorted(data.get("Risky", []), key=lambda f: SEVERITY_ORDER.get(f.get("severity", "Low"), 2))
    recoverable = data.get("Recoverable", [])
    changed = data.get("Changed", [])
    next_steps = data.get("NextSteps", [])
    workflows = data.get("workflows", [])
    high = [f for f in risky if f.get("severity") == "High"]
    medium = [f for f in risky if f.get("severity") == "Medium"]

    lines = [
        f"# PSP Incident Report: `{repo}`",
        f"_Generated: {_timestamp()}_", "",
        "## Summary", "",
        "| Metric | Count |", "|--------|-------|",
        f"| Workflows scanned | {len(workflows)} |",
        f"| Total findings | {len(risky)} |",
        f"| High severity | {len(high)} |",
        f"| Medium severity | {len(medium)} |",
        f"| Recoverable | {len(recoverable)} |", "",
    ]
    if high:
        lines += ["## High Severity Findings", ""]
        for f in high:
            lines += [f"### `{f['id']}` - {f['description']}", f"- **File:** `{f.get('file','')}`", f"- **Remediation:** {f.get('remediation','')}", ""]
    if medium:
        lines += ["## Medium Severity Findings", ""]
        for rule, findings in _group_findings(medium).items():
            lines += [f"### `{findings[0]['id']}` - {findings[0]['description']}", f"- **Affects:** {len(findings)} workflow(s)", f"- **Remediation:** {findings[0].get('remediation','')}", ""]
    if next_steps:
        lines += ["## Next Steps", ""]
        for i, s in enumerate(next_steps, 1):
            lines.append(f"{i}. {s}")
        lines.append("")
    if changed:
        lines += ["## Recent Commits", "", "| SHA | Author | Message |", "|-----|--------|---------|"]
        for c in changed[:10]:
            lines.append(f"| `{c['sha']}` | {c['author']} | {c['message'][:60]} |")
        lines.append("")
    return "\n".join(lines)

def render_report(audit_file, fmt="txt"):
    path = Path(audit_file)
    if not path.exists():
        raise FileNotFoundError(f"Audit file not found: {audit_file}")
    data = json.loads(path.read_text())
    if fmt == "json":
        return json.dumps(data, indent=2)
    if fmt == "txt":
        return render_txt(data)
    if fmt == "md":
        return render_markdown(data)
    raise ValueError("format must be json|txt|md")
