#!/usr/bin/env python3
"""Static QA for Sonora experiment packs. No external dependencies or Suno calls.

Usage:
    python3 scripts/validate_experiment.py songs/experiments/2026-10-31-anchoring
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def validate(directory: Path) -> list[str]:
    errors: list[str] = []
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    targets = manifest["common"]["target_words"]
    if not 3 <= len(targets) <= 4:
        errors.append("Expected 3-4 vocabulary targets")
    for variant in manifest["variants"]:
        path = directory / variant["file"]
        if not path.exists():
            errors.append(f"{variant['id']}: missing file {path}")
            continue
        lyrics = path.read_text(encoding="utf-8")
        for target in targets:
            if target["surface"].casefold() not in lyrics.casefold():
                errors.append(f"{variant['id']}: missing Spanish target {target['surface']}")
        french_sections: list[str] = []
        active_french = False
        for raw_line in lyrics.splitlines():
            line = raw_line.strip()
            if line.startswith("[") and line.endswith("]"):
                active_french = "french" in line.casefold()
                continue
            if active_french and line and not line.startswith("#"):
                french_sections.append(line)
        if len(french_sections) != variant["french_anchor_count"]:
            errors.append(
                f"{variant['id']}: expected {variant['french_anchor_count']} French lines, "
                f"found {len(french_sections)}"
            )
        all_french = "\n".join(french_sections).casefold()
        for target in targets:
            anchor = target["anchor"]
            if not anchor:
                continue
            # Variant C intentionally omits the second anchor; the manifest says so.
            if variant["id"] == "C" and target["lemma"] == "dejar atrás":
                continue
            if anchor.casefold() not in all_french:
                errors.append(f"{variant['id']}: missing French anchor for {target['lemma']}")
        if len(french_sections) not in (1, 2):
            errors.append(f"{variant['id']}: French line count outside 1-2")
    return errors


def main() -> int:
    directory = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        Path(__file__).resolve().parents[1]
        / "songs/experiments/2026-10-31-anchoring"
    )
    problems = validate(directory)
    if problems:
        for problem in problems:
            print("FAIL:", problem)
        return 1
    print("PASS: target surfaces and declared French anchors found in all variants.")
    print("NOTE: semantic correctness, timing, naturalness and audio require human review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
