from pathlib import Path
import json

def run_audit(owner_repo: str, snapshot: bool = False) -> dict:
    if owner_repo.count("/") != 1:
        raise ValueError("owner/repo required")
    owner, repo = owner_repo.split("/", 1)
    return {
        "schema_version": 1,
        "owner": owner,
        "repo": repo,
        "refs": [],
        "tags": [],
        "workflows": [],
        "settings_snapshot": snapshot,
        "Risky": [],
        "Changed": [],
        "Recoverable": [],
        "NextSteps": [],
    }

def save_audit(payload: dict, out_file: str = "audit.json") -> Path:
    path = Path(out_file)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return path
