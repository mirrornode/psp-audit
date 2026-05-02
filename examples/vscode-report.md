# PSP Incident Report: `microsoft/vscode`
_Generated: 2026-05-02 04:39 UTC_

## Summary

| Metric | Count |
|--------|-------|
| Workflows scanned | 16 |
| Total findings | 8 |
| High severity | 4 |
| Medium severity | 4 |
| Recoverable | 4 |

## High Severity Findings

### `R-002` - Shell step in job 'main' interpolates github.event payload
- **File:** `.github/workflows/no-engineering-system-changes.yml`
- **Remediation:** Pass event data via env vars, never interpolate directly into shell.

### `R-002` - Shell step in job 'main' interpolates github.event payload
- **File:** `.github/workflows/no-engineering-system-changes.yml`
- **Remediation:** Pass event data via env vars, never interpolate directly into shell.

### `R-002` - Shell step in job 'main' interpolates github.event payload
- **File:** `.github/workflows/no-engineering-system-changes.yml`
- **Remediation:** Pass event data via env vars, never interpolate directly into shell.

### `R-002` - Shell step in job 'screenshots' interpolates github.event payload
- **File:** `.github/workflows/screenshot-test.yml`
- **Remediation:** Pass event data via env vars, never interpolate directly into shell.

## Medium Severity Findings

### `R-004` - No permissions block at workflow or job level
- **Affects:** 4 workflow(s)
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

## Next Steps

1. Add permissions: read-all to all workflows.
2. Move github.event.* references into env vars before shell use.

## Recent Commits

| SHA | Author | Message |
|-----|--------|---------|
| `8309b22` | Connor Peet | agent host: eagerly create sessions when a folder is picked  |
| `96e4e9e` | Rob Lourens | agentHost: auto-approve reads of Copilot SDK tool-output tem |
| `5abf846` | Paul | Model picker changes  (#313825) |
| `b2e6267` | Rob Lourens | chat: allow text selection in tool confirmation message (#31 |
| `4a644b4` | Paul | Disable flaky test (#313832) |
| `4ca77f1` | Rob Lourens | sessions: hide "Enter to Apply" tooltip in workspace picker  |
| `4bc1682` | Rob Lourens | sessions: remember tunnel disconnects (#313800) |
| `317392e` | Rob Lourens | agent-host: restore sessions without listing catalog (#31382 |
| `f6c05d7` | Rob Lourens | agentHost: forward parent --user-data-dir to spawned host (# |
| `9b92388` | Martin Aeschlimann | UseChatSessionCustomizationsForCustomAgents setting (#313781 |

