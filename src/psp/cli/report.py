import json
from pathlib import Path


def render_report(audit_file, fmt="txt"):
    path = Path(audit_file)
    if not path.exists():
        raise FileNotFoundError(audit_file)
    data = json.loads(path.read_text())

    if fmt == "json":
        return json.dumps(data, indent=2)

    if fmt == "txt":
        lines = [
            f"Repo:        {data.get('owner')}/{data.get('repo')}",
            f"Branches:    {len(data.get('refs', []))}",
            f"Tags:        {len(data.get('tags', []))}",
            f"Workflows:   {len(data.get('workflows', []))}",
            f"Risks:       {len(data.get('Risky', []))}",
            f"Recoverable: {len(data.get('Recoverable', []))}",
            "",
            "Next steps:",
        ]
        for s in data.get("NextSteps", []):
            lines.append(f"  → {s}")
        return "\n".join(lines)

    raise ValueError("format must be json|txt")
