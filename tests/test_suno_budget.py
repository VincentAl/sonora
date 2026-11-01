"""Suno daily-credit guard uses committed logs, not AI/audio inference."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_suno_budget import check_budget, daily_spend  # noqa: E402


class SunoBudgetTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.runs = self.root / "pack" / "runs"
        self.runs.mkdir(parents=True)

    def log(self, name, stamp, spent, before=100, after=None):
        if after is None:
            after = before - spent
        path = self.runs / f"{name}.json"
        path.write_text(json.dumps({
            "run_id": name, "generated_at_utc": stamp,
            "credits": {"before": before, "after": after, "spent": spent}
        }), encoding="utf-8")
        return path

    def test_actual_repo_first_generation_is_counted(self):
        self.assertEqual(20, daily_spend(ROOT / "songs/experiments", "2026-10-31"))

    def test_day_boundary_uses_paris_timezone(self):
        self.log("one", "2026-10-31T23:30:00Z", 10)  # Nov 1, 00:30 in Paris
        self.log("two", "2026-11-01T22:30:00Z", 10)  # Nov 1, 23:30 in Paris
        self.assertEqual(0, daily_spend(self.root, "2026-10-31"))
        self.assertEqual(20, daily_spend(self.root, "2026-11-01"))

    def test_limit_and_live_balance_both_enforced(self):
        self.assertEqual([], check_budget(40, 10, 80))
        self.assertTrue(any("Daily limit" in x for x in check_budget(50, 10, 80)))
        self.assertTrue(any("live Suno balance" in x for x in check_budget(0, 10, 9)))
        self.assertTrue(check_budget(0, 0, 80))

    def test_invalid_log_fails_closed(self):
        self.log("one", "2026-11-01T02:00:00Z", 10, before=100, after=99)
        with self.assertRaisesRegex(ValueError, "delta differs"):
            daily_spend(self.root, "2026-11-01")

    def test_duplicate_run_id_fails_closed(self):
        self.log("one", "2026-11-01T02:00:00Z", 10)
        other = self.log("two", "2026-11-01T03:00:00Z", 10)
        data = json.loads(other.read_text(encoding="utf-8"))
        data["run_id"] = "one"
        other.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate run_id"):
            daily_spend(self.root, "2026-11-01")

    def test_unrelated_dates_still_validate_log(self):
        self.log("one", "2026-10-31T02:00:00Z", -5)
        with self.assertRaisesRegex(ValueError, "non-negative"):
            daily_spend(self.root, "2026-11-01")


if __name__ == "__main__":
    unittest.main()
