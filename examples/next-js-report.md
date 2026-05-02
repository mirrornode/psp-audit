# PSP Incident Report: `vercel/next.js`
_Generated: 2026-05-02 01:55 UTC_

## Summary

| Metric | Count |
|--------|-------|
| Workflows scanned | 37 |
| Total findings | 35 |
| High severity | 6 |
| Medium severity | 29 |
| Recoverable | 29 |

## High Severity Findings

### `R-002` - Shell step in job 'deploy-target' interpolates github.event payload
- **File:** `.github/workflows/build_and_deploy.yml`
- **Remediation:** Pass event data via env vars, never interpolate directly into shell.

### `R-002` - Shell step in job 'deploy-tarball' interpolates github.event payload
- **File:** `.github/workflows/build_and_deploy.yml`
- **Remediation:** Pass event data via env vars, never interpolate directly into shell.

### `R-001` - Workflow uses pull_request_target trigger
- **File:** `.github/workflows/pull_request_auto_label.yml`
- **Remediation:** Replace with pull_request or scope permissions tightly and never checkout untrusted code.

### `R-002` - Shell step in job 'retry-on-failure' interpolates github.event payload
- **File:** `.github/workflows/retry_deploy_test.yml`
- **Remediation:** Pass event data via env vars, never interpolate directly into shell.

### `R-002` - Shell step in job 'retry-on-failure' interpolates github.event payload
- **File:** `.github/workflows/retry_test.yml`
- **Remediation:** Pass event data via env vars, never interpolate directly into shell.

### `R-002` - Shell step in job 'upload' interpolates github.event payload
- **File:** `.github/workflows/upload_preview_tarballs.yml`
- **Remediation:** Pass event data via env vars, never interpolate directly into shell.

## Medium Severity Findings

### `R-004` - No permissions block at workflow or job level
- **Affects:** 28 workflow(s)
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-003` - Mutable action ref 'vercel/next.js/.github/actions/pr-auto-label@canary' in job 'label'
- **Affects:** 1 workflow(s)
- **Remediation:** Pin to full commit SHA: vercel/next.js/.github/actions/pr-auto-label@<sha>

## Next Steps

1. Review pull_request_target workflows immediately — high pwn risk.
2. Pin all action refs to full commit SHAs.
3. Add permissions: read-all to all workflows.
4. Move github.event.* references into env vars before shell use.

## Recent Commits

| SHA | Author | Message |
|-----|--------|---------|
| `908717a` | Matt Mastracci | Drop once_cell from all direct crate deps (#93095) |
| `008e2e4` | next-js-bot[bot] | v16.3.0-canary.8 |
| `aacf6e1` | Sam Selikoff | Fix streaming in draft mode for cache components (#93417) |
| `66776bd` | Luke Sandberg | [turbo-trace-server] optimize loading even more (#93332) |
| `65340b2` | Tim Neutkens | feat(metadata): support non-standard directives in robots.ts |
| `b2491e3` | Tim Neutkens | Revert "Revert "Node.js streams: Add forkpoint for prerender |
| `9a4e4e7` | Tobias Koppers | trace-server: shrink_to_fit LazySortedVec after sorting (#93 |
| `ca7b3a1` | next-js-bot[bot] | v16.3.0-canary.7 |
| `d72a035` | Zack Tanner | [ci]: remove PR creation from deploy test workflow (#93400) |
| `f476c5f` | Tim Neutkens | Remove leftover Turbopack manifests (#93398) |

