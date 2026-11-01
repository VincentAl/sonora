"""Lyric section parsing must support the French tags used by dialogue drafts."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_experiment import lyric_sections  # noqa: E402


class LyricSectionTests(unittest.TestCase):
    def parse(self, content: str):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "lyrics.md"
            path.write_text(content, encoding="utf-8")
            return lyric_sections(path)

    def test_french_english_and_abbreviated_tags(self):
        spanish, french = self.parse(
            "[Verse — español]\nDejé atrás la ciudad.\n"
            "[Voix 2 — français]\nMoi, j'ai laissé les clés.\n"
            "[Verse — Spanish]\nAñoro tu risa.\n"
            "[Chorus — French]\nTon rire me manque.\n"
            "[Réponse FR]\nJe reste ici.\n"
        )
        self.assertEqual(["Dejé atrás la ciudad.", "Añoro tu risa."], spanish)
        self.assertEqual(
            ["Moi, j'ai laissé les clés.", "Ton rire me manque.", "Je reste ici."],
            french,
        )

    def test_unaccented_francais_and_refrain_not_fr(self):
        spanish, french = self.parse(
            "[Couplet francais]\nJ'ai laissé la porte ouverte.\n"
            "[Refrain]\nSigo aquí.\n"
        )
        self.assertEqual(["Sigo aquí."], spanish)
        self.assertEqual(["J'ai laissé la porte ouverte."], french)

    def test_existing_french_tags_still_work(self):
        spanish, french = self.parse(
            "[Verse — Spanish]\nLa noche cae.\n"
            "[Chorus — French]\nLa nuit tombe.\n"
        )
        self.assertEqual(["La noche cae."], spanish)
        self.assertEqual(["La nuit tombe."], french)


if __name__ == "__main__":
    unittest.main()
