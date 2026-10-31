# Semantic reset — four ideas, two French lines

Status: **four real Suno v6-mini audio takes generated on 31 October 2026; first human review completed, structure rejected for further audio iteration**. This pack supersedes the earlier freeform `generation.md` candidate for the next test; that file is kept as a historical draft.

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
- Each variant now has two generated Suno takes (four total); the comparison is not yet evaluated by a human listener.

Human feedback from Vincent:
- B is preferable to A because the French is less visibly grouped;
- however, this does **not** validate B;
- both variants still feel like translated/paraphrased French sentences placed end-to-end;
- A is especially obvious because it resembles a Spanish verse followed by its French translation;
- the target words are repeated too many times for a one-minute song, making the writing feel pedagogical rather than natural;
- these problems are visible from the lyrics alone and should have been caught before spending Suno credits.

Therefore the A/B placement question is secondary. The experiment exposed a more important upstream writing problem: French must contribute naturally to the song, and target repetition should happen mainly across songs rather than several times inside one minute.

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

The user reports that Suno's higher-quality V6 voice was more convincing than mini for French/Spanish; these v6-mini takes are prototypes only and do not validate pronunciation.

## First real Suno MCP run — 31 October 2026

Full machine-readable log: [runs/2026-10-31-mcp-smoke-test.json](runs/2026-10-31-mcp-smoke-test.json).

| Variant | Take | Song | Duration | First aligned word | Outro aligned? |
| --- | --- | --- | ---: | ---: | --- |
| A grouped | 1 | [Listen](https://suno.com/song/43caccdc-d1d5-4123-88da-9f0f5fdb517d) | 59.56 s | 8.17 s | No — likely truncated |
| A grouped | 2 | [Listen](https://suno.com/song/70e582cb-b367-4d40-8b4b-67baaeacc9fe) | 59.96 s | 8.25 s | Yes |
| B spaced | 1 | [Listen](https://suno.com/song/ac7962eb-a401-465a-8b15-65d1ada951ec) | 60.00 s | 8.66 s | Yes, at cap |
| B spaced | 2 | [Listen](https://suno.com/song/a3be1624-9939-4830-b67a-b55cd8d55743) | 59.96 s | 0.74 s | Yes |

Suno generated **two takes per API call**. Two successful calls generated four clips and spent **20 credits total** (100 → 80 on the Free plan). A prior request using `negative_style` was rejected with `feature_not_on_plan` before generation; the exclusion terms were moved into the common style string.

**Early mechanical findings:** the 3-second intro target failed in 3/4 takes despite an explicit style instruction. The hard 60-second cap appears to truncate A1's outro. Automatic analysis reports guitar/acoustic female-vocal arrangements, but it does **not** establish that the songs sound non-cute or that French is intelligible. The first-word timestamps are automatic lyric alignments, not a human-verified vocal-onset measurement. No A/B memory winner can be declared yet.

**Next:** do not generate another audio variant from this structure. First create text-only lyric candidates with fewer forced repetitions and more natural bilingual integration, then obtain Vincent's text review before spending more Suno credits.
