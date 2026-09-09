# PR #1 bounded correction disposition

Starting head: `fbc9cd8dc36d2f7ddd584136b241eabb9b213434`.
Posted review: `04a8f6569ea6603f57a0f3f605137ea3f68a6bb8`.
The sole intervening change added REPO_MAP.md. No predictor correction was lost.
This document accompanies a proposed correction, not independent review clearance.

| Finding | Correction |
| --- | --- |
| Substring false confidence | Withdraw text inference. Require explicit subject-bound risk/mitigation observations. Ambiguous, mitigated and conflicting records abstain. |
| Undefined recall | Null for no positives; precision also null for no predictions. Counts, false positives and misses remain visible. |
| Unverified prospective provenance | Preserve original timing assertion as history; explicitly exclude self-trial from prospective metrics. Define future freeze and subject-binding requirements. |
| Serializer mismatch | Generate the fixture from to_dict and assert exact equality. |
| Authorization-like predictor verdict | PREDICTIONS_PRESENT or UNKNOWN only. |
| Iterable string inconsistency | Normalize context and scoring strings as single values; validate types. |
| Canon Gate unavailable diff passes | Fail on unavailable git evidence; check governance files even with valid empty diff. |
| Canon Gate identity and authority claims | Checkout requested PR head explicitly, verify HEAD identity, report scoped check success without authorizing merge. |

Validation: eight Forward-Finder test methods (including all eight family pairs)
and five Canon Gate integration test methods pass locally. Canon Gate tests use
actual temporary git repositories for invalid refs, mismatched checkout, empty
diffs and missing governance files. Workflow runs both bounded suites.

Residual limits: observations are supplied assessments, not independently
verified facts; text inference is withdrawn. Tests are retrospective regression.
Canon Gate still checks only its enumerated contract constraints. It does not
inspect review clearance, change protection policy, or grant authority.

Next disposition requires independent review bound to the resulting full commit
SHA. Use REQUIRES_REVISION or NO_MATERIAL_FINDINGS_WITHIN_REVIEW_SCOPE, with
reviewer, date, scope and evidence references. Any changed SHA makes prior
clearance stale; unresolved findings do not disappear when the head changes.
Operator authorization remains separate. No merge or deployment is claimed.
