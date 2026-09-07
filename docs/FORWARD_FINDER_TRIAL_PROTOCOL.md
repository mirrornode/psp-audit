# Forward-Finder Prospective Trial Protocol

A trial counts only when its prediction is recorded before the exact-head review it will be scored against.

Required fields:

- repository
- pull request or bounded subject
- exact proposed head when available
- proposed delta
- expected outcome
- predicted material finding codes
- Forward-Finder verdict
- timestamp/order evidence showing prediction preceded review

After review, record:

- exact reviewed head
- actual material finding codes
- true positives
- false positives
- misses
- precision and recall

Do not tune a rule against the same review and then count that review as prospective evidence. Retrospective calibration and prospective performance must remain separate.
