# PSP Incident Report: `microsoft/vscode`

**Status:** BLOCKED
**Operator message:** Stop merge-, release-, and deploy-capable agents immediately.
**Severity score:** 100 (critical)

## Summary
Repository has 8 findings requiring blocked handling.

## Trust Drift
20 trust-relevant changes detected.

## Findings
### `R-002` - Shell step in job 'main' interpolates github.event payload
- **Severity:** High
- **File:** .github/workflows/no-engineering-system-changes.yml
- **Line:** 3
- **Remediation:** Pass event data via env vars, never interpolate directly into shell.

### `R-002` - Shell step in job 'main' interpolates github.event payload
- **Severity:** High
- **File:** .github/workflows/no-engineering-system-changes.yml
- **Line:** 4
- **Remediation:** Pass event data via env vars, never interpolate directly into shell.

### `R-002` - Shell step in job 'main' interpolates github.event payload
- **Severity:** High
- **File:** .github/workflows/no-engineering-system-changes.yml
- **Line:** 8
- **Remediation:** Pass event data via env vars, never interpolate directly into shell.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/pr-darwin-test.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/pr-linux-cli-test.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/pr-linux-test.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/pr-win32-test.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-002` - Shell step in job 'screenshots' interpolates github.event payload
- **Severity:** High
- **File:** .github/workflows/screenshot-test.yml
- **Line:** 16
- **Remediation:** Pass event data via env vars, never interpolate directly into shell.

## Recoverability
4 recoverable items identified.

## Agent Policy
### coding_agent
- Allowed: read
- Blocked: merge, push, workflow_dispatch

### deploy_agent
- Allowed: read
- Blocked: deploy, release, workflow_dispatch

### release_bot
- Allowed: read
- Blocked: tag, release, publish

### comment_bot
- Allowed: read, issue_comment
- Blocked: none

## Next Steps
1. Add permissions: read-all to all workflows.
2. Move github.event.* references into env vars before shell use.
