# GitHub App Permissions

GitHub Apps use explicit, least-privilege permissions.

## Permission mechanics

- **Default state:** GitHub Apps have no permissions by default. Selected permissions determine what the app can access through GitHub APIs and which webhooks it can subscribe to.
- **Installation permissions:** When an app is installed on a user or organization account, the installation grants the repository and organization permissions the app requested.
- **Account permissions:** If a user authorizes the app to act on their behalf, that authorization grants the app the requested account permissions for that user.
- **Permission updates:** If an app's permissions change later, the owner of each installation must approve the new permissions before they take effect for that installation; otherwise the installation continues using the old permissions.

## Git specifics

- **General Git access (HTTP):** HTTP-based Git access with an installation or user access token requires the `Contents` repository permission.
- **Workflow Git access:** If the app needs to access or edit Actions files in `.github/workflows`, it must also request the `Workflows` repository permission.

## Endpoint validation

GitHub's REST API exposes the `X-Accepted-GitHub-Permissions` response header, which identifies the permissions an endpoint requires. PSP uses this header during implementation to keep its permission matrix honest and minimal — no scope is added to the baseline install unless an endpoint explicitly requires it.

## PSP minimum permission matrix

| Permission | Type | Scope | Reason |
|------------|------|-------|--------|
| `Contents` | Repository | Read | Read workflow files and repo contents via HTTP Git |
| `Workflows` | Repository | Read | Access `.github/workflows` directory |
| `Metadata` | Repository | Read | Required by all GitHub Apps; provides repo metadata |

## PSP posture

PSP requests only the minimum permissions needed to inspect repository trust posture, workflow state, and related evidence. When PSP needs broader visibility for optional enrichment (e.g., org audit logs, branch protection rules), that scope is explained explicitly and is not included in the baseline install.

Permissions are never requested speculatively. If a capability is not in the current PSP feature set, its permission is not in the install manifest.
