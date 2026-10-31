#!/usr/bin/env python3
"""Audit planned vocabulary separately from actual learner exposures.

Draft lyrics and unplayed Suno generations MUST NOT increment appearance_count.
Usage: python3 scripts/audit_vocabulary.py
"""
from __future__ import annotations

import csv
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOCABULARY = ROOT / "data" / "vocabulary.csv"
EXPERIMENTS = ROOT / "songs" / "experiments"
FIELDS = ["term", "translation", "status", "introduced_on", "last_used_on",
          "appearance_count", "notes"]
STATES = {"new", "reinforcing", "familiar", "acquired"}


def audit(vocabulary: Path = VOCABULARY, experiments: Path = EXPERIMENTS):
    """Return (errors, coverage by lemma). Coverage is planned, never listened."""
    errors = []
    try:
        with vocabulary.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != FIELDS:
                errors.append(f"Vocabulary CSV must have columns: {', '.join(FIELDS)}")
            rows = list(reader)
    except OSError as exc:
        return [f"Cannot read vocabulary: {exc}"], {}

    by_term = {}
    for row in rows:
        term = (row.get("term") or "").strip()
        if not term:
            errors.append("Empty vocabulary term")
            continue
        if term in by_term:
            errors.append(f"Duplicate vocabulary term: {term}")
            continue
        by_term[term] = row
        if (row.get("status") or "") not in STATES:
            errors.append(f"{term}: invalid learning status")
        try:
            count = int(row.get("appearance_count") or "")
            if count < 0:
                raise ValueError
        except ValueError:
            errors.append(f"{term}: appearance_count must be a nonnegative integer")
            continue
        introduced = (row.get("introduced_on") or "").strip()
        last = (row.get("last_used_on") or "").strip()
        if count == 0:
            if introduced or last:
                errors.append(f"{term}: zero real exposures must have blank dates")
            if row.get("status") != "new":
                errors.append(f"{term}: zero real exposures require status=new")
        else:
            if not introduced or not last:
                errors.append(f"{term}: positive exposures require both dates")
            else:
                try:
                    first_day = date.fromisoformat(introduced)
                    last_day = date.fromisoformat(last)
                    if last_day < first_day:
                        errors.append(f"{term}: last_used_on precedes introduced_on")
                except ValueError:
                    errors.append(f"{term}: exposure dates must be ISO YYYY-MM-DD")

    if not experiments.is_dir():
        return errors + [f"Missing experiments directory: {experiments}"], {}
    packs = sorted(p for p in experiments.iterdir() if p.is_dir() and not p.name.startswith("."))
    if not packs:
        errors.append("No experiment packs found")

    coverage = {}
    for pack in packs:
        try:
            manifest = json.loads((pack / "manifest.json").read_text(encoding="utf-8"))
            targets = manifest["common"]["target_words"]
            variants = manifest["variants"]
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f"{pack.name}: cannot inspect manifest: {exc}")
            continue
        seen = set()
        for target in targets:
            lemma = target["lemma"]
            if lemma in seen:
                errors.append(f"{pack.name}: duplicate target {lemma}")
                continue
            seen.add(lemma)
            if lemma not in by_term:
                errors.append(f"{pack.name}: target {lemma} missing from vocabulary.csv")
            elif by_term[lemma]["translation"] != target["fr"]:
                errors.append(f"{pack.name}: translation mismatch for {lemma}")
            stats = coverage.setdefault(lemma, {
                "planned_packs": 0, "planned_variants": 0,
                "anchored_packs": 0, "anchored_variants": 0,
            })
            anchored = sum(lemma in variant.get("anchored_lemmas", []) for variant in variants)
            stats["planned_packs"] += 1
            stats["planned_variants"] += len(variants)
            stats["anchored_packs"] += int(anchored > 0)
            stats["anchored_variants"] += anchored
    return errors, coverage


def main() -> int:
    errors, coverage = audit()
    if errors:
        for error in errors:
            print("FAIL:", error, file=sys.stderr)
        return 1
    print("PASS: vocabulary registry matches draft experiment manifests")
    print("NOTE: planned variants are NOT real listening exposures.")
    writer = csv.writer(sys.stdout)
    writer.writerow(["term", "planned_packs", "planned_variants",
                     "anchored_packs", "anchored_variants"])
    for term, stats in sorted(coverage.items()):
        writer.writerow([term, *(stats[key] for key in
                        ("planned_packs", "planned_variants",
                         "anchored_packs", "anchored_variants"))])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
