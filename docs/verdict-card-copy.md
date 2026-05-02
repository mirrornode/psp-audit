# Verdict Card Copy

Verdict cards are the primary operator-facing output surface. Each card derives entirely from the canonical envelope. No card introduces new facts.

---

## Card: `safe`

```
┌─────────────────────────────────────────┐
│  ✓  SAFE                                │
│  {owner}/{repo}                         │
│                                         │
│  No blocking findings detected.         │
│  This repository may be handed to an    │
│  agent executor.                        │
│                                         │
│  Workflows scanned: {N}                 │
│  Findings: 0                            │
│  Audited: {timestamp}                   │
└─────────────────────────────────────────┘
```

`operator_message`: `"{repo} is safe for agent execution."`
`agent_policy.verdict`: `safe`
`agent_policy.executor_class`: `any`

---

## Card: `review`

```
┌─────────────────────────────────────────┐
│  ⚠  REVIEW REQUIRED                    │
│  {owner}/{repo}                         │
│                                         │
│  {N} medium finding(s) detected.        │
│  Human review recommended before        │
│  agent execution.                       │
│                                         │
│  Workflows scanned: {N}                 │
│  Medium findings: {N}                   │
│  Audited: {timestamp}                   │
│                                         │
│  Primary finding:                       │
│  {review_rule_ids[0]} — {description}   │
└─────────────────────────────────────────┘
```

`operator_message`: `"{repo} requires review before agent execution."`
`agent_policy.verdict`: `review`
`agent_policy.executor_class`: `restricted`

---

## Card: `blocked`

```
┌─────────────────────────────────────────┐
│  ✗  BLOCKED                            │
│  {owner}/{repo}                         │
│                                         │
│  {N} high finding(s) detected.          │
│  This repository must not be handed     │
│  to an agent executor until             │
│  remediated.                            │
│                                         │
│  Workflows scanned: {N}                 │
│  High findings: {N}                     │
│  Audited: {timestamp}                   │
│                                         │
│  Blocking finding:                      │
│  {blocking_rule_ids[0]} — {description} │
│                                         │
│  Recovery: {recoverability.steps[0]}    │
└─────────────────────────────────────────┘
```

`operator_message`: `"{repo} is blocked. {blocking_rule_ids[0] description}."`
`agent_policy.verdict`: `blocked`
`agent_policy.executor_class`: `none`

---

## Trust drift indicator

Append to any card when a baseline snapshot exists:

```
│  Trust drift: {improving ↑ | degrading ↓ | stable →}  │
│  vs. snapshot: {snapshot_date}                          │
│  New findings: {N}  |  Resolved: {N}                   │
```

---

## Copy constraints

- Verdict label is always one of: `SAFE`, `REVIEW REQUIRED`, `BLOCKED`
- `operator_message` is always derived from `agent_policy.verdict` — never written independently
- Card body never exceeds the envelope — no inferred recommendations
- Timestamp is always UTC ISO 8601
