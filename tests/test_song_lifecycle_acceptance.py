"""Lifecycle acceptance checks: two clips, independent decisions, playlist drift.

No Suno calls, human feedback fabrication, or state changes. Run via unittest discovery.
"""
from __future__ import annotations

import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_weekly_feedback import validate
from check_weekly_playlist import PLAYLIST_ID, reconcile

NOW = datetime(2026, 11, 5, 12, 0, tzinfo=timezone.utc)


def clip(clip_id: str) -> dict:
    return {
        "clip_id": clip_id, "song": "Fixture", "mechanism": "M01",
        "generated_at_utc": "2026-11-05T10:00:00Z",
        "targets": ["darse cuenta de"], "selection": "pending",
        "human_feedback": None, "audio_approved": False,
        "pedagogy_approved": False, "playlist_state": "not_added",
    }


def feedback() -> dict:
    # Synthetic fixture only; never write this as real human feedback.
    return {"quote": "fixture only", "source": "unit-test fixture",
            "at_utc": "2026-11-05T11:00:00Z"}


def snapshot(ids: list[str]) -> dict:
    return {"playlist_id": PLAYLIST_ID, "complete": True, "next_cursor": None,
            "retrieved_at_utc": "2026-11-05T12:00:00Z",
            "items": [{"id": clip_id} for clip_id in ids]}


class SongLifecycleAcceptanceTests(unittest.TestCase):
    def test_two_clips_from_one_generation_have_independent_decisions(self):
        first, second = clip("take-a"), clip("take-b")
        first.update(selection="kept", human_feedback=feedback(),
                     audio_approved=True, pedagogy_approved=True,
                     playlist_state="added")
        journal = {"version": 1, "entries": [first, second]}
        validate(journal)
        self.assertEqual(1, reconcile(journal, snapshot(["take-a"]), now=NOW))
        with self.assertRaisesRegex(ValueError, "not marked added"):
            reconcile(journal, snapshot(["take-a", "take-b"]), now=NOW)

    def test_like_is_not_pedagogical_approval(self):
        entry = clip("take-a")
        entry.update(selection="liked", human_feedback=feedback(),
                     audio_approved=True, pedagogy_approved=False,
                     playlist_state="added")
        with self.assertRaisesRegex(ValueError, "playlist addition requires"):
            validate({"version": 1, "entries": [entry]})

    def test_suno_added_but_journal_not_updated_is_detected(self):
        journal = {"version": 1, "entries": [clip("take-a")]}
        with self.assertRaisesRegex(ValueError, "not marked added"):
            reconcile(journal, snapshot(["take-a"]), now=NOW)

    def test_journal_added_but_suno_missing_is_detected(self):
        entry = clip("take-a")
        entry.update(selection="kept", human_feedback=feedback(),
                     audio_approved=True, pedagogy_approved=True,
                     playlist_state="added")
        with self.assertRaisesRegex(ValueError, "absent from playlist"):
            reconcile({"version": 1, "entries": [entry]}, snapshot([]), now=NOW)


if __name__ == "__main__":
    unittest.main()
