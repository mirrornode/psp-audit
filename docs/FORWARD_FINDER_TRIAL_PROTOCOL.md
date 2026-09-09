# Forward-Finder Prospective Trial Protocol

A trial counts only when a frozen prediction is demonstrably recorded before
the exact-head review against which it is scored.

Required record:

- repository and PR or bounded subject;
- full exact subject head to be reviewed;
- predictor version/commit, full input and its digest;
- proposed delta, expected outcome and any structured risk observations;
- serialized predictions and non-authorizing verdict;
- immutable record reference/digest and independently inspectable ordering
  evidence that the prediction was frozen before review.

Freeze the prediction separately from the subject to avoid a self-referential
commit SHA. If an early prediction precedes implementation, bind it to the
resulting reviewed subject through a preserved delta record before review.
Do not silently substitute a successor head for the recorded subject.

After review, bind the review reference, reviewer, date and exact reviewed SHA,
actual material codes, true positives, false positives, misses, precision and
recall. Review and prediction subject SHAs must agree for this exact-head trial.
Any unknown binding or ordering makes eligibility UNVERIFIED: exclude it from
prospective metrics. Preserve the record and its limitations. Author timestamps
or a timing label alone do not establish trustworthy ordering.

The existing self-trial is UNVERIFIED. Preserve its original claim as history;
do not backdate evidence or treat this correction as a new prospective trial.
Known findings and all tests tuned against them are retrospective regression.

Undefined precision/recall denominators yield null, excluded from averages.
Zero predictions means UNKNOWN, never CLEAR. A review is evidence within its
scope, not Operator authorization. Any head change invalidates prior review
clearance; unresolved findings persist until explicitly disposed with evidence
on the current head.
