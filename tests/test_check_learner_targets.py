"""Regression tests for the learner self-assessment target gate (no external dependencies)."""
import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_learner_targets.py"
DATA = ROOT / "data" / "learner_vocabulary_diagnostic_2026-11-03.json"
spec = importlib.util.spec_from_file_location("check_learner_targets", SCRIPT)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class LearnerTargetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))

    def test_exact_diagnostic_counts_and_no_overlap(self):
        self.assertEqual(len(self.data["known"]), 30)
        self.assertEqual(len(self.data["to_learn_or_confirm"]), 30)
        self.assertEqual(
            len({gate.normalize(x) for x in self.data["known"] + self.data["to_learn_or_confirm"]}),
            60,
        )

    def test_known_expression_is_excluded_as_new_target(self):
        result = gate.classify(self.data, ["atreverse a", "pasar página"])
        self.assertTrue(all(x["state"] == "known" for x in result))
        self.assertTrue(all(not x["eligible_as_new_target"] for x in result))

    def test_unchecked_is_candidate_not_confirmed_unknown(self):
        result = gate.classify(self.data, ["echar en cara", "dar marcha atrás"])
        self.assertEqual([x["state"] for x in result], ["to_learn_or_confirm"] * 2)
        self.assertTrue(all(x["eligible_as_new_target"] for x in result))

    def test_unassessed_is_not_assumed_unknown(self):
        result = gate.classify(self.data, ["expresión no evaluada"])
        self.assertEqual(result[0]["state"], "unassessed")
        self.assertFalse(result[0]["eligible_as_new_target"])

    def test_normalization_is_case_and_whitespace_tolerant(self):
        self.assertEqual(gate.classify(self.data, ["  ECHAR   EN CARA  "])[0]["state"], "to_learn_or_confirm")

    def test_overlap_is_rejected(self):
        bad = {"known": ["dar marcha atrás"], "to_learn_or_confirm": ["DAR MARCHA ATRÁS"]}
        with self.assertRaises(ValueError):
            gate.classify(bad, ["dar marcha atrás"])


if __name__ == "__main__":
    unittest.main()
