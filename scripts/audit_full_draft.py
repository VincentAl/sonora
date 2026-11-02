#!/usr/bin/env python3
"""Deterministic structural preflight for full-length Sonora lyric drafts.

This is NOT an approval or a semantic/audio assessment.
Usage:
  python3 scripts/audit_full_draft.py songs/drafts/2026-11-01-la-luz-del-pasillo-full.md \
    --target "Dejé atrás" --target "Añoro" --target "Hallé" --target "sosiego"
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from validate_experiment import count_phrase

WORD = re.compile(r"\b\w+(?:['’]\w+)*\b", re.UNICODE)


def audit(path: Path, targets: list[str]) -> tuple[dict, list[str]]:
    errors: list[str] = []
    spanish: list[str] = []
    french: list[str] = []
    sections: list[str] = []
    in_lyrics = False
    language = None
    found = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line == "## Paroles":
            found = True
            in_lyrics = True
            continue
        if in_lyrics and line.startswith("## "):
            break
        if not in_lyrics or not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            tag = line[1:-1].casefold()
            if re.search(r"fran[cç]ais|franc[eé]s|french", tag):
                language = "fr"
            elif re.search(r"espa[nñ]ol|spanish", tag):
                language = "es"
            else:
                errors.append(f"Unrecognized section language: {line}")
                language = None
            sections.append(line)
            continue
        if language == "es":
            spanish.append(line)
        elif language == "fr":
            french.append(line)
        else:
            errors.append(f"Lyric line without language section: {line}")

    if not found:
        errors.append("Missing ## Paroles section")
    if len(sections) < 6:
        errors.append("Expected at least 6 labeled sections for a full song")
    if len(french) < 4:
        errors.append("Expected at least 4 French lyric lines")
    if len(spanish) <= len(french):
        errors.append("Expected Spanish-dominant lyrics")

    spanish_text = "\n".join(spanish)
    counts = {target: count_phrase(spanish_text, target) for target in targets}
    if not targets or len(set(t.casefold() for t in targets)) != len(targets):
        errors.append("Supply distinct target surfaces")
    for target, count in counts.items():
        if count == 0:
            errors.append(f"Missing Spanish target: {target}")
        if count > 2:
            errors.append(f"Target repeated more than twice: {target} ({count})")
    report = {
        "draft": str(path),
        "sections": len(sections),
        "spanish_lines": len(spanish),
        "french_lines": len(french),
        "sung_words": len(WORD.findall(spanish_text + "\n" + "\n".join(french))),
        "target_occurrences": counts,
        "human_lyrics_approval": "NOT CHECKED — required before Suno",
        "semantic_accuracy": "NOT CHECKED — requires human review",
        "duration": "NOT MEASURED — requires generated audio",
    }
    return report, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path)
    parser.add_argument("--target", action="append", required=True)
    args = parser.parse_args()
    try:
        report, errors = audit(args.draft, args.target)
    except OSError as exc:
        print(f"FAIL: {exc}")
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    for error in errors:
        print("FAIL:", error)
    if errors:
        return 1
    print("PASS: structural preflight only; NOT approved for generation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
