import json
from pathlib import Path

def render_report(audit_file: str, fmt: str = "json") -> str:
    path = Path(audit_file)
    if not path.exists():
        raise FileNotFoundError(audit_file)
    data = json.loads(path.read_text())
    if fmt == "json":
        return json.dumps(data, indent=2)
    if fmt == "txt":
        return "\n".join([
            f"Repo: {data.get('owner')}/{data.get('repo')}",
            f"Risks: {len(data.get('Risky', []))}",
            f"Recoverable: {len(data.get('Recoverable', []))}",
        ])
    if fmt == "pdf":
        return "PDF generation placeholder"
    raise ValueError("format must be json|txt|pdf")
