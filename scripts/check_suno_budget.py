#!/usr/bin/env python3
"""Deterministic Suno spending preflight; no API, audio or model calls.

Before every Suno request, check the *live* provider balance separately, then
run this script with that balance. Record the completed call in a run JSON and
commit it before the next generation. This checks the local daily budget, not
Suno's actual reset policy or account balance.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PARIS = ZoneInfo("Europe/Paris")
DEFAULT_DAILY_LIMIT = 50
ROOT = Path(__file__).resolve().parents[1]


def daily_spend(runs_root: Path, paris_day: str) -> int:
    """Sum observed credits once per run, using the Paris calendar date.

    Fail closed for malformed logs; never silently undercount an unknown cost.
    """
    datetime.strptime(paris_day, "%Y-%m-%d")
    total = 0
    seen: set[str] = set()
    for path in sorted(runs_root.glob("*/runs/*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            run_id = data["run_id"]
            stamp = datetime.fromisoformat(data["generated_at_utc"].replace("Z", "+00:00"))
            credits = data["credits"]
            spent = credits["spent"]
            if not isinstance(run_id, str) or not run_id:
                raise ValueError("missing run_id")
            if run_id in seen:
                raise ValueError(f"duplicate run_id {run_id}")
            seen.add(run_id)
            if stamp.tzinfo is None:
                raise ValueError("generated_at_utc must have timezone")
            if type(spent) is not int or spent < 0:
                raise ValueError("credits.spent must be a non-negative integer")
            before, after = credits.get("before"), credits.get("after")
            if before is not None and after is not None:
                if type(before) is not int or type(after) is not int or before - after != spent:
                    raise ValueError("credit balance delta differs from credits.spent")
            if stamp.astimezone(PARIS).date().isoformat() == paris_day:
                total += spent
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid Suno run log {path}: {exc}") from exc
    return total


def check_budget(spent: int, proposed: int, balance: int, daily_limit: int = DEFAULT_DAILY_LIMIT) -> list[str]:
    """Return reasons to block; never make a provider call."""
    if any(type(x) is not int for x in (spent, proposed, balance, daily_limit)):
        return ["Budget values must be integers"]
    if spent < 0 or proposed <= 0 or balance < 0 or daily_limit <= 0:
        return ["Invalid budget values (cost and limit must be positive)"]
    errors = []
    if spent + proposed > daily_limit:
        errors.append(f"Daily limit: {spent} already spent + {proposed} proposed > {daily_limit}")
    if proposed > balance:
        errors.append(f"Insufficient live Suno balance: {proposed} proposed > {balance} available")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cost", type=int, required=True, help="Expected cost of ONE proposed Suno call")
    parser.add_argument("--balance", type=int, required=True, help="Fresh live Suno credits balance")
    parser.add_argument("--date", default=datetime.now(PARIS).date().isoformat(), help="Paris date YYYY-MM-DD")
    parser.add_argument("--daily-limit", type=int, default=DEFAULT_DAILY_LIMIT)
    parser.add_argument("--runs-root", type=Path, default=ROOT / "songs/experiments")
    args = parser.parse_args()
    try:
        spent = daily_spend(args.runs_root, args.date)
        errors = check_budget(spent, args.cost, args.balance, args.daily_limit)
    except ValueError as exc:
        errors = [str(exc)]
        spent = None
    if errors:
        for error in errors:
            print("BLOCKED:", error)
        return 1
    print(f"OK: Paris {args.date}; spent {spent}/{args.daily_limit}, proposed {args.cost}; "
          f"remaining daily allowance {args.daily_limit - spent - args.cost}; "
          f"live Suno balance {args.balance}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
