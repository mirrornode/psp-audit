from __future__ import annotations

from dataclasses import asdict, dataclass
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


@dataclass(frozen=True)
class RiskObservation:
    """Caller-supplied assessment, not independently verified implementation evidence.

    Each observation concerns one consequence family on one bounded subject.
    risk_present means the family's risky condition is observed; mitigation_present
    means its stated correction is already implemented. None means unknown.
    evidence_ref identifies the source supporting both assessments.
    """

    code: str
    subject: str
    evidence_ref: str
    risk_present: bool | None
    mitigation_present: bool | None


# Family descriptions and corrections are retrospective guidance, not text rules.
_RULES = (
    (
        "FF-UNKNOWN-CONSISTENCY",
        "P2",
        "UNKNOWN may be permitted in one contract but omitted from another exhaustive outcome set.",
        "Cross-check every exhaustive state/outcome enumeration touched by the delta and add UNKNOWN consistently where incomplete evidence must remain epistemically unresolved.",
    ),
    (
        "FF-BRANCH-IDENTITY",
        "P2",
        "A single branch field may collapse source-branch identity and execution-worktree identity.",
        "Represent source branch and execution worktree branch separately whenever they can differ; make the execution field conditional rather than implicit.",
    ),
    (
        "FF-ACTIVE-NEXT-EVIDENCE",
        "P2",
        "An ACTIVE record may have no fresh evidence-producing next action after the current step completes.",
        "Require every ACTIVE record to name one bounded, evidence-producing next action or move it out of ACTIVE.",
    ),
    (
        "FF-ROUTING-FRESHNESS",
        "P2",
        "Machine-readable routing may still describe the predecessor correction step after the successor state has advanced.",
        "After every correction commit, reconcile all current-state registers and next-action fields to the resulting tree before requesting review.",
    ),
    (
        "FF-SEAT-BINDING",
        "P2",
        "Evidence may identify a node/model but not the operating seat that defines its authority boundary.",
        "Bind each receipt/check-in to both identity and operating seat, and validate the seat against the current registry.",
    ),
    (
        "FF-EXECUTOR-SEPARATION",
        "P2",
        "A role table may state separation of execution while omitting an explicit Executor seat.",
        "Make Executor an explicit seat wherever BUILD/REVIEW/AUTHORIZE/EXECUTE separation is normative.",
    ),
    (
        "FF-HISTORICAL-EVIDENCE",
        "P2",
        "A cleanup may delete concrete predecessor requirements while claiming they remain retained as historical evidence.",
        "Move removed operational detail into a dated continuity artifact or preserve it under a historical heading before simplifying the current file.",
    ),
    (
        "FF-IMMUTABLE-SUBJECT",
        "P2",
        "Merged work may be referenced only by PR number even though the system requires immutable subject identity.",
        "Bind merged subjects to source-head or merge SHA in every current-work record that depends on them.",
    ),
)


def _items(values: Iterable[str] | str) -> tuple[str, ...]:
    items = (values,) if isinstance(values, str) else tuple(values)
    if any(not isinstance(item, str) for item in items):
        raise TypeError("Expected strings")
    return items


def predict(
    *,
    proposed_delta: str,
    expected_outcome: str,
    touched_artifacts: Iterable[str] | str = (),
    invariants: Iterable[str] | str = (),
    observations: Iterable[RiskObservation] = (),
) -> ForwardFinderResult:
    """Evaluate explicit observations; unstructured prose alone remains UNKNOWN.

    Outcomes, invariants and artifact names provide context only. They cannot
    establish a defect. Predictions report conditional consequences of supplied
    observations; they neither verify those observations nor authorize action.
    """
    if not isinstance(proposed_delta, str) or not isinstance(expected_outcome, str):
        raise TypeError("Delta and expected outcome must be strings")
    _items(touched_artifacts)
    _items(invariants)
    families = {code: (severity, finding, correction)
                for code, severity, finding, correction in _RULES}
    grouped: dict[tuple[str, str], list[RiskObservation]] = {}
    for observation in observations:
        if not isinstance(observation, RiskObservation):
            raise TypeError("Expected RiskObservation")
        if observation.code not in families:
            raise ValueError("Unknown consequence family")
        if (not isinstance(observation.subject, str) or not observation.subject.strip()
                or not isinstance(observation.evidence_ref, str)
                or not observation.evidence_ref.strip()):
            raise ValueError("Observation requires subject and evidence reference")
        for value in (observation.risk_present, observation.mitigation_present):
            if value is not None and type(value) is not bool:
                raise TypeError("Observation assessments must be bool or None")
        grouped.setdefault((observation.code, observation.subject.strip()), []).append(observation)

    predictions: list[Prediction] = []
    for (code, subject), records in sorted(grouped.items()):
        # Unknown, mitigated or conflicting assessments for a subject abstain.
        if not all(r.risk_present is True and r.mitigation_present is False
                   for r in records):
            continue
        severity, finding, correction = families[code]
        references = ", ".join(sorted({r.evidence_ref.strip() for r in records}))
        predictions.append(Prediction(
            code=code, severity=severity, finding=finding,
            rationale=(f"Caller-reported risk on {subject}; mitigation reported absent. "
                       f"Evidence references (not verified by predictor): {references}."),
            preemptive_correction=correction,
        ))
    return ForwardFinderResult(
        expected_outcome=expected_outcome,
        predictions=tuple(predictions),
        verdict="PREDICTIONS_PRESENT" if predictions else "UNKNOWN",
    )


def score_prediction(predicted_codes: Iterable[str], actual_codes: Iterable[str]) -> dict[str, float | int | None]:
    """Return calibration metrics for prediction -> exact-head review."""

    predicted = set(_items(predicted_codes))
    actual = set(_items(actual_codes))
    true_positive = len(predicted & actual)
    precision = true_positive / len(predicted) if predicted else None
    recall = true_positive / len(actual) if actual else None
    return {
        "predicted": len(predicted),
        "actual": len(actual),
        "true_positive": true_positive,
        "false_positive": len(predicted - actual),
        "misses": len(actual - predicted),
        "precision": precision,
        "recall": recall,
    }
