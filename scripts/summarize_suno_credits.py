#!/usr/bin/env python3
"""Read-only Suno credit summary from committed run logs; no provider calls."""
import argparse
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")
ROOT = Path(__file__).resolve().parents[1]


def summarize(root: Path, day: str) -> dict:
    datetime.strptime(day, "%Y-%m-%d")
    seen = set()
    grouped = defaultdict(lambda: {"calls": 0, "credits": 0})
    total = calls = 0
    for path in sorted(root.glob("*/runs/*.json")):
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
            rid = item["run_id"]
            timestamp = datetime.fromisoformat(item["generated_at_utc"].replace("Z", "+00:00"))
            credits = item["credits"]
            spent = credits["spent"]
            if not isinstance(rid, str) or not rid or rid in seen:
                raise ValueError("missing or duplicate run_id")
            seen.add(rid)
            if timestamp.tzinfo is None or type(spent) is not int or spent < 0:
                raise ValueError("invalid timestamp or credits.spent")
            before, after = credits.get("before"), credits.get("after")
            if (before is None) != (after is None):
                raise ValueError("incomplete before/after balance")
            if before is not None and (type(before) is not int or type(after) is not int or before - after != spent):
                raise ValueError("inconsistent credit delta")
            if timestamp.astimezone(PARIS).date().isoformat() == day:
                calls += 1
                total += spent
                group = grouped[path.parent.parent.name]
                group["calls"] += 1
                group["credits"] += spent
        except (ValueError, KeyError, TypeError, OSError) as exc:
            raise ValueError(f"Invalid Suno log {path}: {exc}") from exc
    return {"paris_date": day, "generation_calls": calls, "credits_spent": total,
            "by_experiment": dict(sorted(grouped.items())),
            "caveat": "Committed logs only; provider-side or unlogged usage is not included."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=datetime.now(PARIS).date().isoformat())
    parser.add_argument("--runs-root", type=Path, default=ROOT / "songs/experiments")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = summarize(args.runs_root, args.date)
    except ValueError as exc:
        parser.exit(1, f"BLOCKED: {exc}\n")
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Paris {result['paris_date']}: {result['generation_calls']} calls, {result['credits_spent']} credits recorded")
        for name, item in result["by_experiment"].items():
            print(f"  {name}: {item['calls']} calls, {item['credits']} credits")
        print(result["caveat"])


if __name__ == "__main__":
    main()
