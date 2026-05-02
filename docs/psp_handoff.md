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
