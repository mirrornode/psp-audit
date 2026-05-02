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
