# PSP Founder Brief

## The problem

GitHub Actions is the dominant CI/CD substrate for open source and enterprise software. It is also the most exploited attack surface in modern software supply chains. Workflow files are code — they run on push, on pull request, on schedule — and most teams have no systematic way to know whether their workflow posture is safe before an agent, a bot, or an attacker exercises it.

The result: repositories with `pull_request_target` triggers, unscoped `GITHUB_TOKEN` write access, and shell steps interpolating untrusted event payloads sit in production, quietly exploitable, for months or years.

## The insight

The information needed to answer "is this repository safe for agent execution?" already exists in the repository. It does not require audit logs, runtime telemetry, or org-level access. It requires a deterministic reading of the workflow files, ref state, and settings snapshot — and a judgment engine that maps that reading to a canonical trust verdict.

PSP is that judgment engine.

## The lead question

> Can this repository be treated as safe for agent execution right now?

Every PSP output — CLI table, incident report, verdict card, agent policy signal — is a derived answer to this question. Nothing on any output surface introduces facts that are not in the canonical envelope.

## The canonical envelope

PSP emits one envelope per audit. All surfaces derive from it.

| Field | Purpose |
|-------|---------|
| `operator_message` | Human-readable verdict for the repository owner |
| `trust_drift` | Delta between current state and last known clean snapshot |
| `agent_policy` | Machine-readable policy signal for automated consumers |
| `recoverability` | Prioritized remediation path back to `safe` |

## Trust boundary framing

PSP does not scan for vulnerabilities in application code. PSP scans for conditions that make a repository unsafe as an execution substrate — for an agent, a bot, a GitHub App, or a CI pipeline acting on behalf of a human or organization.

The trust boundary is: **can the repository be handed to an automated executor without that executor becoming a vector for privilege escalation, secret exfiltration, or supply chain compromise?**

## Judgment states

| State | Meaning |
|-------|---------|
| `safe` | No blocking findings. Repository may be handed to an agent executor. |
| `review` | Medium findings present. Human review recommended before agent execution. |
| `blocked` | High findings present. Repository must not be handed to an agent executor until remediated. |

## The market moment

The rise of GitHub-native agents — Copilot Workspace, Devin, Claude Code, custom automation — means that repository trust posture is no longer a static security concern. It is a live operational constraint. Every agent that acts on a repository inherits its trust posture. PSP makes that posture legible before execution, not after incident.

## The team

PSP was designed and built by a solo founder working with a distributed team of specialized AI collaborators, using GitHub's own public API against its own infrastructure. The findings in this report are real, derived from live repositories, and reproducible by anyone with a GitHub token and a terminal.
