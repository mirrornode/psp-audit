import unittest

from psp.forward_finder import predict, score_prediction


PR63_ACTUAL = {
    "FF-UNKNOWN-CONSISTENCY",
    "FF-BRANCH-IDENTITY",
    "FF-ACTIVE-NEXT-EVIDENCE",
    "FF-ROUTING-FRESHNESS",
    "FF-SEAT-BINDING",
    "FF-EXECUTOR-SEPARATION",
    "FF-HISTORICAL-EVIDENCE",
    "FF-IMMUTABLE-SUBJECT",
}


class ForwardFinderTests(unittest.TestCase):
    def test_pr63_calibration_recovers_all_material_categories(self):
        result = predict(
            proposed_delta="""
            Reconcile current machine-readable workstreams after a correction cycle and pending review.
            Permit UNKNOWN state/outcome handling. Separate source branch from execution worktree branch.
            Keep post-merge ACTIVE rollout work with a next action. Bind node review receipt to seat.
            Preserve BUILD/REVIEW/AUTHORIZE/EXECUTE separation including Executor.
            Rewrite historical TODO continuity without deleting predecessor evidence.
            Record merged pull request subjects with exact head or commit identity.
            """,
            expected_outcome="Fresh exact-head review with no unresolved material findings.",
            touched_artifacts=(
                "NODE_CHECKIN_CONTRACT.md",
                "MIRRORNODE_ENGINEERING_DOCTRINE_V1.md",
                "workstreams.v1.json",
                "AGENTS_TODO.md",
            ),
        )
        predicted = {item.code for item in result.predictions}
        score = score_prediction(predicted, PR63_ACTUAL)

        self.assertEqual(predicted, PR63_ACTUAL)
        self.assertEqual(score["recall"], 1.0)
        self.assertEqual(score["precision"], 1.0)
        self.assertEqual(result.verdict, "GO_WITH_CORRECTION")

    def test_no_signal_is_unknown_not_clear(self):
        result = predict(
            proposed_delta="rename cosmetic heading",
            expected_outcome="documentation remains readable",
        )
        self.assertEqual(result.verdict, "UNKNOWN")
        self.assertEqual(result.predictions, ())


if __name__ == "__main__":
    unittest.main()
