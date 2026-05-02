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
