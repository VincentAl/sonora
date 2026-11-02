"""Full-song promotion must remain a blocked, deterministic operation."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prepare_full_song_pack import prepare  # noqa: E402
from check_generation_gate import check_generation_gate, lyrics_digest  # noqa: E402
from validate_experiment import validate, lyric_sections  # noqa: E402

DRAFT = ROOT / "songs/drafts/2026-11-01-la-luz-del-pasillo-full.md"
TEMPLATE = ROOT / "songs/drafts/2026-11-01-la-luz-del-pasillo-pack-template.json"


class FullSongPromotionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.output = self.folder / "pack"

    def test_real_draft_promotes_but_remains_blocked(self):
        manifest = prepare(DRAFT, TEMPLATE, self.output)
        self.assertEqual([], validate(self.output))
        self.assertTrue(check_generation_gate(self.output))
        self.assertEqual("pending", manifest["human_lyrics_approval"]["status"])
        self.assertEqual(manifest["candidate_lyrics_sha256"], lyrics_digest(self.output, manifest))
        lyrics = (self.output / "lyrics.md").read_text(encoding="utf-8")
        self.assertNotIn("## Prévalidation sémantique", lyrics)
        self.assertNotIn("**Statut", lyrics)
        spanish, french = lyric_sections(self.output / "lyrics.md")
        self.assertEqual(8, len(french))
        self.assertGreater(len(spanish), len(french))

    def test_reject_existing_pack_without_overwrite(self):
        self.output.mkdir()
        with self.assertRaisesRegex(ValueError, "Refusing to overwrite"):
            prepare(DRAFT, TEMPLATE, self.output)

    def test_reject_template_with_fake_approval(self):
        t = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        t["human_lyrics_approval"] = {"status": "approved", "reviewer": "Vincent"}
        altered = self.folder / "template.json"
        altered.write_text(json.dumps(t), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "must not contain an approval"):
            prepare(DRAFT, altered, self.output)
        self.assertFalse(self.output.exists())

    def test_missing_target_does_not_create_pack(self):
        altered = self.folder / "draft.md"
        altered.write_text(DRAFT.read_text(encoding="utf-8").replace("Hallé una carta", "Vi una carta"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Missing Spanish target"):
            prepare(altered, TEMPLATE, self.output)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
