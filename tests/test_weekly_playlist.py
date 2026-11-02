"""Read-only playlist reconciliation, with synthetic complete Suno snapshots."""
import copy
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_weekly_playlist import PLAYLIST_ID, reconcile

NOW = datetime(2026, 11, 2, 14, 30, tzinfo=timezone.utc)


def snapshot(*ids):
    return {
        "playlist_id": PLAYLIST_ID,
        "retrieved_at_utc": NOW.isoformat(),
        "complete": True,
        "items": [{"id": x} for x in ids],
    }


def journal(*, added=False):
    item = {
        "clip_id": "clip-1", "generated_at_utc": "2026-11-02T12:00:00Z",
        "song": "Test", "mechanism": "M01", "targets": ["añorar"],
        "selection": "pending", "human_feedback": None,
        "audio_approved": False, "pedagogy_approved": False,
        "playlist_state": "not_added",
    }
    if added:
        item.update({
            "selection": "kept", "playlist_state": "added",
            "audio_approved": True, "pedagogy_approved": True,
            "human_feedback": {"quote": "Je garde celle-ci", "source": "conversation Sonora",
                               "at_utc": "2026-11-02T12:00:00Z"},
        })
    return {"version": 1, "entries": [item]}


class PlaylistTests(unittest.TestCase):
    def test_empty_and_approved(self):
        self.assertEqual(reconcile({"version": 1, "entries": []}, snapshot(), now=NOW), 0)
        self.assertEqual(reconcile(journal(added=True), snapshot("clip-1"), now=NOW), 1)

    def test_untracked_clip(self):
        with self.assertRaisesRegex(ValueError, "untracked"):
            reconcile(journal(), snapshot("unknown"), now=NOW)

    def test_missing_and_unexpected(self):
        with self.assertRaisesRegex(ValueError, "absent"):
            reconcile(journal(added=True), snapshot(), now=NOW)
        with self.assertRaisesRegex(ValueError, "not marked added"):
            reconcile(journal(), snapshot("clip-1"), now=NOW)

    def test_incomplete_stale_wrong_playlist(self):
        x = snapshot()
        x["complete"] = False
        with self.assertRaisesRegex(ValueError, "complete"):
            reconcile(journal(), x, now=NOW)
        x = snapshot()
        x["next_cursor"] = "next"
        with self.assertRaisesRegex(ValueError, "complete"):
            reconcile(journal(), x, now=NOW)
        x = snapshot()
        x["playlist_id"] = "wrong"
        with self.assertRaisesRegex(ValueError, "playlist_id"):
            reconcile(journal(), x, now=NOW)
        x = snapshot()
        with self.assertRaisesRegex(ValueError, "stale"):
            reconcile(journal(), x, now=NOW + timedelta(hours=2))

    def test_duplicate_and_bad_ids(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            reconcile(journal(), snapshot("clip-1", "clip-1"), now=NOW)
        x = snapshot()
        x["items"] = [{"clip_id": "clip-1"}]
        with self.assertRaisesRegex(ValueError, "id"):
            reconcile(journal(), x, now=NOW)

    def test_invalid_journal_still_blocked(self):
        x = copy.deepcopy(journal())
        x["entries"][0]["selection"] = "kept"
        with self.assertRaisesRegex(ValueError, "feedback"):
            reconcile(x, snapshot(), now=NOW)


if __name__ == "__main__":
    unittest.main()
