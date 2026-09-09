import json
from pathlib import Path
import unittest

from psp.forward_finder import RiskObservation, predict, score_prediction

ROOT = Path(__file__).resolve().parents[1]
CODES = json.loads((ROOT / 'examples/pr63_actual_codes.json').read_text())


def run(*observations, **kwargs):
    return predict(proposed_delta=kwargs.pop('proposed_delta', ''),
                   expected_outcome=kwargs.pop('expected_outcome', ''),
                   observations=observations, **kwargs)


class ForwardFinderTests(unittest.TestCase):
    def test_risk_mitigation_unknown_pairs_for_all_families(self):
        for code in CODES:
            with self.subTest(code=code):
                for risk, mitigation, expected in [(True, False, 'PREDICTIONS_PRESENT'),
                        (True, True, 'UNKNOWN'), (True, None, 'UNKNOWN'),
                        (False, False, 'UNKNOWN'), (None, False, 'UNKNOWN')]:
                    result = run(RiskObservation(code, 'bounded subject', 'fixture:assessment', risk, mitigation))
                    self.assertEqual(result.verdict, expected)
                    self.assertEqual(len(result.predictions), int(expected == 'PREDICTIONS_PRESENT'))

    def test_free_text_does_not_establish_defects(self):
        for delta in ['Separate source branch from execution worktree branch',
                      'Do not delete predecessor TODO evidence', 'execution branch',
                      'Delete predecessor TODO evidence',
                      (ROOT / 'examples/pr63_forward_finder_trial_input.txt').read_text()]:
            with self.subTest(delta=delta):
                self.assertEqual(run(proposed_delta=delta).verdict, 'UNKNOWN')

    def test_context_cannot_supply_risk(self):
        self.assertEqual(run(proposed_delta='branch', expected_outcome='execution worktree',
                         invariants='Preserve predecessor evidence',
                         touched_artifacts='execution worktree').predictions, ())
        self.assertEqual(run(touched_artifacts='execution worktree', invariants='branch'),
                         run(touched_artifacts=('execution worktree',), invariants=('branch',)))

    def test_conflicts_abstain_per_subject(self):
        code = CODES[0]
        a = RiskObservation(code, 'A', 'fixture:a', True, False)
        b = RiskObservation(code, 'A', 'fixture:b', True, True)
        self.assertEqual(run(a, b).verdict, 'UNKNOWN')
        c = RiskObservation(code, 'B', 'fixture:c', True, False)
        self.assertEqual(len(run(a, b, c).predictions), 1)
        self.assertIn('on B;', run(a, b, c).predictions[0].rationale)

    def test_observation_validation(self):
        for observation in [RiskObservation('bad', 'A', 'ref', True, False),
                            RiskObservation(CODES[0], '', 'ref', True, False),
                            RiskObservation(CODES[0], 'A', '', True, False)]:
            with self.assertRaises(ValueError):
                run(observation)
        with self.assertRaises(TypeError):
            run(RiskObservation(CODES[0], 'A', 'ref', 1, False))

    def test_score_denominators(self):
        for predicted, actual, precision, recall in [([], [], None, None),
                (['A'], [], 0.0, None), ([], ['A'], None, 0.0),
                (['A', 'B'], ['A', 'C'], 0.5, 0.5)]:
            score = score_prediction(predicted, actual)
            self.assertEqual(score['precision'], precision)
            self.assertEqual(score['recall'], recall)
            self.assertEqual(score['misses'], len(set(actual) - set(predicted)))
            self.assertEqual(score['false_positive'], len(set(predicted) - set(actual)))
        self.assertEqual(score_prediction('ABC', 'ABC')['true_positive'], 1)

    def test_public_serialization_fixture(self):
        delta = (ROOT / 'examples/pr63_forward_finder_trial_input.txt').read_text()
        expected = json.loads((ROOT / 'examples/forward_finder_expected_output.json').read_text())
        self.assertEqual(run(proposed_delta=delta, expected_outcome=expected['expected_outcome']).to_dict(), expected)
        risk = run(RiskObservation(CODES[0], 'A', 'fixture:a', True, False)).to_dict()
        self.assertEqual(set(risk), {'expected_outcome', 'predictions', 'verdict'})
        self.assertEqual(risk['predictions'][0]['code'], CODES[0])

    def test_historical_trial_excluded(self):
        trial = json.loads((ROOT / 'examples/forward_finder_self_trial.json').read_text())
        self.assertFalse(trial['eligible_for_prospective_metrics'])
        self.assertEqual(trial['provenance_status'], 'UNVERIFIED')
        self.assertEqual(trial['forward_finder_verdict'], 'UNKNOWN')
