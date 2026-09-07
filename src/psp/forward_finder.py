from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable


@dataclass(frozen=True)
class Prediction:
    code: str
    severity: str
    finding: str
    rationale: str
    preemptive_correction: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ForwardFinderResult:
    expected_outcome: str
    predictions: tuple[Prediction, ...]
    verdict: str

    def to_dict(self) -> dict[str, object]:
        return {
            "expected_outcome": self.expected_outcome,
            "predictions": [item.to_dict() for item in self.predictions],
            "verdict": self.verdict,
        }


_RULES = (
    (
        "FF-UNKNOWN-CONSISTENCY",
        ("unknown", "outcome", "state"),
        "P2",
        "UNKNOWN may be permitted in one contract but omitted from another exhaustive outcome set.",
        "Cross-check every exhaustive state/outcome enumeration touched by the delta and add UNKNOWN consistently where incomplete evidence must remain epistemically unresolved.",
    ),
    (
        "FF-BRANCH-IDENTITY",
        ("branch", "worktree", "source branch"),
        "P2",
        "A single branch field may collapse source-branch identity and execution-worktree identity.",
        "Represent source branch and execution worktree branch separately whenever they can differ; make the execution field conditional rather than implicit.",
    ),
    (
        "FF-ACTIVE-NEXT-EVIDENCE",
        ("active", "next action", "rollout", "post-merge"),
        "P2",
        "An ACTIVE record may have no fresh evidence-producing next action after the current step completes.",
        "Require every ACTIVE record to name one bounded, evidence-producing next action or move it out of ACTIVE.",
    ),
    (
        "FF-ROUTING-FRESHNESS",
        ("current", "pending review", "correction", "machine-readable"),
        "P2",
        "Machine-readable routing may still describe the predecessor correction step after the successor state has advanced.",
        "After every correction commit, reconcile all current-state registers and next-action fields to the resulting tree before requesting review.",
    ),
    (
        "FF-SEAT-BINDING",
        ("seat", "reviewer", "receipt", "node"),
        "P2",
        "Evidence may identify a node/model but not the operating seat that defines its authority boundary.",
        "Bind each receipt/check-in to both identity and operating seat, and validate the seat against the current registry.",
    ),
    (
        "FF-EXECUTOR-SEPARATION",
        ("execute", "executor", "authorize", "builder"),
        "P2",
        "A role table may state separation of execution while omitting an explicit Executor seat.",
        "Make Executor an explicit seat wherever BUILD/REVIEW/AUTHORIZE/EXECUTE separation is normative.",
    ),
    (
        "FF-HISTORICAL-EVIDENCE",
        ("delete", "rewrite", "historical", "todo", "continuity"),
        "P2",
        "A cleanup may delete concrete predecessor requirements while claiming they remain retained as historical evidence.",
        "Move removed operational detail into a dated continuity artifact or preserve it under a historical heading before simplifying the current file.",
    ),
    (
        "FF-IMMUTABLE-SUBJECT",
        ("merged", "pull request", "pr #", "exact head", "commit"),
        "P2",
        "Merged work may be referenced only by PR number even though the system requires immutable subject identity.",
        "Bind merged subjects to source-head or merge SHA in every current-work record that depends on them.",
    ),
)


def _normalize(parts: Iterable[str]) -> str:
    return "\n".join(part for part in parts if part).lower()


def predict(
    *,
    proposed_delta: str,
    expected_outcome: str,
    touched_artifacts: Iterable[str] = (),
    invariants: Iterable[str] = (),
) -> ForwardFinderResult:
    """Predict likely next-review findings without mutating the subject.

    The engine is intentionally deterministic and conservative. It does not approve,
    merge, execute, or replace exact-head review. It only turns a proposed delta and
    its declared invariants into likely review objections and preemptive corrections.
    """

    corpus = _normalize((proposed_delta, expected_outcome, *touched_artifacts, *invariants))
    predictions: list[Prediction] = []

    for code, triggers, severity, finding, correction in _RULES:
        if any(trigger in corpus for trigger in triggers):
            predictions.append(
                Prediction(
                    code=code,
                    severity=severity,
                    finding=finding,
                    rationale=f"Triggered by proposed-delta vocabulary: {', '.join(t for t in triggers if t in corpus) or 'related invariant'}.",
                    preemptive_correction=correction,
                )
            )

    # A proposed change with no predicted consequence is not evidence of safety.
    verdict = "GO_WITH_CORRECTION" if predictions else "UNKNOWN"
    return ForwardFinderResult(
        expected_outcome=expected_outcome,
        predictions=tuple(predictions),
        verdict=verdict,
    )


def score_prediction(predicted_codes: Iterable[str], actual_codes: Iterable[str]) -> dict[str, float | int]:
    """Return simple calibration metrics for prediction -> exact-head review."""

    predicted = set(predicted_codes)
    actual = set(actual_codes)
    true_positive = len(predicted & actual)
    precision = true_positive / len(predicted) if predicted else 0.0
    recall = true_positive / len(actual) if actual else 1.0
    return {
        "predicted": len(predicted),
        "actual": len(actual),
        "true_positive": true_positive,
        "precision": precision,
        "recall": recall,
    }
