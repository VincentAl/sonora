#!/usr/bin/env python3
"""Read-only reconciliation of a complete Suno playlist snapshot and Sonora's journal.

The snapshot is obtained outside this script using Suno MCP. This tool never
calls Suno, updates a playlist, or changes a human decision.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from validate_weekly_feedback import DEFAULT_PATH, _utc, validate

PLAYLIST_ID = "152d06fb-bd76-4d7c-9eb3-b11bd3c90bde"


def reconcile(journal: object, snapshot: object, *, now: datetime | None = None,
              max_age_minutes: int = 60) -> int:
    """Return clip count, or fail closed on incomplete/stale data or drift."""
    validate(journal)
    if not isinstance(snapshot, dict) or snapshot.get("playlist_id") != PLAYLIST_ID:
        raise ValueError("Snapshot playlist_id does not match Sonora — Hebdo")
    if snapshot.get("complete") is not True or snapshot.get("next_cursor"):
        raise ValueError("Snapshot must include all playlist pages (complete=true, no next_cursor)")
    stamp = snapshot.get("retrieved_at_utc")
    _utc(stamp, "snapshot.retrieved_at_utc")
    retrieved = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    now = now or datetime.now(timezone.utc)
    age_seconds = (now - retrieved).total_seconds()
    if age_seconds < -300 or age_seconds > max_age_minutes * 60:
        raise ValueError("Snapshot is stale or has a future timestamp; fetch a fresh full playlist")
    items = snapshot.get("items")
    if not isinstance(items, list):
        raise ValueError("snapshot.items must be an array")
    playlist_ids: set[str] = set()
    for i, item in enumerate(items):
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"].strip():
            raise ValueError(f"snapshot.items[{i}].id must be a nonempty Suno clip ID")
        clip_id = item["id"]
        if clip_id in playlist_ids:
            raise ValueError(f"Duplicate playlist clip ID: {clip_id}")
        playlist_ids.add(clip_id)

    entries = {e["clip_id"]: e for e in journal["entries"]}
    expected = {clip_id for clip_id, e in entries.items() if e["playlist_state"] == "added"}
    untracked = sorted(playlist_ids - set(entries))
    missing = sorted(expected - playlist_ids)
    unexpected = sorted((playlist_ids & set(entries)) - expected)
    problems = []
    if untracked:
        problems.append(f"untracked playlist clips: {', '.join(untracked)}")
    if missing:
        problems.append(f"journal says added but absent from playlist: {', '.join(missing)}")
    if unexpected:
        problems.append(f"playlist contains clips not marked added: {', '.join(unexpected)}")
    if problems:
        raise ValueError("; ".join(problems))
    return len(playlist_ids)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path, help="Complete Suno MCP playlist snapshot as JSON")
    parser.add_argument("--journal", type=Path, default=DEFAULT_PATH)
    args = parser.parse_args()
    try:
        journal = json.loads(args.journal.read_text(encoding="utf-8"))
        snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        count = reconcile(journal, snapshot)
    except (OSError, ValueError) as exc:
        print(f"BLOCKED: {exc}")
        return 1
    print(f"OK: {count} playlist clips match the Sonora feedback journal (read-only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
