# Forward-Finder v0.1 — bounded correction

Forward-Finder reports possible consequences of explicit, caller-supplied risk
observations. It does not approve, merge, deploy, mutate provider state, verify
observations, or replace exact-head review and Operator authorization.

## Inputs and abstention

`predict` retains proposed delta, expected outcome, touched artifacts and
invariants as context. Prose alone returns `UNKNOWN`: the old substring matcher
could not distinguish defects from corrections or independent from overlapping
signals. Its text inference is withdrawn, not advertised as repaired NLP.

An optional `RiskObservation` binds a consequence `code` to a nonblank `subject`
and `evidence_ref`, with separate `risk_present` and `mitigation_present`
assessments. The risk means the condition described by that family's finding;
the mitigation means its stated correction is already implemented. Each value
must be a boolean or `None` (unknown). The caller must assess the actual subject,
not infer an implemented mitigation from a desired outcome or an invariant.
References are traceability inputs; the predictor does not fetch or authenticate
them. This is an explicit assessment interface, not independent detection.

Only risk `True` with mitigation `False` yields a conditional prediction.
Unknown, mitigated, or conflicting records for the same code and subject
abstain. Different subjects cannot supply each other's evidence. Unsupported
families and malformed observations are rejected. No assessment establishes
clearance, including an assessment of mitigation present.

Single strings for artifacts or invariants are accepted as one item; lists and
tuples of strings are also accepted. Context never creates a prediction.

## Output

`to_dict()` emits `expected_outcome`, a `predictions` array of full objects, and
`verdict`. Verdict is `PREDICTIONS_PRESENT` when at least one supported conditional
prediction exists, otherwise `UNKNOWN`. Both states are non-authorizing.
`PREDICTIONS_PRESENT` does not imply complete coverage of the subject.

The eight consequence families and their corrections remain retrospective
review guidance: UNKNOWN consistency, branch identity, ACTIVE next evidence,
routing freshness, seat binding, Executor separation, historical evidence,
and immutable subject identity.

## Evaluation

The old PR #63 8/8 result is historical, seeded regression evidence only. The
corrected implementation abstains on its correction-language input. Paired
risk/mitigation tests exercise the structured interface; they establish neither
natural-language detection accuracy nor prospective predictive performance.

`score_prediction` counts unique consequence codes, true positives, false
positives and misses. Precision is `None`/JSON `null` without predictions; recall
is `None`/JSON `null` without actual findings. Exclude undefined metrics from
macro averages; do not impute perfect performance. Codes are scored per trial;
multiple subjects of one family do not create multiple code-level successes.
The scorer computes arithmetic only: trial provenance eligibility must be
established before including a trial in performance reporting.

Known review findings may seed regression tests, never a new prospective score
on the same review. See the trial protocol for future trials.
