"""Deterministic journal checks; run: python3 -m unittest discover -s tests."""
import copy
import importlib.util
import unittest
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "scripts/validate_weekly_feedback.py"
spec = importlib.util.spec_from_file_location("weekly_feedback_validator", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def sample():
    return {"version": 1, "entries": [{
        "clip_id": "clip-1", "generated_at_utc": "2026-11-02T12:00:00Z",
        "song": "Test", "mechanism": "M01", "targets": ["añorar"],
        "selection": "pending", "human_feedback": None,
        "audio_approved": False, "pedagogy_approved": False,
        "playlist_state": "not_added",
    }]}


class WeeklyFeedbackTests(unittest.TestCase):
    def test_empty_and_pending(self):
        module.validate({"version": 1, "entries": []})
        module.validate(sample())

    def test_like_needs_human_feedback(self):
        x = sample()
        x["entries"][0]["selection"] = "liked"
        with self.assertRaises(ValueError):
            module.validate(x)

    def test_playlist_needs_both_approvals(self):
        x = sample()
        entry = x["entries"][0]
        entry["selection"] = "kept"
        entry["human_feedback"] = {
            "quote": "Je garde celle-ci", "source": "conversation Sonora",
            "at_utc": "2026-11-02T12:00:00Z"
        }
        entry["playlist_state"] = "added"
        with self.assertRaises(ValueError):
            module.validate(x)
        entry["audio_approved"] = True
        entry["pedagogy_approved"] = True
        module.validate(x)

    def test_duplicate_clip_and_bad_date(self):
        x = sample()
        x["entries"].append(copy.deepcopy(x["entries"][0]))
        with self.assertRaises(ValueError):
            module.validate(x)
        x["entries"].pop()
        x["entries"][0]["generated_at_utc"] = "2026-11-02"
        with self.assertRaises(ValueError):
            module.validate(x)


if __name__ == "__main__":
    unittest.main()
