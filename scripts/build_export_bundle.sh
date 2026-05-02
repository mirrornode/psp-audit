#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p exports
rm -f exports/*

python - <<'PY'
import json
from pathlib import Path
from src.psp.judgment.envelope import build_envelope
from src.psp.renderers.report import render_json, render_text, render_markdown

samples = [
    ("vscode", "examples/vscode-audit.json"),
    ("nextjs", "examples/nextjs-audit.json"),
]

for name, path in samples:
    audit = json.loads(Path(path).read_text())
    envelope = build_envelope(audit)

    Path(f"exports/{name}-envelope.json").write_text(render_json(envelope) + "\n")
    Path(f"exports/{name}-report.txt").write_text(render_text(envelope) + "\n")
    Path(f"exports/{name}-report.md").write_text(render_markdown(envelope) + "\n")
    Path(f"exports/{name}-webhook.json").write_text(json.dumps({
        "repo": envelope["repo"],
        "status": envelope["status"],
        "operator_message": envelope["operator_message"],
        "severity_score": envelope["severity_score"],
        "severity_label": envelope["severity_label"]
    }, indent=2) + "\n")
PY

{
  shasum -a 256 VERSION README.md
  find docs schemas exports -type f | sort | while read -r f; do shasum -a 256 "$f"; done
} > MANIFEST.sha256
