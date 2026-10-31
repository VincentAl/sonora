"""Regression tests for experiment QA and deterministic Suno job export."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_experiment import validate  # noqa: E402
from prepare_suno_batch import prepare  # noqa: E402

PACK = ROOT / "songs/experiments/2026-10-31-anchoring"


class ExperimentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.pack = Path(self.tmp.name) / "pack"
        shutil.copytree(PACK, self.pack)

    def mutate_manifest(self, fn):
        path = self.pack / "manifest.json"
        obj = json.loads(path.read_text(encoding="utf-8"))
        fn(obj)
        path.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")

    def test_reference_pack_passes(self):
        self.assertEqual([], validate(self.pack))

    def test_missing_spanish_target_fails(self):
        path = self.pack / "A-anchors-grouped.md"
        path.write_text(path.read_text(encoding="utf-8").replace("añoro", "extraño"), encoding="utf-8")
        self.assertTrue(any("missing Spanish target" in e for e in validate(self.pack)))

    def test_anchor_not_declared_fails(self):
        self.mutate_manifest(lambda m: m["variants"][0].update(anchored_lemmas=["añorar"]))
        self.assertTrue(any("count differs" in e for e in validate(self.pack)))

    def test_anchor_missing_fails(self):
        path = self.pack / "B-anchors-spaced.md"
        path.write_text(path.read_text(encoding="utf-8").replace("J'ai laissé derrière moi", "J'ai oublié"), encoding="utf-8")
        self.assertTrue(any("missing French anchor" in e for e in validate(self.pack)))

    def test_controlled_pair_spanish_drift_fails(self):
        path = self.pack / "B-anchors-spaced.md"
        path.write_text(path.read_text(encoding="utf-8").replace("la luz de la tarde", "el color de la tarde"), encoding="utf-8")
        self.assertTrue(any("Spanish lyrics differ" in e for e in validate(self.pack)))

    def test_export_six_jobs_without_network(self):
        jobs = prepare(self.pack, Path(self.tmp.name) / "out")
        self.assertEqual(6, len(jobs))
        self.assertEqual(6, len({json.loads(p.read_text())["job_id"] for p in jobs}))
        self.assertTrue(all(json.loads(p.read_text())["suno_url"] is None for p in jobs))

    def test_invalid_pack_cannot_export(self):
        self.mutate_manifest(lambda m: m["variants"][0].update(french_anchor_count=0))
        with self.assertRaises(ValueError):
            prepare(self.pack, Path(self.tmp.name) / "out")


if __name__ == "__main__":
    unittest.main()
