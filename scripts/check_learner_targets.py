#!/usr/bin/env python3
"""Check proposed learning targets against Vincent's explicit self-assessment.

Example:
  python3 scripts/check_learner_targets.py --targets "echar en cara" "dar marcha atrás"
  python3 scripts/check_learner_targets.py --targets "atreverse a"  # exits 1

Only 'known' is a hard exclusion for NEW learning targets. Unchecked means
'to learn or confirm', never proven unknown; unassessed needs clarification.
"""
import argparse
import json
import pathlib
import sys
import unicodedata

# Explicit spelling variants of the same lexical entry, not broad stemming.
# Avoid marking a known expression as unassessed just because a draft omits
# its optional preposition. Do not infer other aliases from morphology.
LEXICAL_ALIASES = {
    "atreverse": "atreverse a",
    "darse cuenta": "darse cuenta de",
}

DEFAULT_DATA = pathlib.Path(__file__).resolve().parents[1] / "data" / "learner_vocabulary_diagnostic_2026-11-03.json"

def normalize(value):
    return " ".join(unicodedata.normalize("NFC", value).casefold().strip().split())

def classify(data, targets):
    known = {normalize(item) for item in data["known"]}
    candidates = {normalize(item) for item in data["to_learn_or_confirm"]}
    if known & candidates:
        raise ValueError("Diagnostic contains overlapping states")
    results = []
    for target in targets:
        key = normalize(target)
        key = LEXICAL_ALIASES.get(key, key)
        state = "known" if key in known else "to_learn_or_confirm" if key in candidates else "unassessed"
        results.append({"target": target, "state": state, "eligible_as_new_target": state == "to_learn_or_confirm"})
    return results

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=pathlib.Path, default=DEFAULT_DATA)
    parser.add_argument("--targets", nargs="+", required=True)
    args = parser.parse_args()
    data = json.loads(args.data.read_text(encoding="utf-8"))
    results = classify(data, args.targets)
    print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
    return 1 if any(item["state"] == "known" for item in results) else 0

if __name__ == "__main__":
    sys.exit(main())
