# Repo-Snap Pistol Shrimp (PSP)

**PSP is the trust boundary for GitHub-native agents.**

One scan. One report. One recovery plan.

## The lead question

> Can this repository be treated as safe for agent execution right now?

PSP answers that question deterministically — from repo state alone, without org audit logs or external enrichment — and emits a canonical envelope that every downstream surface (CLI, dashboard, API, agent policy) derives from without adding new facts.

## What it does

- Audits a repository with deterministic, file-based output
- Detects risky workflow patterns (injection, privilege escalation, mutable refs)
- Emits a canonical envelope with `operator_message`, `trust_drift`, `agent_policy`, and `recoverability`
- Produces a recovery-oriented incident report in `txt`, `md`, or `json`
- Supports optional snapshot-based comparison against a last known clean state

## MVP scope

- `psp audit owner/repo [--snapshot]`
- `psp report audit.json --format json|txt|md`
- `psp rate-limit`
- Versioned payloads with `schema_version`

## Repository layout

- `docs/` — architecture, permissions, product, and handoff specs
- `payloads/` — example canonical envelopes
- `src/psp/` — CLI, GitHub client, risk engine, report renderer
- `test/` — unit and integration tests

## Installation

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
export GITHUB_TOKEN=your_token
psp audit owner/repo
```

## Security posture

PSP requests only the minimum permissions needed to inspect repository trust posture and workflow state. See `docs/github-app-permissions.md` for the full permission model.

## Next steps

- Wire deterministic judgment spine (`safe` / `review` / `blocked`)
- Implement `trust_drift` scoring
- GitHub App installation flow
- Render verdict cards for operator-facing surfaces
