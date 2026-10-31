#!/usr/bin/env python3
"""Export a deterministic, *offline* Suno copy/paste batch. Never calls an API.

Usage: python3 scripts/prepare_suno_batch.py [pack-dir] [output-dir]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from validate_experiment import DEFAULT_PACK, validate
from check_generation_gate import check_generation_gate

ROOT = Path(__file__).resolve().parents[1]


def prepare(pack: Path, output: Path) -> list[Path]:
    errors = validate(pack)
    if errors:
        raise ValueError("Experiment validation failed:\n" + "\n".join(errors))
    gate_errors = check_generation_gate(pack)
    manifest = json.loads((pack / "manifest.json").read_text(encoding="utf-8"))
    style_path = ROOT / manifest["common"]["style_prompt"]
    style = style_path.read_text(encoding="utf-8").strip()
    output.mkdir(parents=True, exist_ok=True)
    created = []
    for variant in manifest["variants"]:
        raw = (pack / variant["file"]).read_text(encoding="utf-8")
        lyrics = "\n".join(line for line in raw.splitlines() if not line.startswith("# ")).strip()
        for replicate in range(1, manifest["common"].get("planned_generation_replicates_per_variant", 2) + 1):
            job_id = f"{manifest['experiment_id']}-{variant['id']}-r{replicate}"
            payload = {
                "job_id": job_id,
                "experiment_id": manifest["experiment_id"],
                "variant": variant["id"],
                "replicate": replicate,
                "title_suggestion": f"Sonora {manifest['experiment_id']} {variant['id']} #{replicate}",
                "style_prompt": style,
                "lyrics": lyrics,
                "generation_mode": "custom_lyrics",
                "target_duration_seconds": manifest["common"].get("estimated_duration_seconds"),
                "model_preference": manifest["common"].get("model_preference"),
                "intro_max_seconds": manifest["common"].get("intro_max_seconds"),
                "status": "ready_for_manual_generation" if not gate_errors else "awaiting_human_lyrics_approval",
                "generation_gate_errors": gate_errors,
                "suno_url": None,
                "note": "Offline preparation only. Suno calls require an approved human lyrics gate and available credits."
            }
            dest = output / f"{job_id}.json"
            dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            created.append(dest)
    return created


def main() -> int:
    pack = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACK
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "artifacts" / "suno-batch"
    try:
        files = prepare(pack, output)
    except (OSError, ValueError, KeyError) as exc:
        print("FAIL:", exc, file=sys.stderr)
        return 1
    print(f"Prepared {len(files)} offline jobs in {output} (no Suno calls or credits used).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
