"""Generation requires explicit human approval bound to exact lyric bytes."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_generation_gate import check_generation_gate, lyrics_digest  # noqa: E402
from prepare_suno_batch import prepare  # noqa: E402

PACK = ROOT / "songs/experiments/2026-10-31-semantic-reset"


class GenerationGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.pack = Path(self.temp.name) / "pack"
        shutil.copytree(PACK, self.pack)

    def approve(self):
        path = self.pack / "manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["human_lyrics_approval"] = {
            "status": "approved",
            "reviewer": "Vincent",
            "lyrics_sha256": lyrics_digest(self.pack, manifest),
            "evidence": "Vincent explicit approval in review",
            "approved_on": "2026-11-12",
        }
        path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

    def test_old_generated_pack_still_blocked_without_approval(self):
        self.assertTrue(any("not approved" in e for e in check_generation_gate(self.pack)))

    def test_exact_approved_text_passes(self):
        self.approve()
        self.assertEqual([], check_generation_gate(self.pack))

    def test_lyric_edit_invalidates_approval(self):
        self.approve()
        path = self.pack / "A-grouped.md"
        path.write_text(path.read_text(encoding="utf-8") + "\n[Instrumental]\n", encoding="utf-8")
        self.assertTrue(any("SHA-256 mismatch" in e for e in check_generation_gate(self.pack)))

    def test_offline_export_stays_blocked_without_review(self):
        jobs = prepare(self.pack, Path(self.temp.name) / "jobs")
        self.assertTrue(jobs)
        self.assertTrue(all(
            json.loads(path.read_text(encoding="utf-8"))["status"] == "awaiting_human_lyrics_approval"
            for path in jobs
        ))

    def test_offline_export_ready_after_review(self):
        self.approve()
        jobs = prepare(self.pack, Path(self.temp.name) / "jobs")
        self.assertTrue(all(
            json.loads(path.read_text(encoding="utf-8"))["status"] == "ready_for_manual_generation"
            for path in jobs
        ))

    def test_missing_evidence_is_blocked(self):
        self.approve()
        path = self.pack / "manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        del manifest["human_lyrics_approval"]["evidence"]
        path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assertTrue(any("evidence" in e for e in check_generation_gate(self.pack)))

    def test_reviewer_cannot_be_omitted(self):
        self.approve()
        path = self.pack / "manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["human_lyrics_approval"]["reviewer"] = "automation"
        path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
        self.assertTrue(any("Vincent" in e for e in check_generation_gate(self.pack)))


if __name__ == "__main__":
    unittest.main()
