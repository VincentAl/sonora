# Semantic reset — four ideas, two French lines

Status: **text-only drafts**. No Suno audio generated or verified in this repository. This pack supersedes the earlier freeform `generation.md` candidate for the next test; that file is kept as a historical draft.

## Problem addressed

The earlier attempt risked turning a one-minute song into a bilingual dictation: four consecutive French lines recapped all four targets. It also ran long and the directory lacked a manifest, breaking all-pack validation.

The new pack has **83 sung words**, two French lines, four targets, a short-form non-cute style prompt and explicit per-line anchor mapping.

| Target | Spanish idea | French anchor | Shared meaning |
| --- | --- | --- | --- |
| dejar atrás | leaving the city / haste | `derrière moi` | leaving something behind |
| añorar | missing unhurried Sundays | `me manquent` | longing for the same days |
| sosiego | calm beneath the rain | `le calme` | calm in the rainy scene |
| hallar | finding a note in a coat | `j'ai trouvé` | discovering the note |

These are **two lyrical sentences**, not four separate vocabulary definitions. Human review must still determine whether the listener understands all four meanings without reading the text.

## Controlled comparison

- **A — grouped**: both French lines appear together after the chorus.
- **B — spaced**: first French line after the verse, second after the chorus.
- The Spanish lines, French lines, target words and style prompt are identical.
- Each variant has two planned Suno takes, but none has been generated.

The hypothesis is that spreading the same two French lines may improve comprehension without sounding like a classroom interlude. A single listener hearing both variants cannot support an unbiased memory comparison because of carryover. Test different listeners or treat comparisons as qualitative.

## Execution (offline, no credits)

```bash
python3 scripts/validate_experiment.py songs/experiments/2026-10-31-semantic-reset
python3 scripts/prepare_suno_batch.py songs/experiments/2026-10-31-semantic-reset artifacts/suno-semantic-reset
```

The exporter writes four JSON copy/paste jobs. It does not access Suno.

## Listening review

1. Reject any spoken educational introduction, long intro, bouncy/cute beat or inaudible French.
2. Confirm French and Spanish pronunciation, natural tempo, and whether all lines were actually sung.
3. Without showing lyrics, ask for the four Spanish meanings. Record immediate and delayed recall separately.
4. Note whether the French lines feel like natural song lyrics, and whether grouped or spaced placement disrupts the song.
5. Keep failed takes in the log. Do not claim an A/B winner until audio and listening data exist.

The user reports that Suno's higher-quality V6 voice was more convincing than mini for French/Spanish; use mini only as a drafting baseline if available and avoid treating text-only QA as proof of pronunciation.
