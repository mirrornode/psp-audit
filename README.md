# Repo-Snap Pistol Shrimp (psp)

One scan. One report. One recovery plan.

PSP is a GitHub repository audit tool for incident review, workflow-risk detection, and recovery planning. It helps teams understand what changed, what is risky, what may be recoverable, and what to do next.

## What it does
- Audits a repo with deterministic file-based output
- Detects risky workflow patterns
- Produces a recovery-oriented incident report
- Supports optional snapshot-based comparison against a last known clean state

## MVP scope
- `psp audit owner/repo [--snapshot]`
- `psp report audit.json --format json|txt|pdf`
- Versioned payloads with `schema_version`
- Docs, payloads, source stubs, and tests for rapid handoff

## Repository layout
- `docs/` — handoff specs and product docs
- `payloads/` — example JSON payloads
- `src/psp/` — source stubs for CLI, risk, incident, and landing
- `test/` — initial tests

## Security direction
PSP follows least-privilege GitHub Actions guidance and surfaces risky patterns such as `pull_request_target`, mutable action tags, missing `permissions:` blocks, and broad token write access.

## Next steps
- Wire a real CLI entrypoint
- Implement baseline workflow detectors
- Render text and PDF reports from `audit.json`
- Add GitHub App installation flow with minimum required permissions
