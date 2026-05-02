# PSP Incident Report: `vercel/next.js`

**Status:** BLOCKED
**Operator message:** Stop merge-, release-, and deploy-capable agents immediately.
**Severity score:** 100 (critical)

## Summary
Repository has 35 findings requiring blocked handling.

## Trust Drift
20 trust-relevant changes detected.

## Findings
### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/build_and_deploy.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-002` - Shell step in job 'deploy-target' interpolates github.event payload
- **Severity:** High
- **File:** .github/workflows/build_and_deploy.yml
- **Line:** 2
- **Remediation:** Pass event data via env vars, never interpolate directly into shell.

### `R-002` - Shell step in job 'deploy-tarball' interpolates github.event payload
- **Severity:** High
- **File:** .github/workflows/build_and_deploy.yml
- **Line:** 7
- **Remediation:** Pass event data via env vars, never interpolate directly into shell.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/build_and_test.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/build_reusable.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/code_freeze.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/create_release_branch.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/graphite_ci_optimizer.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/integration_tests_reusable.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/issue_stale.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/issue_wrong_template.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/popular.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-001` - Workflow uses pull_request_target trigger
- **Severity:** High
- **File:** .github/workflows/pull_request_auto_label.yml
- **Line:** 1
- **Remediation:** Replace with pull_request or scope permissions tightly and never checkout untrusted code.

### `R-003` - Mutable action ref 'vercel/next.js/.github/actions/pr-auto-label@canary' in job 'label'
- **Severity:** Medium
- **File:** .github/workflows/pull_request_auto_label.yml
- **Line:** 1
- **Remediation:** Pin to full commit SHA: vercel/next.js/.github/actions/pr-auto-label@<sha>

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/pull_request_stats.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/release-next-rspack.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-002` - Shell step in job 'retry-on-failure' interpolates github.event payload
- **Severity:** High
- **File:** .github/workflows/retry_deploy_test.yml
- **Line:** 1
- **Remediation:** Pass event data via env vars, never interpolate directly into shell.

### `R-002` - Shell step in job 'retry-on-failure' interpolates github.event payload
- **Severity:** High
- **File:** .github/workflows/retry_test.yml
- **Line:** 2
- **Remediation:** Pass event data via env vars, never interpolate directly into shell.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/rspack-nextjs-build-integration-tests.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/rspack-nextjs-dev-integration-tests.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/rspack-update-tests-manifest.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/setup-nextjs-build.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/sync_backport_canary_release.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/test-turbopack-rust-bench-test.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/test_e2e_deploy_release.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/test_e2e_project_reset_cron.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/test_examples.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/trigger_release.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/turbopack-nextjs-build-integration-tests.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/turbopack-nextjs-dev-integration-tests.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/turbopack-update-tests-manifest.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/update_fonts_data.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/update_react.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-004` - No permissions block at workflow or job level
- **Severity:** Medium
- **File:** .github/workflows/upload-tests-manifest.yml
- **Line:** 1
- **Remediation:** Add permissions: read-all at workflow level, override per job as needed.

### `R-002` - Shell step in job 'upload' interpolates github.event payload
- **Severity:** High
- **File:** .github/workflows/upload_preview_tarballs.yml
- **Line:** 8
- **Remediation:** Pass event data via env vars, never interpolate directly into shell.

## Recoverability
29 recoverable items identified.

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
1. Pass event data via env vars, never interpolate directly into shell.
2. Replace with pull_request or scope permissions tightly and never checkout untrusted code.
3. Add permissions: read-all at workflow level, override per job as needed.
4. Pin to full commit SHA: vercel/next.js/.github/actions/pr-auto-label@<sha>
