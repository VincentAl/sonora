#!/usr/bin/env python3
"""Read-only structural vocabulary preflight; NEVER semantic or human approval.

Usage:
 python3 scripts/check_draft_targets.py DRAFT --target ID:SURFACE:ANCHOR
 python3 scripts/check_draft_targets.py --self-test
ANCHOR must be an exact fragment of a French lyric, not a translation inferred by AI.
"""
import argparse
import json
import re
import unicodedata
from pathlib import Path


def norm(value):
    return unicodedata.normalize("NFC", value).casefold()


def lyric_lines(text):
    inside = False
    lang = None
    lines = {"es": [], "fr": []}
    for raw in text.splitlines():
        line = raw.strip()
        if line == "## Paroles":
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if not inside or not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            tag = norm(line[1:-1])
            lang = ("fr" if any(x in tag for x in ("français", "francés", "french"))
                    else "es" if any(x in tag for x in ("español", "spanish")) else None)
        elif lang in lines:
            lines[lang].append(line)
    return lines


def check(draft, vocabulary, specs):
    lines = lyric_lines(draft)
    items = {item["id"]: item for item in vocabulary["targets"]}
    errors = []
    seen = set()
    for target_id, surface, anchor in specs:
        if target_id in seen:
            errors.append(f"{target_id}: duplicate declaration")
        seen.add(target_id)
        item = items.get(target_id)
        if item is None:
            errors.append(f"{target_id}: absent from register; assessment unknown")
            continue
        if item.get("status") != "candidate":
            errors.append(f"{target_id}: status {item.get('status')!r} is not candidate")
        pattern = r"(?<!\w)" + re.escape(norm(surface)) + r"(?!\w)"
        if not any(re.search(pattern, norm(line)) for line in lines["es"]):
            errors.append(f"{target_id}: Spanish surface absent from Spanish lyrics")
        if not anchor.strip() or not any(norm(anchor) in norm(line) for line in lines["fr"]):
            errors.append(f"{target_id}: French anchor absent from French lyrics")
    if not specs:
        errors.append("no mappings supplied")
    return errors


def self_test():
    draft = ("## Paroles\n[Verso — español]\nDejé atrás el miedo.\n"
             "[Respuesta — français]\nJ’ai laissé mes regrets derrière moi.\n## Notes")
    vocabulary = {"targets": [{"id": "a", "status": "candidate"},
                              {"id": "b", "status": "known"}]}
    good = [("a", "Dejé atrás", "mes regrets derrière moi")]
    assert not check(draft, vocabulary, good)
    assert "absent from register" in str(check(draft, vocabulary, [("x", "Dejé atrás", "mes regrets")]))
    assert "not candidate" in str(check(draft, vocabulary, [("b", "Dejé atrás", "mes regrets")]))
    assert "Spanish surface absent" in str(check(draft, vocabulary, [("a", "hallé", "mes regrets")]))
    assert "French anchor absent" in str(check(draft, vocabulary, [("a", "Dejé atrás", "je suis heureux")]))
    assert "duplicate" in str(check(draft, vocabulary, good + good))
    assert check(draft, vocabulary, [])
    print("PASS: 7 structural cases; semantic accuracy NOT checked")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", nargs="?", type=Path)
    parser.add_argument("--vocabulary", type=Path, default=Path("data/vocabulary.json"))
    parser.add_argument("--target", action="append", default=[], metavar="ID:SURFACE:ANCHOR")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.draft is None:
        parser.error("draft required unless --self-test")
    specs = [tuple(s.split(":", 2)) for s in args.target]
    if any(len(spec) != 3 for spec in specs):
        parser.error("expected ID:SURFACE:ANCHOR")
    try:
        errors = check(args.draft.read_text(encoding="utf-8"),
                       json.loads(args.vocabulary.read_text(encoding="utf-8")), specs)
    except (OSError, ValueError, KeyError) as exc:
        parser.error(str(exc))
    print(json.dumps({"status": "FAIL" if errors else "PASS_STRUCTURAL_ONLY",
                      "errors": errors, "semantic_approval": "NOT CHECKED"},
                     ensure_ascii=False, indent=2))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
