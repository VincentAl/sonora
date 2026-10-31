#!/usr/bin/env python3
"""Dependency-free static validation for a Sonora lyric experiment.

Usage: python3 scripts/validate_experiment.py songs/experiments/2026-10-31-anchoring
Static QA does not establish semantic correctness, pronunciation or learning efficacy.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DEFAULT_PACK = Path(__file__).resolve().parents[1] / "songs/experiments/2026-10-31-anchoring"


def lyric_sections(path: Path) -> tuple[list[str], list[str]]:
    """Return (Spanish/other lyric lines, French lyric lines), excluding headings/tags."""
    spanish, french = [], []
    in_french = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            in_french = "french" in line.casefold()
            continue
        (french if in_french else spanish).append(line)
    return spanish, french


def contains_phrase(text: str, phrase: str) -> bool:
    """Require whole-word phrase, case-insensitively, not a substring of a longer word."""
    return bool(re.search(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", text, re.IGNORECASE))


def validate(directory: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Cannot load manifest: {exc}"]

    common = manifest.get("common", {})
    targets = common.get("target_words", [])
    if not isinstance(targets, list) or not 3 <= len(targets) <= 4:
        return ["Expected 3–4 vocabulary targets"]
    target_map: dict[str, dict] = {}
    for target in targets:
        lemma, surface = target.get("lemma"), target.get("surface")
        if not isinstance(lemma, str) or not lemma.strip() or not isinstance(surface, str) or not surface.strip():
            errors.append("Every target needs nonempty lemma and surface")
            continue
        if lemma in target_map:
            errors.append(f"Duplicate target lemma: {lemma}")
        target_map[lemma] = target

    variants = manifest.get("variants", [])
    if not isinstance(variants, list) or not variants:
        return errors + ["At least one variant is required"]
    seen_ids: set[str] = set()
    parsed: dict[str, tuple[list[str], list[str]]] = {}
    for variant in variants:
        variant_id = variant.get("id", "<missing-id>")
        if variant_id in seen_ids:
            errors.append(f"Duplicate variant id: {variant_id}")
        seen_ids.add(variant_id)
        file_name = variant.get("file")
        if not isinstance(file_name, str) or not file_name.endswith(".md") or Path(file_name).name != file_name:
            errors.append(f"{variant_id}: invalid lyric filename")
            continue
        path = directory / file_name
        if not path.is_file():
            errors.append(f"{variant_id}: missing file {file_name}")
            continue
        spanish, french = lyric_sections(path)
        parsed[variant_id] = (spanish, french)
        spanish_text = "\n".join(spanish)
        for lemma, target in target_map.items():
            if not contains_phrase(spanish_text, target["surface"]):
                errors.append(f"{variant_id}: missing Spanish target {target['surface']} ({lemma})")

        expected_count = variant.get("french_anchor_count")
        if not isinstance(expected_count, int) or expected_count not in (1, 2):
            errors.append(f"{variant_id}: french_anchor_count must be 1 or 2")
        elif len(french) != expected_count:
            errors.append(f"{variant_id}: expected {expected_count} French lines, found {len(french)}")
        anchored = variant.get("anchored_lemmas")
        if not isinstance(anchored, list) or len(anchored) != len(set(anchored)):
            errors.append(f"{variant_id}: anchored_lemmas must be a unique list")
            continue
        # Legacy packs anchor one target per French line. Newer packs can
        # naturally anchor multiple targets in a single line via anchor_line_map.
        line_map = variant.get("anchor_line_map")
        if line_map is None:
            if len(anchored) != expected_count:
                errors.append(f"{variant_id}: anchored_lemmas count differs from French line count")
        elif not isinstance(line_map, dict) or set(line_map) != set(anchored):
            errors.append(f"{variant_id}: anchor_line_map must cover exactly anchored_lemmas")
        if common.get("require_all_targets_anchored") and set(anchored) != set(target_map):
            errors.append(f"{variant_id}: not all targets have French anchors")
        semantic_links = variant.get("semantic_links", {})
        if common.get("require_all_targets_anchored"):
            if not isinstance(semantic_links, dict) or any(
                not isinstance(semantic_links.get(lemma), str) or not semantic_links[lemma].strip()
                for lemma in anchored
            ):
                errors.append(f"{variant_id}: missing semantic link explanations")
        french_text = "\n".join(french)
        for lemma in anchored:
            target = target_map.get(lemma)
            if not target:
                errors.append(f"{variant_id}: unknown anchored lemma {lemma}")
                continue
            if not target.get("anchor"):
                errors.append(f"{variant_id}: no French anchor defined for {lemma}")
                continue
            if isinstance(line_map, dict):
                index = line_map.get(lemma)
                if type(index) is not int or not 0 <= index < len(french):
                    errors.append(f"{variant_id}: invalid French line index for {lemma}")
                elif not contains_phrase(french[index], target["anchor"]):
                    errors.append(f"{variant_id}: missing French anchor for {lemma} in assigned line")
            elif not contains_phrase(french_text, target["anchor"]):
                errors.append(f"{variant_id}: missing French anchor for {lemma}")

        max_words = common.get("max_sung_words")
        if max_words is not None:
            if type(max_words) is not int or max_words <= 0:
                errors.append("max_sung_words must be a positive integer")
            else:
                word_count = len(re.findall(r"\b\w+(?:['’]\w+)*\b", spanish_text + "\n" + french_text))
                if word_count > max_words:
                    errors.append(f"{variant_id}: {word_count} sung words exceeds max {max_words}")

    for pair in manifest.get("controlled_pairs", []):
        ids = pair.get("variants", [])
        if len(ids) != 2 or any(i not in parsed for i in ids):
            errors.append(f"Invalid controlled pair: {ids}")
            continue
        a, b = (parsed[i] for i in ids)
        if "spanish_lyrics" in pair.get("hold_constant", []) and a[0] != b[0]:
            errors.append(f"Controlled pair {ids}: Spanish lyrics differ")
        if "french_lyrics" in pair.get("hold_constant", []) and a[1] != b[1]:
            errors.append(f"Controlled pair {ids}: French lyrics differ")
    return errors


def main() -> int:
    directory = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACK
    problems = validate(directory)
    if problems:
        for problem in problems:
            print("FAIL:", problem)
        return 1
    print(f"PASS: {directory} — declared targets, anchors and controlled pairs")
    print("NOTE: semantic accuracy, pronunciation, musical quality and recall require listening tests.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
