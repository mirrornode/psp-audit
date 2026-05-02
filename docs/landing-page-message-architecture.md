# Landing Page Message Architecture

## Core message hierarchy

Every surface — landing page, CLI output, report header, verdict card — derives from a single message spine. Nothing on any surface contradicts or extends beyond this spine.

---

### Level 1: The lead question (always present)

> Can this repository be treated as safe for agent execution right now?

This question appears above the fold on the landing page, as the first line of every report, and as the framing device in all operator-facing copy. It is never paraphrased. It is never replaced with a softer question.

---

### Level 2: The trust boundary statement (always present)

> PSP is the trust boundary for GitHub-native agents.

This is the product identity sentence. It appears in the hero, in the README, in the founder brief, and in any external positioning. It is not a tagline. It is a technical description.

---

### Level 3: The verdict (per audit)

One of three states, always explicit:

| Verdict | Operator message pattern |
|---------|--------------------------|
| `safe` | "{repo} is safe for agent execution." |
| `review` | "{repo} requires review before agent execution." |
| `blocked` | "{repo} is blocked. {Primary blocking finding}." |

---

### Level 4: The recovery path (per audit, when not safe)

> {N} finding(s) must be resolved. Estimated {M} workflow file(s) require changes.

Followed by the ordered `recoverability.steps` list.

---

## Landing page sections

### Hero
- Headline: `PSP — the trust boundary for GitHub-native agents`
- Subhead: `Can this repository be treated as safe for agent execution right now?`
- CTA: `Run your first audit` → installs PSP or opens hosted scan

### How it works
1. PSP scans your workflow files, refs, and settings
2. PSP emits a canonical trust verdict: `safe`, `review`, or `blocked`
3. PSP generates a recovery plan if your repository is not safe
4. Every automated executor downstream inherits that verdict

### What PSP catches
- `pull_request_target` triggers without scoped permissions
- Shell steps interpolating `github.event.*` payload directly
- Mutable action refs (`@main`, `@canary`, `@latest`)
- Missing `permissions:` blocks at workflow or job level
- Broad `GITHUB_TOKEN` write access

### Trust drift
> PSP tracks how your repository's trust posture changes over time.

Compare any audit against a previous snapshot. Know immediately whether your posture is improving, degrading, or stable.

### For agent builders
> Every GitHub-native agent inherits the trust posture of the repository it executes in. PSP makes that posture legible before execution — not after incident.

`agent_policy` field is machine-readable. Wire it directly into your agent's execution gate.

---

## Copy constraints

- Never use "vulnerability" to describe PSP findings. Use "trust posture risk" or "workflow finding."
- Never claim PSP replaces a security audit. PSP answers one specific question about one specific trust boundary.
- Never introduce findings on the landing page that are not derivable from the canonical envelope.
- The `operator_message` field is the only text that may be surfaced verbatim as a verdict.
