#!/usr/bin/env python3
"""Deterministic human-approval gate for Sonora audio generation.

Run before ANY Suno call. Static validation is necessary but not sufficient:
Vincent must explicitly approve the lyric text. Approval evidence and date are required.\nAny subsequent lyric edit requires renewed human approval; this script cannot\nindependently prove that an approval applies to unchanged text. No AI calls.
"""
from __future__ import annotations

import json
import hashlib
import sys
from pathlib import Path

from validate_experiment import validate


def lyrics_digest(pack: Path, manifest: dict) -> str:
    """Stable digest for legacy packs and optional edit-detection on new approvals."""
    digest = hashlib.sha256()
    for variant in sorted(manifest["variants"], key=lambda item: item["file"]):
        digest.update(variant["file"].encode("utf-8"))
        digest.update(b"\\0")
        digest.update((pack / variant["file"]).read_bytes())
        digest.update(b"\\0")
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
    if not approval.get("evidence"):
        errors.append("Human approval must cite an explicit review (evidence URL or reference)")
    if not approval.get("approved_on"):
        errors.append("Human approval must include its date")
    if approval.get("lyrics_sha256") and approval["lyrics_sha256"] != lyrics_digest(pack, manifest):
        errors.append("SHA-256 mismatch: lyrics changed since approval")
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
            return 1
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print("BLOCKED:", exc)
        return 1
    print("APPROVED: explicit Vincent lyric approval recorded; review any lyric edits before generation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
