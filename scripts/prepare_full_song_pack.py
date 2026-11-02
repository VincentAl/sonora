#!/usr/bin/env python3
"""Prepare an UNAPPROVED full-song experiment from a reviewed draft candidate.

This creates a frozen lyric file and a manifest, but never grants human
approval or calls Suno. Use check_generation_gate.py before generation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

from audit_full_draft import audit
from check_generation_gate import check_generation_gate, lyrics_digest
from validate_experiment import validate


def extract_lyrics(draft: Path) -> str:
    text = draft.read_text(encoding="utf-8")
    lines = text.splitlines()
    try:
        start = lines.index("## Paroles") + 1
    except ValueError as exc:
        raise ValueError("Draft must contain an exact '## Paroles' heading") from exc
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    body = "\n".join(lines[start:end]).strip()
    if not body or not body.startswith("["):
        raise ValueError("No labeled lyric sections found under '## Paroles'")
    return body + "\n"


def prepare(draft: Path, template: Path, output: Path) -> dict:
    if output.exists():
        raise ValueError(f"Refusing to overwrite existing pack: {output}")
    manifest = json.loads(template.read_text(encoding="utf-8"))
    approval = manifest.get("human_lyrics_approval") or {}
    if approval.get("status") == "approved" or approval.get("lyrics_sha256"):
        raise ValueError("Template must not contain an approval or approved digest")
    variants = manifest.get("variants")
    if not isinstance(variants, list) or len(variants) != 1 or variants[0].get("file") != "lyrics.md":
        raise ValueError("Template must declare exactly one variant with file lyrics.md")
    targets = [t["surface"] for t in manifest["common"]["target_words"]]
    _, errors = audit(draft, targets)
    if errors:
        raise ValueError("Draft structural preflight failed: " + "; ".join(errors))
    lyrics = extract_lyrics(draft)
    manifest["status"] = "awaiting_human_lyrics_approval"
    manifest["human_lyrics_approval"] = {"status": "pending"}
    manifest["source_draft_sha256"] = hashlib.sha256(draft.read_bytes()).hexdigest()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="sonora-pack-", dir=output.parent) as tmp:
        staged = Path(tmp) / "pack"
        staged.mkdir()
        (staged / "lyrics.md").write_text(lyrics, encoding="utf-8")
        manifest["candidate_lyrics_sha256"] = lyrics_digest(staged, manifest)
        (staged / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        errors = validate(staged)
        if errors:
            raise ValueError("Experiment validation failed: " + "; ".join(errors))
        if not check_generation_gate(staged):
            raise ValueError("Safety invariant violated: unapproved pack passed generation gate")
        staged.rename(output)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path)
    parser.add_argument("template", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        manifest = prepare(args.draft, args.template, args.output)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print("BLOCKED:", exc)
        return 1
    print("PREPARED (NOT APPROVED):", args.output)
    print("Candidate lyric digest:", manifest["candidate_lyrics_sha256"])
    print("Suno remains blocked until Vincent explicitly approves these exact lyrics.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
