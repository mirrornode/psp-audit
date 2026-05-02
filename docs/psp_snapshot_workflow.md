# PSP Snapshot Workflow

## Flow
1. User runs `psp audit owner/repo --snapshot`
2. CLI explains saved metadata
3. User confirms opt-in
4. Snapshot metadata is stored
5. Later audits compare current state against that snapshot

## Retention
Default retention is 90 days.

## Security
- store minimal metadata only
- never store raw secrets
- expose retention policy clearly
