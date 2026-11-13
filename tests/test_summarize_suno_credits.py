"""Regression tests for the read-only Suno credits summary."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "summarize_suno_credits.py"
spec = importlib.util.spec_from_file_location("suno_credit_summary", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SummaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def log(self, experiment, name, run_id, timestamp, spent=10, before=50, after=40):
        directory = self.root / experiment / "runs"
        directory.mkdir(parents=True, exist_ok=True)
        data = {
            "run_id": run_id,
            "generated_at_utc": timestamp,
            "credits": {"before": before, "after": after, "spent": spent},
        }
        (directory / name).write_text(json.dumps(data), encoding="utf-8")

    def test_empty_day(self):
        self.assertEqual(module.summarize(self.root, "2026-11-05")["credits_spent"], 0)

    def test_paris_midnight_and_grouping(self):
        self.log("d1", "one.json", "one", "2026-11-04T23:30:00Z")
        self.log("d1", "two.json", "two", "2026-11-05T10:00:00Z")
        self.log("d2", "three.json", "three", "2026-11-05T23:30:00Z")
        result = module.summarize(self.root, "2026-11-05")
        self.assertEqual(result["generation_calls"], 2)
        self.assertEqual(result["credits_spent"], 20)
        self.assertEqual(result["by_experiment"]["d1"], {"calls": 2, "credits": 20})

    def test_daylight_saving_transition(self):
        self.log("d1", "early.json", "early", "2026-10-24T22:30:00Z")
        self.log("d1", "late.json", "late", "2026-10-25T23:30:00Z")
        self.assertEqual(module.summarize(self.root, "2026-10-25")["generation_calls"], 1)

    def test_duplicate_id_fails_even_across_days(self):
        self.log("d1", "one.json", "same", "2026-11-04T10:00:00Z")
        self.log("d2", "two.json", "same", "2026-11-05T10:00:00Z")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            module.summarize(self.root, "2026-11-05")

    def test_bad_credit_delta_fails(self):
        self.log("d1", "bad.json", "bad", "2026-11-05T10:00:00Z", spent=10, before=50, after=45)
        with self.assertRaisesRegex(ValueError, "delta"):
            module.summarize(self.root, "2026-11-05")

    def test_naive_timestamp_fails(self):
        self.log("d1", "bad.json", "bad", "2026-11-05T10:00:00")
        with self.assertRaisesRegex(ValueError, "timestamp"):
            module.summarize(self.root, "2026-11-05")

    def test_boolean_credit_fails(self):
        self.log("d1", "bad.json", "bad", "2026-11-05T10:00:00Z", spent=True)
        with self.assertRaisesRegex(ValueError, "credits.spent"):
            module.summarize(self.root, "2026-11-05")

    def test_invalid_date_fails(self):
        with self.assertRaises(ValueError):
            module.summarize(self.root, "2026-02-30")


if __name__ == "__main__":
    unittest.main()
