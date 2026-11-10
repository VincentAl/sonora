#!/usr/bin/env python3
"""Extract the exact Vincent-reviewed M08 V2 lyrics without rewriting them.

This is a preparatory, read-only command. A digest is NOT a Suno approval:
the generation gate still requires a validated pack and explicit approval
bound to its exact exported bytes.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

START = "## Paroles V2 — texte candidat à figer après revue"
END = "## Contrôle sémantique éditorial (non automatisable)"


def extract(text: str) -> str:
    lines = text.splitlines()
    if lines.count(START) != 1 or lines.count(END) != 1:
        raise ValueError("M08 V2 section markers missing or duplicated")
    a = lines.index(START)
    b = lines.index(END)
    if b <= a + 1:
        raise ValueError("M08 V2 lyric section is empty")
    body = "\n".join(lines[a + 1:b]).strip() + "\n"
    if not body.startswith("[Intro") or "[Outro" not in body:
        raise ValueError("Expected intro/outro sections missing")
    return body


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path)
    parser.add_argument("--output", type=Path, help="Optional new file; never overwrite")
    args = parser.parse_args()
    try:
        lyrics = extract(args.draft.read_text(encoding="utf-8"))
        digest = hashlib.sha256(lyrics.encode("utf-8")).hexdigest()
        if args.output:
            with args.output.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(lyrics)
        print("M08 V2 lyric bytes SHA-256:", digest)
        print("NOT APPROVED FOR GENERATION: pack gate remains mandatory")
        return 0
    except (OSError, ValueError) as exc:
        print("BLOCKED:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
