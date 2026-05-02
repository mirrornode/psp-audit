from pathlib import Path
import json
import textwrap

text_files = {
    "docs/psp_handoff.md": """
    # Repo-Snap Pistol Shrimp (psp) MVP Handoff

    ## Overview
    Repo-Snap Pistol Shrimp (psp) is a one-scan, one-report recovery planning tool for GitHub repositories.

    ## Deliverables
    - CLI contract: `docs/psp_cli_contract.md`
    - Risk baseline: `docs/psp_risk_baseline.md`
    - Incident report layout: `docs/psp_incident_report_layout.md`
    - Landing page block: `docs/psp_landing_page_block.md`
    - Snapshot workflow: `docs/psp_snapshot_workflow.md`
    - GitHub App permissions: `docs/psp_github_app_permissions.md`
    - Example payloads: `payloads/`
    - Source stubs: `src/psp/`
    - Tests: `test/`

    ## Hybrid Map trace
    - ROOT: Codex, Engines, Languages, Glyph Index, Token Engine
    - INFRA: GitHub, Vercel, Figma, Trello
    - AI_NETWORK: RIO, Merlin, Claude, Grok, Thea, Perplexity
    - EXTERNAL_MODULES: Story Game, SMI Console, HUD, PSP Audit
    - ACTIVE_TASKS: PSP Audit CLI contract, Risk-pattern baseline, Incident report layout, Landing page block, Snapshot workflow

    ## Success criteria
    - `psp audit owner/repo` validates input and emits a versioned payload
    - `psp report audit.json --format json|txt|pdf` uses deterministic file input
    - all payloads include `schema_version`
    - repo contains docs, payloads, stubs, tests, and changelog

    ## Downstream AI prompts
    ### PSP_CLI_CONTRACT_PROMPT
    Generate the CLI contract for `psp audit owner/repo [--snapshot]` and `psp report audit.json --format json|txt|pdf`.

    ### PSP_RISK_BASELINE_PROMPT
    Generate initial rules for `pull_request_target`, unsafe shell usage, mutable tags, missing permissions blocks, and broad token write access.

    ### INCIDENT_REPORT_LAYOUT_PROMPT
    Generate four report sections: Changed, Risky, Recoverable, NextSteps.

    ### LANDING_PAGE_BLOCK_PROMPT
    Generate static hero, subhead, CTA, pricing snapshot, and accessibility notes.

    ### SNAPSHOT_WORKFLOW_PROMPT
    Define opt-in last clean state snapshots, retention, provenance, and audit integration.

    ## Versioning
    - `v0.4.0`: MVP handoff package
    - `v0.4.x`: non-breaking refinements
    - `v0.5.0`: org-wide scan prototype
    - `v1.0.0`: complete end-to-end MVP
    """,
    "docs/psp_cli_contract.md": """
    # PSP CLI Contract

    ## Commands
    ```bash
    psp audit owner/repo [--snapshot]
    psp report audit.json --format json|txt|pdf
    ```

    ## Flags
    - `--snapshot`: opt-in last clean state capture
    - `--format`: default `json`; options `json|txt|pdf`

    ## Validation
    - `psp audit` requires `owner/repo`
    - `psp report` requires an existing audit file
    - snapshot-dependent operations must fail clearly when snapshot data is missing

    ## Exit codes
    - `0`: success
    - `1`: warnings present
    - `2`: fatal failure

    ## Notes
    Every payload must include `"schema_version": 1`.
    """,
    "docs/psp_risk_baseline.md": """
    # PSP Risk Baseline

    ## Initial rules
    - detect `pull_request_target`
    - detect unsafe shell usage of event payload or env vars
    - detect mutable action tags such as `@latest` and `@v1`
    - detect missing `permissions:` blocks
    - detect broad token write access

    ## Finding fields
    - `id`
    - `description`
    - `severity`
    - `file`
    - `line`
    - `remediation`

    ## Severity
    - High
    - Medium
    - Low
    - Info
    """,
    "docs/psp_incident_report_layout.md": """
    # PSP Incident Report Layout

    ## Sections
    - Changed
    - Risky
    - Recoverable
    - NextSteps

    ## Human-readable flow
    1. What changed
    2. What is risky
    3. What can be restored
    4. What to do next

    ## PDF notes
    - header with repo metadata
    - severity chips for findings
    - final checklist page
    """,
    "docs/psp_landing_page_block.md": """
    # PSP Landing Page Block

    ## Hero
    - Headline: One scan. One report. One recovery plan.
    - Subhead: Help teams restore trust and save time after repo incidents.
    - CTA: Scan your repo for $5.99

    ## Layout
    1. Hero
    2. Demo placeholder
    3. Features teaser
    4. Pricing snapshot
    5. CTA footer

    ## Accessibility
    - high contrast
    - visible focus states
    - semantic headings
    - explicit CTA copy
    """,
    "docs/psp_snapshot_workflow.md": """
    # PSP Snapshot Workflow

    ## Flow
    1. User runs `psp audit owner/repo --snapshot`
    2. CLI explains saved metadata
    3. User confirms opt-in
    4. Snapshot metadata is stored
    5. Later audits compare current state against that snapshot

    ## Retention
    Default retention is 90 days.

    ## Security
    - store minimal metadata only
    - never store raw secrets
    - expose retention policy clearly
    """,
    "docs/psp_github_app_permissions.md": """
    # PSP GitHub App Permissions

    | Scope | Permission | Level | Why |
    |---|---|---:|---|
    | Repository | Metadata | read | identify repo and installation scope |
    | Repository | Contents | read | inspect workflows and refs |
    | Repository | Actions | read | inspect workflow configuration and runs |
    | Organization | Audit log | read | optional org timeline reconstruction |

    ## CI notes
    - repo mode must work without org audit access
    - org mode must detect missing audit-log permission cleanly
    """,
    "src/psp/__init__.py": """
    __all__ = ["__version__"]
    __version__ = "0.4.0"
    """,
    "src/psp/cli/audit.py": """
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
        path.write_text(json.dumps(payload, indent=2) + "\\n")
        return path
    """,
    "src/psp/cli/report.py": """
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
            return "\\n".join([
                f"Repo: {data.get('owner')}/{data.get('repo')}",
                f"Risks: {len(data.get('Risky', []))}",
                f"Recoverable: {len(data.get('Recoverable', []))}",
            ])
        if fmt == "pdf":
            return "PDF generation placeholder"
        raise ValueError("format must be json|txt|pdf")
    """,
    "src/psp/risk/engine.py": """
    RULES = [
        "pull_request_target",
        "unsafe_shell_event_payload",
        "mutable_action_tags",
        "missing_permissions_block",
        "broad_token_write_access",
    ]

    def baseline_findings():
        return [{
            "id": "R-001",
            "description": "pull_request_target used in workflow",
            "severity": "High",
            "file": ".github/workflows/ci.yml",
            "line": 12,
            "remediation": "Use safer triggers and least-privilege permissions."
        }]
    """,
    "src/psp/landing/page.html": """
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>PSP Audit</title>
      <link rel="stylesheet" href="styles.css">
    </head>
    <body>
      <main class="wrap">
        <h1>One scan. One report. One recovery plan.</h1>
        <p>Help teams restore trust and save time after repo incidents.</p>
        <a class="cta" href="#pricing">Scan your repo for $5.99</a>
      </main>
    </body>
    </html>
    """,
    "src/psp/landing/styles.css": """
    body { margin: 0; font-family: Inter, system-ui, sans-serif; background: #0b1020; color: #eaf0ff; }
    .wrap { max-width: 960px; margin: 0 auto; padding: 64px 24px; }
    .cta { display: inline-block; padding: 12px 18px; background: #6633ee; color: white; text-decoration: none; border-radius: 10px; }
    """,
    "test/test_psp_cli.py": """
    from src.psp.cli.audit import run_audit

    def test_owner_repo_validation():
        try:
            run_audit("invalid")
            assert False
        except ValueError:
            assert True

    def test_valid_audit_payload():
        payload = run_audit("Acme/stellar")
        assert payload["schema_version"] == 1
        assert payload["owner"] == "Acme"
        assert payload["repo"] == "stellar"
    """,
    "test/test_risk_baseline.py": """
    from src.psp.risk.engine import baseline_findings

    def test_baseline_findings_present():
        findings = baseline_findings()
        assert len(findings) >= 1
        assert findings[0]["severity"] in {"High", "Medium", "Low", "Info"}
    """,
    "test/test_incident_report.py": """
    import json
    from pathlib import Path

    def test_incident_payload_shape():
        data = json.loads(Path("payloads/incident_report_example.json").read_text())
        assert data["schema_version"] == 1
        assert set(data.keys()) >= {"Changed", "Risky", "Recoverable", "NextSteps"}
    """,
    "CHANGELOG.md": """
    # Changelog

    ## v0.4.0
    - added MVP handoff package
    - added deterministic file-based report input
    - added versioned payloads
    - added minimal GitHub App permissions matrix
    """
}

json_files = {
    "payloads/audit_example.json": {
        "schema_version": 1,
        "owner": "Acme",
        "repo": "stellar",
        "refs": ["abcdef123456"],
        "tags": ["v1.0.0"],
        "workflows": [".github/workflows/ci.yml"],
        "settings_snapshot": False,
        "Risky": [{
            "id": "R-001",
            "description": "pull_request_target used in workflow",
            "severity": "High",
            "file": ".github/workflows/ci.yml",
            "line": 12,
            "remediation": "Reduce token scope and prefer safer triggers."
        }],
        "Changed": [{
            "timestamp": "2026-05-01T12:00:00Z",
            "action": "workflow_modified",
            "actor": "system"
        }],
        "Recoverable": [{
            "type": "branch",
            "name": "main",
            "status": "restorable",
            "link": "GitHub restore path"
        }],
        "NextSteps": [
            "Rotate tokens",
            "Lock sensitive branches",
            "Validate actions permissions"
        ]
    },
    "payloads/incident_report_example.json": {
        "schema_version": 1,
        "Changed": [{
            "timestamp": "2026-04-28T10:15:00Z",
            "action": "PR opened by user",
            "actor": "user"
        }],
        "Risky": [{
            "id": "R-001",
            "description": "pull_request_target usage",
            "severity": "High"
        }],
        "Recoverable": [{
            "type": "workflow",
            "name": "ci.yml",
            "status": "recoverable"
        }],
        "NextSteps": [
            "Rotate tokens",
            "Restore workflow",
            "Lock branches"
        ]
    },
    "payloads/snapshot_model.json": {
        "schema_version": 1,
        "name": "last_clean_state",
        "retention_days": 90,
        "sources": ["audit"],
        "ingest": True
    },
    "src/psp/risk/schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "psp-risk-findings",
        "type": "array",
        "items": {
            "type": "object",
            "required": ["id", "description", "severity", "file", "line", "remediation"]
        }
    },
    "src/psp/incident/schema.json": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "psp-incident-report",
        "type": "object",
        "required": ["schema_version", "Changed", "Risky", "Recoverable", "NextSteps"]
    }
}

for name, content in text_files.items():
    path = Path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip())

for name, content in json_files.items():
    path = Path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(content, indent=2) + "\\n")

print("bootstrap complete")
