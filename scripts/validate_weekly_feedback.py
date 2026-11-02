#!/usr/bin/env python3
"""Validate Sonora's weekly feedback journal without touching Suno or audio."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_PATH = Path(__file__).resolve().parents[1] / "data/weekly_feedback.json"
SELECTIONS = {"pending", "liked", "rejected", "kept"}
PLAYLIST_STATES = {"not_added", "added", "removed"}


def _utc(value: object, field: str) -> None:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an ISO 8601 UTC timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field}: invalid timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise ValueError(f"{field} must include UTC timezone")


def validate(data: object) -> None:
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("Expected journal object with version=1")
    entries = data.get("entries")
    if not isinstance(entries, list):
        raise ValueError("entries must be an array")
    seen: set[str] = set()
    for i, item in enumerate(entries):
        tag = f"entries[{i}]"
        if not isinstance(item, dict):
            raise ValueError(f"{tag} must be an object")
        for field in ("clip_id", "song", "mechanism"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError(f"{tag}.{field} must be nonempty text")
        clip_id = item["clip_id"]
        if clip_id in seen:
            raise ValueError(f"Duplicate clip_id: {clip_id}")
        seen.add(clip_id)
        _utc(item.get("generated_at_utc"), f"{tag}.generated_at_utc")
        targets = item.get("targets")
        if not isinstance(targets, list) or not targets or any(
            not isinstance(x, str) or not x.strip() for x in targets
        ) or len(set(targets)) != len(targets):
            raise ValueError(f"{tag}.targets must be unique nonempty strings")
        selection = item.get("selection")
        playlist = item.get("playlist_state")
        if selection not in SELECTIONS or playlist not in PLAYLIST_STATES:
            raise ValueError(f"{tag}: invalid selection or playlist_state")
        audio_ok = item.get("audio_approved")
        pedagogy_ok = item.get("pedagogy_approved")
        if type(audio_ok) is not bool or type(pedagogy_ok) is not bool:
            raise ValueError(f"{tag}: approvals must be booleans")
        feedback = item.get("human_feedback")
        if feedback is not None:
            if not isinstance(feedback, dict) or any(
                not isinstance(feedback.get(k), str) or not feedback[k].strip()
                for k in ("quote", "source", "at_utc")
            ):
                raise ValueError(f"{tag}: feedback needs quote, source and at_utc")
            _utc(feedback["at_utc"], f"{tag}.human_feedback.at_utc")
        if (selection != "pending" or audio_ok or pedagogy_ok) and feedback is None:
            raise ValueError(f"{tag}: human feedback required for decisions")
        if playlist == "added" and not (
            selection == "kept" and audio_ok and pedagogy_ok
        ):
            raise ValueError(f"{tag}: playlist addition requires kept and both approvals")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("journal", nargs="?", type=Path, default=DEFAULT_PATH)
    args = parser.parse_args()
    try:
        data = json.loads(args.journal.read_text(encoding="utf-8"))
        validate(data)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"BLOCKED: {exc}")
        return 1
    print(f"OK: {len(data['entries'])} weekly feedback entries validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
