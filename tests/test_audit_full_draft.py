#!/usr/bin/env python3
"""Regression tests for the structural full-song preflight; no audio or semantic scoring."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_full_draft import audit

TARGETS = ["Dejé atrás", "Añoro", "Hallé", "sosiego"]
SECTIONS = [
    ("Verso 1 — español", ["Dejé atrás el miedo al salir", "No pude mirar atrás"]),
    ("Respuesta — français", ["J'ai laissé mes regrets derrière moi"]),
    ("Verso 2 — español", ["Añoro la casa del puerto", "El mar se quedó atrás"]),
    ("Respuesta — français", ["Le bruit de tes pas me manque"]),
    ("Verso 3 — español", ["Hallé una carta vieja", "La guardé sin decir nada"]),
    ("Respuesta — français", ["J'ai trouvé un mot dans le livre"]),
    ("Puente — español", ["El sosiego llegó despacio", "Pude dormir sin temor"]),
    ("Respuesta — français", ["Enfin je me suis senti en paix"]),
    ("Estribillo — español", ["Ya no espero tu regreso", "La luz del pasillo se apagó"]),
]

def make_draft(sections=SECTIONS, heading="## Paroles", suffix=""):
    lines = ["# Test", heading]
    for label, lyrics in sections:
        lines.append(f"[{label}]")
        lines.extend(lyrics)
        lines.append("")
    return "\n".join(lines) + suffix

class FullDraftAuditTests(unittest.TestCase):
    def check(self, content, targets=TARGETS):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "draft.md"
            path.write_text(content, encoding="utf-8")
            return audit(path, targets)

    def test_valid_draft_passes_structural_only(self):
        report, errors = self.check(make_draft())
        self.assertEqual([], errors)
        self.assertEqual(9, report["sections"])
        self.assertEqual(4, report["french_lines"])
        self.assertIn("NOT CHECKED", report["human_lyrics_approval"])
        self.assertIn("NOT CHECKED", report["semantic_accuracy"])

    def test_missing_lyrics_heading_fails(self):
        _, errors = self.check(make_draft(heading="## Lyrics"))
        self.assertTrue(any("Missing ## Paroles" in e for e in errors))

    def test_missing_target_fails(self):
        _, errors = self.check(make_draft().replace("Hallé una carta", "Vi una carta"))
        self.assertTrue(any("Missing Spanish target: Hallé" in e for e in errors))

    def test_excessive_repetition_fails(self):
        _, errors = self.check(make_draft().replace("Pude dormir sin temor", "sosiego sosiego sosiego"))
        self.assertTrue(any("Target repeated more than twice: sosiego" in e for e in errors))

    def test_duplicate_target_casefold_fails(self):
        _, errors = self.check(make_draft(), TARGETS + ["SOSIEGO"])
        self.assertTrue(any("Supply distinct target surfaces" in e for e in errors))

    def test_unlabeled_language_fails(self):
        _, errors = self.check(make_draft(sections=[("Intro", ["No hay idioma"])] + SECTIONS))
        self.assertTrue(any("Unrecognized section language" in e for e in errors))
        self.assertTrue(any("Lyric line without language section" in e for e in errors))

    def test_no_spanish_dominance_fails(self):
        sections = [(name, lyrics + (["Encore une phrase française"] * 30 if "français" in name else [])) for name, lyrics in SECTIONS]
        _, errors = self.check(make_draft(sections=sections))
        self.assertTrue(any("Expected Spanish-dominant lyrics" in e for e in errors))

    def test_next_heading_is_not_counted_as_lyrics(self):
        report, errors = self.check(make_draft(suffix="\n## Notes\nHallé sosiego sosiego sosiego\n"))
        self.assertEqual([], errors)
        self.assertEqual(1, report["target_occurrences"]["sosiego"])

if __name__ == "__main__":
    unittest.main()
