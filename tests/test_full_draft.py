"""Deterministic preflight of full-song drafts without granting approval."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_full_draft import audit  # noqa: E402
from validate_experiment import validate  # noqa: E402

DRAFT = ROOT / "songs/drafts/2026-11-01-la-luz-del-pasillo-full.md"
TARGETS = ["Dejé atrás", "Añoro", "Hallé", "sosiego"]


class FullDraftTests(unittest.TestCase):
    def test_real_full_draft_passes_structural_preflight(self):
        report, errors = audit(DRAFT, TARGETS)
        self.assertEqual([], errors)
        self.assertEqual(4, len(report["target_occurrences"]))
        self.assertEqual(8, report["french_lines"])
        self.assertGreaterEqual(report["sections"], 6)
        self.assertEqual("NOT CHECKED — required before Suno", report["human_lyrics_approval"])

    def test_missing_target_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "draft.md"
            p.write_text(DRAFT.read_text(encoding="utf-8").replace("Hallé una carta", "Vi una carta"), encoding="utf-8")
            _, errors = audit(p, TARGETS)
            self.assertTrue(any("Missing Spanish target: Hallé" in e for e in errors))

    def test_unknown_language_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "draft.md"
            p.write_text(DRAFT.read_text(encoding="utf-8").replace("[Verso 2 — voz A, español]", "[Verso 2 — voz A]"), encoding="utf-8")
            _, errors = audit(p, TARGETS)
            self.assertTrue(any("Unrecognized section language" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
