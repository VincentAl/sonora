#!/usr/bin/env python3
"""Validate every Sonora experiment pack; fail closed on missing manifests.

Usage: python3 scripts/validate_all_experiments.py [experiments-root]
No Suno calls or external dependencies.
"""
from __future__ import annotations

import sys
from pathlib import Path

from validate_experiment import validate

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = ROOT / "songs" / "experiments"


def validate_all(root: Path) -> list[str]:
    if not root.is_dir():
        return [f"Experiments directory missing: {root}"]
    packs = sorted(path for path in root.iterdir() if path.is_dir() and not path.name.startswith("."))
    if not packs:
        return [f"No experiment packs found under {root}"]
    errors: list[str] = []
    for pack in packs:
        if not (pack / "manifest.json").is_file():
            errors.append(f"{pack.name}: missing manifest.json")
            continue
        errors.extend(f"{pack.name}: {error}" for error in validate(pack))
    return errors


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ROOT
    errors = validate_all(root)
    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1
    count = len([p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")])
    print(f"PASS: validated {count} experiment packs under {root}")
    print("NOTE: static QA does not establish semantic correctness or learning efficacy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
