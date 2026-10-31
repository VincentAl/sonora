"""Regression tests for follow-up semantic anchoring and all-pack discovery."""
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
from validate_all_experiments import validate_all  # noqa: E402
from validate_experiment import validate  # noqa: E402

FOLLOWUP = ROOT / "songs/experiments/2026-10-31-reinforcement"


class ReinforcementTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.pack = Path(self.temp.name) / "2026-10-31-reinforcement"
        shutil.copytree(FOLLOWUP, self.pack)

    def test_reference_followup_passes(self):
        self.assertEqual([], validate(self.pack))

    def test_early_late_control_rejects_spanish_drift(self):
        path = self.pack / "B-late-anchors.md"
        text = path.read_text(encoding="utf-8").replace("último tren", "primer tren")
        path.write_text(text, encoding="utf-8")
        self.assertTrue(any("Spanish lyrics differ" in e for e in validate(self.pack)))

    def test_early_late_control_rejects_french_drift(self):
        path = self.pack / "B-late-anchors.md"
        text = path.read_text(encoding="utf-8").replace("après la pluie", "avant la pluie")
        path.write_text(text, encoding="utf-8")
        self.assertTrue(any("French lyrics differ" in e for e in validate(self.pack)))

    def test_missing_sosiego_anchor_fails(self):
        path = self.pack / "A-early-anchors.md"
        text = path.read_text(encoding="utf-8").replace("sa quiétude", "son calme")
        path.write_text(text, encoding="utf-8")
        self.assertTrue(any("missing French anchor" in e for e in validate(self.pack)))

    def test_four_offline_jobs(self):
        paths = prepare(self.pack, Path(self.temp.name) / "jobs")
        self.assertEqual(4, len(paths))
        jobs = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
        self.assertEqual({"A", "B"}, {job["variant"] for job in jobs})
        self.assertEqual({1, 2}, {job["replicate"] for job in jobs})
        self.assertTrue(all(job["suno_url"] is None for job in jobs))

    def test_all_pack_discovery_fails_on_missing_manifest(self):
        root = Path(self.temp.name) / "experiments"
        root.mkdir()
        shutil.copytree(self.pack, root / self.pack.name)
        (root / "broken-pack").mkdir()
        errors = validate_all(root)
        self.assertTrue(any("broken-pack: missing manifest.json" in e for e in errors))

    def test_all_real_packs_pass(self):
        self.assertEqual([], validate_all(ROOT / "songs/experiments"))


if __name__ == "__main__":
    unittest.main()
