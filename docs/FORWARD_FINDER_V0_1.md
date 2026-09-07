# Forward-Finder v0.1

## Purpose

Forward-Finder predicts likely material review findings before implementation or fresh exact-head review.

Sequence:

`AUDIT -> FORWARD-FINDER -> PISTOL SHRIMP -> IMPLEMENT -> EXACT-HEAD REVIEW`

Forward-Finder predicts. Pistol Shrimp attacks. Neither approves, merges, deploys, mutates provider state, or replaces exact-head evidence.

## Inputs

- bounded proposed delta
- expected outcome
- touched artifacts
- invariants that must remain true

## Output

- likely P1/P2/P3 review findings
- second-order consequences
- preemptive correction for each prediction
- verdict: `GO_WITH_CORRECTION` or `UNKNOWN` in v0.1

`UNKNOWN` is intentional when the deterministic rule set has no supported prediction. Absence of a prediction is never treated as clearance.

## v0.1 consequence families

1. exhaustive state/outcome consistency, including `UNKNOWN`
2. source-branch vs execution-worktree identity
3. ACTIVE work must retain a fresh evidence-producing next action
4. machine-readable routing freshness after a correction cycle
5. receipt identity must bind the operating seat
6. explicit Executor separation where execution is normative
7. preservation of predecessor/historical evidence during cleanup
8. immutable commit identity for merged subjects

## Calibration loop

For each change:

1. record Forward-Finder predictions before implementation;
2. run Pistol Shrimp/adversarial review;
3. implement the surviving bounded delta;
4. obtain fresh exact-head review;
5. map actual material findings to consequence families;
6. score prediction precision and recall;
7. add or refine a rule only when a real miss exposes a reusable invariant.

The metric is not number of warnings. The metric is material exact-head findings anticipated before implementation.

## First calibration subject: CORE-HUB PR #63

The eight unresolved P2 findings on exact head `df645e26da389c4d035f4bc5f8d69d1de5824890` are used as the initial regression corpus. The v0.1 rule families intentionally correspond to those reusable consequence classes, not to specific file names or PR numbers.

This is a calibration baseline, not a claim that the engine would have predicted the historical review before those findings were known. Future evaluations must be prospective to measure real predictive value.
