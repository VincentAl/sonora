"""Regression tests for short-form four-target Sonora generation packs."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from prepare_suno_batch import prepare  # noqa: E402
from validate_experiment import validate  # noqa: E402

PACK = ROOT / "songs/experiments/2026-10-31-semantic-reset"


class SemanticResetTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.pack = Path(self.tmp.name) / "pack"
        shutil.copytree(PACK, self.pack)

    def change_manifest(self, change):
        path = self.pack / "manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        change(manifest)
        path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

    def test_four_targets_two_french_lines_pass(self):
        self.assertEqual([], validate(self.pack))

    def test_anchor_line_must_match_target(self):
        self.change_manifest(
            lambda m: m["variants"][0]["anchor_line_map"].update({"hallar": 0})
        )
        self.assertTrue(any("missing French anchor" in e for e in validate(self.pack)))

    def test_missing_target_anchor_fails(self):
        self.change_manifest(
            lambda m: m["variants"][0].update(
                anchored_lemmas=["añorar", "sosiego", "hallar"]
            )
        )
        self.assertTrue(any("not all targets" in e for e in validate(self.pack)))

    def test_missing_semantic_link_fails(self):
        self.change_manifest(
            lambda m: m["variants"][0]["semantic_links"].update({"sosiego": ""})
        )
        self.assertTrue(any("missing semantic link" in e for e in validate(self.pack)))

    def test_oversized_lyrics_fail(self):
        self.change_manifest(lambda m: m["common"].update(max_sung_words=30))
        self.assertTrue(any("sung words exceeds max" in e for e in validate(self.pack)))

    def test_controlled_pair_detects_changed_french(self):
        path = self.pack / "B-spaced.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "nos dimanches me manquent", "je pense aux dimanches"
            ),
            encoding="utf-8",
        )
        self.assertTrue(any("French lyrics differ" in e for e in validate(self.pack)))

    def test_export_four_offline_jobs(self):
        jobs = prepare(self.pack, Path(self.tmp.name) / "out")
        self.assertEqual(4, len(jobs))
        payloads = [json.loads(path.read_text(encoding="utf-8")) for path in jobs]
        self.assertTrue(all(job["suno_url"] is None for job in payloads))
        self.assertTrue(all(job["generation_mode"] == "custom_lyrics" for job in payloads))
        self.assertTrue(all(job["intro_max_seconds"] == 3 for job in payloads))
        self.assertTrue(all("V6" in job["model_preference"] for job in payloads))
        self.assertTrue(all(job["target_duration_seconds"] == "45-65" for job in payloads))
        self.assertTrue(all("no spoken introduction" in job["style_prompt"] for job in payloads))
        self.assertTrue(all("Je laisse la ville" in job["lyrics"] for job in payloads))


if __name__ == "__main__":
    unittest.main()
