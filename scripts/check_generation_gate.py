#!/usr/bin/env python3
"""Deterministic human-approval gate for Sonora audio generation.

Run before ANY Suno call. Static validation is necessary but not sufficient:
Vincent must explicitly approve the exact lyric files. No network or AI calls.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from validate_experiment import validate


def lyrics_digest(pack: Path, manifest: dict) -> str:
    """Hash variant filenames + exact bytes; order independent."""
    digest = hashlib.sha256()
    for variant in sorted(manifest["variants"], key=lambda item: item["file"]):
        name = variant["file"]
        digest.update(name.encode("utf-8") + b"\0")
        digest.update((pack / name).read_bytes() + b"\0")
    return digest.hexdigest()


def check_generation_gate(pack: Path) -> list[str]:
    errors = validate(pack)
    if errors:
        return errors
    manifest = json.loads((pack / "manifest.json").read_text(encoding="utf-8"))
    approval = manifest.get("human_lyrics_approval") or {}
    if approval.get("status") != "approved":
        return ["Human lyric review is not approved: no Suno generation allowed"]
    if approval.get("reviewer") != "Vincent":
        errors.append("Human approval must explicitly name Vincent as reviewer")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/check_generation_gate.py <experiment-pack>", file=sys.stderr)
        return 2
    pack = Path(sys.argv[1])
    try:
        errors = check_generation_gate(pack)
        if errors:
            for error in errors:
                print("BLOCKED:", error)
            if (pack / "manifest.json").exists():
                manifest = json.loads((pack / "manifest.json").read_text(encoding="utf-8"))
                if not validate(pack):
                    print("Current lyric digest:", lyrics_digest(pack, manifest))
            return 1
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print("BLOCKED:", exc)
        return 1
    print("APPROVED: exact lyric files match Vincent's recorded approval")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
