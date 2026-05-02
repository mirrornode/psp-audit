# Oracle Handoff: PSP Judgment Spine

This document defines the deterministic judgment spine for PSP v0.5. Same inputs must always produce the same envelope. All derivations are from captured repo truth only.

---

## Canonical envelope schema

```json
{
  "schema_version": 2,
  "owner": "string",
  "repo": "string",
  "audited_at": "ISO 8601 UTC timestamp",
  "refs": ["branch names"],
  "tags": ["tag names"],
  "workflows": [
    {
      "name": "string",
      "path": "string",
      "findings": "integer"
    }
  ],
  "settings_snapshot": {},
  "findings": [
    {
      "id": "string (R-001 ... R-NNN)",
      "rule": "string (machine key)",
      "description": "string (human readable)",
      "severity": "High | Medium | Low",
      "file": "string",
      "line": "integer",
      "remediation": "string"
    }
  ],
  "operator_message": "string",
  "trust_drift": {
    "snapshot_date": "ISO 8601 | null",
    "new_findings": ["finding ids"],
    "resolved_findings": ["finding ids"],
    "drift_direction": "improving | degrading | stable | no_baseline"
  },
  "agent_policy": {
    "verdict": "safe | review | blocked",
    "blocking_rule_ids": ["finding ids"],
    "review_rule_ids": ["finding ids"],
    "executor_class": "any | restricted | none"
  },
  "recoverability": {
    "steps": ["ordered remediation strings"],
    "estimated_files": "integer",
    "blocking_count": "integer"
  }
}
```

---

## Judgment-state rules

Rules are evaluated in order. First match wins.

### `blocked`
Condition: one or more findings with `severity == "High"`

```
agent_policy.verdict = "blocked"
agent_policy.executor_class = "none"
agent_policy.blocking_rule_ids = [id for f in findings if f.severity == "High"]
operator_message = "{repo} is blocked. {findings[0].description}."
```

### `review`
Condition: no High findings AND one or more findings with `severity == "Medium"`

```
agent_policy.verdict = "review"
agent_policy.executor_class = "restricted"
agent_policy.review_rule_ids = [id for f in findings if f.severity == "Medium"]
operator_message = "{repo} requires review before agent execution."
```

### `safe`
Condition: no findings of any severity

```
agent_policy.verdict = "safe"
agent_policy.executor_class = "any"
agent_policy.blocking_rule_ids = []
agent_policy.review_rule_ids = []
operator_message = "{repo} is safe for agent execution."
```

---

## Stable finding catalog

| ID | Rule key | Severity | Trigger condition |
|----|----------|----------|-------------------|
| R-001 | `pull_request_target` | High | `pull_request_target` present in `on:` |
| R-002 | `unsafe_shell_event_payload` | High | `${{ github.event.` present in a `run:` step |
| R-003 | `mutable_action_tags` | Medium | `uses:` ref is not a full SHA and not a semver tag |
| R-004 | `missing_permissions_block` | Medium | No `permissions:` at workflow level and not all jobs have `permissions:` |
| R-005 | `broad_token_write_access` | High | `permissions: write-all` or `permissions.contents: write` at workflow level |

Rule IDs are stable. New rules increment from R-006. Rules are never renumbered.

---

## Deterministic scoring table

| Condition | Verdict | executor_class |
|-----------|---------|----------------|
| Any R-001 present | blocked | none |
| Any R-002 present | blocked | none |
| Any R-005 present | blocked | none |
| R-003 present, no High | review | restricted |
| R-004 present, no High | review | restricted |
| No findings | safe | any |

Multiple High findings do not compound the verdict — `blocked` is the ceiling. The `blocking_rule_ids` list surfaces all contributors.

---

## Trust drift model

Trust drift is computed only when a baseline snapshot exists.

```
new_findings = current_finding_ids - baseline_finding_ids
resolved_findings = baseline_finding_ids - current_finding_ids

if new_findings is empty and resolved_findings is empty:
    drift_direction = "stable"
elif len(resolved_findings) > len(new_findings):
    drift_direction = "improving"
elif len(new_findings) > len(resolved_findings):
    drift_direction = "degrading"
else:
    drift_direction = "stable"
```

If no baseline exists: `drift_direction = "no_baseline"`, all other fields are null.

Org audit logs are optional enrichment only. They do not affect the verdict. They may be surfaced in a future `audit_log_enrichment` field that is explicitly optional and does not feed `agent_policy`.

---

## Recoverability model

```
recoverability.steps = [
    remediation string for each unique rule in findings,
    ordered by severity (High first), then by finding count descending
]
recoverability.estimated_files = count of unique files in findings
recoverability.blocking_count = count of High findings
```

Recoverability is a guide, not a guarantee. Resolving all `blocking_count` findings is necessary to move from `blocked` to `review` or `safe`. Resolving all findings is sufficient for `safe`, but the verdict is re-derived from the next audit — PSP does not grant `safe` status without re-scanning.

---

## Actor-class agent_policy model

The `executor_class` field is designed for direct consumption by agent execution gates.

| executor_class | Meaning | Recommended gate behavior |
|----------------|---------|--------------------------|
| `any` | No restrictions | Proceed |
| `restricted` | Human review recommended | Require explicit human approval before proceeding |
| `none` | Execution must not proceed | Hard block; surface `operator_message` to operator |

Agent consumers must not derive their own verdict from the findings list. They must consume `agent_policy.verdict` and `agent_policy.executor_class` as the authoritative signal. If those fields are absent, the consumer must treat the repository as `blocked`.

---

## Policy simulation notes

- PSP does not simulate attacks. It classifies posture.
- A `safe` verdict means no known trust-boundary violations were found in the current repo state. It does not mean the repository is free of application vulnerabilities.
- A `blocked` verdict means the repository has conditions that make it unsafe as an execution substrate for an automated agent. It does not mean the repository has been compromised.
- PSP findings are reproducible. The same repo state produces the same findings on every run. If findings change between runs without a commit, that is a PSP bug.

---

**PSP judgment spine locked.**
