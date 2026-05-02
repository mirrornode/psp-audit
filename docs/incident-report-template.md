# PSP Incident Report Template

This template defines the canonical structure of a PSP incident report. All rendered surfaces (txt, md, json, verdict card) derive from this structure. No surface adds facts not present in the canonical envelope.

---

## Envelope fields

### `operator_message`
A single human-readable sentence stating the current trust verdict and the highest-priority action required.

Format: `"{repo} is {safe|under review|blocked}. {Primary action or confirmation}."`

Examples:
- `"vercel/next.js is blocked. Remediate pull_request_target trigger in pull_request_auto_label.yml before enabling agent execution."`
- `"torvalds/linux is safe. No workflow findings detected. Repository may be handed to an agent executor."`

---

### `trust_drift`
The delta between the current audit state and the last known clean snapshot, if one exists.

Fields:
- `snapshot_date` — ISO 8601 date of last clean snapshot
- `new_findings` — findings present now that were not present at snapshot
- `resolved_findings` — findings present at snapshot that are no longer present
- `drift_direction` — `improving` | `degrading` | `stable` | `no_baseline`

If no snapshot exists: `drift_direction: no_baseline`.

---

### `agent_policy`
Machine-readable policy signal for automated consumers.

Fields:
- `verdict` — `safe` | `review` | `blocked`
- `blocking_rule_ids` — list of finding IDs that contribute to a `blocked` verdict
- `review_rule_ids` — list of finding IDs that contribute to a `review` verdict
- `executor_class` — `any` | `restricted` | `none` (what class of executor may proceed)

---

### `recoverability`
Prioritized remediation path back to `safe`.

Fields:
- `steps` — ordered list of remediation actions, highest severity first
- `estimated_files` — number of workflow files requiring changes
- `blocking_count` — number of High findings to resolve before verdict can improve

---

## Report sections

```
SUMMARY
  repo, generated timestamp, schema_version
  workflow count, finding counts by severity
  trust verdict

HIGH SEVERITY FINDINGS
  per finding: id, rule, description, file, line, remediation

MEDIUM SEVERITY FINDINGS
  grouped by rule: id, description, affected workflow count, remediation

NEXT STEPS
  ordered remediation list derived from recoverability.steps

RECENT COMMITS
  last N commits: sha, author, message

ENVELOPE
  operator_message
  trust_drift
  agent_policy
  recoverability
```

---

## Derivation rule

Every field in every report section must be derivable from the canonical envelope. If a surface needs to display something that is not in the envelope, the envelope must be extended first — the surface must not introduce new facts unilaterally.
