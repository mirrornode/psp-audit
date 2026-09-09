# PSP Repository Map

Repository: `mirrornode/psp-audit`

## Scope and contract relationship

This repository contains the Repo-Snap Pistol Shrimp Python inspection and
reporting tools. `SYSTEM_CONTRACT.md` carries the shared MIRRORNODE system
contract, attributed there to `mirrornode/MIRRORNODE-CORE-HUB`. Its agent
registry and runtime paths describe the wider system; they are not evidence
that those runtimes are implemented or deployed in this repository.

This map follows the contract's requirement that documentation reflect real
code paths. It does not change the shared registry, command routing, or
authority. `AGENTS_TODO.md` retains the shared agent priorities.

## Implementation paths

| Path | Repository responsibility |
| --- | --- |
| `pyproject.toml` | Python packaging and the `psp = psp.cli:main` entry point |
| `src/psp/cli/__init__.py` | CLI commands for audit, report, and rate-limit inspection |
| `src/psp/cli/audit.py` | Repository audit collection and output persistence |
| `src/psp/github_client.py` | GitHub API client |
| `src/psp/risk/` | Risk engine and schema |
| `src/psp/judgment/` | Judgment-envelope construction |
| `src/psp/cli/report.py`, `src/psp/renderers/` | Report rendering |
| `src/psp/incident/` | Incident schema |
| `src/psp/landing/` | Landing-page assets |
| `src/psp/forward_finder.py` | Proposed Forward-Finder prediction and calibration logic |
| `test/`, `tests/` | Existing tests, including Forward-Finder tests |
| `docs/` | Contracts, design notes, handoff material, and trial protocol |
| `examples/`, `payloads/`, `exports/`, `audit.json` | Stored examples and evidence outputs; not live attestations |

## Repository validation

`.github/workflows/canon-gate.yml` runs `scripts/canon_gate.py` for pull
requests targeting `main`. The gate checks the incoming diff and requires
`SYSTEM_CONTRACT.md`, `REPO_MAP.md`, and `AGENTS_TODO.md` to be present.
Passing that check is limited validation evidence, not independent review,
deployment approval, or permission to execute consequential actions.

Forward-Finder remains a proposal under review in PR #1. Mapping its source
does not resolve its review findings or establish predictive accuracy.
