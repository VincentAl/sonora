# Sonora — first controlled listening experiment

## Hypothesis

Two autonomous French anchors placed at separate moments (B) may be easier to process and remember than the same two anchors grouped together (A), without hurting musical naturalness. C has only one French anchor and is exploratory: it is **not** a clean placement comparison because it changes the amount of French.

## What is held constant

A and B use the same Spanish lyric lines in the same order, the same French lines in the same order, the same four vocabulary targets, and the same folk style prompt. Only the insertion points change. The validator checks these invariants automatically. Suno generations will still vary stochastically: generate at least two replicates per variant before drawing any conclusions.

## Before audio generation

```sh
python3 scripts/validate_experiment.py
python3 -m unittest discover -s tests -v
python3 scripts/prepare_suno_batch.py
```

The exporter creates six JSON jobs under `artifacts/suno-batch/`. These are **offline copy/paste packages**, not API calls. No credits are used. The folder is gitignored. A Suno login and authorization to spend credits are required to actually generate audio.

## Blind listening protocol

1. Assign anonymized IDs to the six generated takes; do not reveal A/B/C to the listener. Randomize the order and balance it across listeners when possible.
2. Use the same playback device and volume. Listen once without reading lyrics or seeing the target translations.
3. Rate French intelligibility, Spanish intelligibility, musical naturalness (0–5 each), and rushed transitions (0–5, where 5 is worse). Record actual duration and whether all lines are sung.
4. Ask the listener to write the meanings of **añorar, sosiego, hallar, dejar atrás**, without cues. Score each 0/1 by semantic accuracy (not just thematic association). Do not reveal the correct answers until after the delayed test.
5. Repeat the same uncued recall test after 24 hours, without replaying the songs. Avoid playing both A and B to the same person in a memory comparison: prior exposure contaminates the second condition. Use separate listener groups, or treat a single-person comparison as purely qualitative.
6. Log all takes, including failed ones; don't cherry-pick the best-sounding take. Compare medians and inspect failures before making changes to prompts.

## Decision rules

- **Hard gate:** if French cannot be understood without lyrics, the generation fails the pedagogical objective regardless of musical quality.
- **A vs B:** favor B only if its listening quality is not materially worse and recall is better across more than one listener/take. Otherwise keep both in the candidate pool.
- **C:** compare listener fatigue and musical naturalness, but do not interpret recall differences as a placement effect.
- **No audio yet:** no claim of improved memorization, pronunciation, or naturalness is justified.

## Suggested review record

`take_id,variant,replicate,suno_url,duration_s,french_intelligibility_0_5,spanish_intelligibility_0_5,musical_naturalness_0_5,rushed_transitions_0_5,immediate_recall_0_4,delayed_recall_0_4,missing_lines,comments`

Store results separately from lyric manifests; do not mark drafts as generated until a real URL and a listening review exist.
