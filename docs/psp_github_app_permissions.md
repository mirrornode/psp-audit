# PSP GitHub App Permissions

| Scope | Permission | Level | Why |
|---|---|---:|---|
| Repository | Metadata | read | identify repo and installation scope |
| Repository | Contents | read | inspect workflows and refs |
| Repository | Actions | read | inspect workflow configuration and runs |
| Organization | Audit log | read | optional org timeline reconstruction |

## CI notes
- repo mode must work without org audit access
- org mode must detect missing audit-log permission cleanly
