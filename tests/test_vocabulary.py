"""Vocabulary planning is distinct from actual listening history."""
from __future__ import annotations

import csv
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_vocabulary import audit, FIELDS  # noqa: E402

SOURCE = ROOT / "data" / "vocabulary.csv"
PACKS = ROOT / "songs" / "experiments"


class VocabularyAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.csv = Path(self.temp.name) / "vocabulary.csv"
        shutil.copyfile(SOURCE, self.csv)

    def modify(self, change):
        with self.csv.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        change(rows)
        with self.csv.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)

    def test_all_existing_drafts_covered_without_exposures(self):
        errors, coverage = audit(self.csv, PACKS)
        self.assertEqual([], errors)
        self.assertEqual({"añorar", "sosiego", "hallar", "dejar atrás"}, set(coverage))
        # Derive expected coverage from manifests rather than freezing the
        # number of packs/variants: adding a new valid experiment is not a regression.
        manifests = [
            json.loads(p.read_text(encoding="utf-8"))
            for p in sorted(PACKS.glob("*/manifest.json"))
        ]
        for lemma, stats in coverage.items():
            relevant = [
                m for m in manifests
                if any(t["lemma"] == lemma for t in m["common"]["target_words"])
            ]
            expected_packs = len(relevant)
            expected_variants = sum(len(m["variants"]) for m in relevant)
            expected_anchored = sum(
                any(lemma in v["anchored_lemmas"] for v in m["variants"])
                for m in manifests
            )
            self.assertEqual(expected_packs, stats["planned_packs"])
            self.assertEqual(expected_variants, stats["planned_variants"])
            self.assertEqual(expected_anchored, stats["anchored_packs"])
        with self.csv.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertTrue(all(row["appearance_count"] == "0" for row in rows))
        self.assertTrue(all(not row["introduced_on"] and not row["last_used_on"] for row in rows))

    def test_missing_registry_entry_is_rejected(self):
        self.modify(lambda rows: rows.pop())
        errors, _ = audit(self.csv, PACKS)
        self.assertTrue(any("missing from vocabulary.csv" in e for e in errors))

    def test_draft_cannot_be_falsely_marked_as_listened(self):
        self.modify(lambda rows: rows[0].update(introduced_on="2026-10-31"))
        errors, _ = audit(self.csv, PACKS)
        self.assertTrue(any("zero real exposures" in e for e in errors))

    def test_nonnew_state_requires_real_exposure(self):
        self.modify(lambda rows: rows[0].update(status="reinforcing"))
        errors, _ = audit(self.csv, PACKS)
        self.assertTrue(any("require status=new" in e for e in errors))

    def test_positive_exposure_requires_dates(self):
        self.modify(lambda rows: rows[0].update(appearance_count="1"))
        errors, _ = audit(self.csv, PACKS)
        self.assertTrue(any("require both dates" in e for e in errors))

    def test_translation_mismatch_is_rejected(self):
        self.modify(lambda rows: rows[0].update(translation="wrong"))
        errors, _ = audit(self.csv, PACKS)
        self.assertTrue(any("translation mismatch" in e for e in errors))

    def test_duplicate_lemma_is_rejected(self):
        self.modify(lambda rows: rows.append(rows[0].copy()))
        errors, _ = audit(self.csv, PACKS)
        self.assertTrue(any("Duplicate vocabulary term" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
