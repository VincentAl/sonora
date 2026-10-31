# Sonora

Sonora explores music as a learning medium.

The first proof of concept focuses on Spanish vocabulary: generate short original songs that remain enjoyable background music while deliberately reinforcing a small set of target words and expressions.

## Current POC

- Generator: Suno
- Song length: about 1 minute
- Target load: 3–4 Spanish words/expressions per song
- Main language: Spanish
- French: sparse, natural, standalone lines that anchor exact meanings
- Musical families:
  1. intimate folk
  2. soft indie pop
  3. minimal Latin/electronic

## Core idea

A target should be understandable from context, but ambiguity must eventually be removed. French is not used as line-by-line translation. Instead, a short autonomous French sentence naturally contains the exact equivalent of one target.

Example:

Spanish:
> Te di por hecho sin pensarlo más.

French break:
> Ton sourire, je l'ai pris pour acquis.

The French line is a real lyric, not a glossary entry, but it anchors `dar por hecho` precisely.

## Repository

- `docs/SPEC.md` — product and generation specification
- `docs/PEDAGOGY_RULES.md` — learning rules discovered during testing
- `prompts/` — Suno style prompts
- `data/vocabulary.csv` — vocabulary tracking
- `data/songs.csv` — song-generation history
- `songs/` — generated lyric packs and metadata
- `scripts/` — future automation

## Next milestone

Generate and evaluate a small manual batch, then automate:

1. vocabulary selection
2. lyric generation
3. Suno generation
4. review/selection
5. spaced reappearance of learned vocabulary

## First controlled experiment

The first lyric-only comparison is ready in
[`songs/experiments/2026-10-31-anchoring/`](songs/experiments/2026-10-31-anchoring/).
It contains three variants testing the placement and density of French semantic anchors,
a manifest, a review protocol, and a dependency-free static validator.

Run locally:

```bash
python3 scripts/validate_experiment.py
```

No audio has been generated yet. Static checks cannot assess pronunciation, musical naturalness, or recall.

## Suno integration update (October 2026)

Suno now documents an **official MCP (Beta) connector for ChatGPT**, authenticated via Suno login rather than an API key. See [`docs/SUNO_INTEGRATION.md`](docs/SUNO_INTEGRATION.md) for setup and current automation limitations. Generation uses Suno credits and is not triggered without authorization.

## Reproducible QA and offline generation queue

The A/B controlled comparison is now explicit in the manifest: the same Spanish and French lines are held constant, with only French-anchor placement changed. C changes the number of anchors and remains exploratory.

See [the listening protocol](docs/EXPERIMENT_PROTOCOL.md). The validator is generic (no hardcoded exception for C), the regression suite checks seven success/failure scenarios, and GitHub Actions runs static checks on push/PR.

```bash
python3 scripts/validate_experiment.py
python3 -m unittest discover -s tests -v
python3 scripts/prepare_suno_batch.py
```

The last command writes **six offline JSON jobs** (A/B/C × two takes) into ignored `artifacts/suno-batch/`. Each contains lyrics, style prompt, and metadata for manual or future authorized MCP generation. It never calls Suno or spends credits. Record audio evaluations in `data/reviews.csv`.

Static QA and seven unit tests passed locally on 31 October 2026; GitHub Actions status should be checked separately. **No audio exists yet**, so recall, pronunciation and musical quality are untested.

## Second controlled experiment — early vs late anchors

The [reinforcement pack](songs/experiments/2026-10-31-reinforcement/) reuses the four Spanish targets and now anchors **sosiego → quiétude** and **hallar → trouver**, which were intentionally left unanchored in the first song. Two variants keep the same ten Spanish lines and two French lines, changing only whether the French bridge comes before or after the chorus. Both use the same indie-pop prompt. This is an untested hypothesis about anchor timing, not evidence of better recall.

```bash
python3 scripts/validate_all_experiments.py
python3 scripts/prepare_suno_batch.py songs/experiments/2026-10-31-reinforcement artifacts/suno-reinforcement
```

The exporter now prepares **10 offline jobs across two packs** (6 + 4), without any Suno calls. CI validates every experiment pack and runs the regression tests.

## Current preferred generation pack (31 October 2026)

The [semantic-reset pack](songs/experiments/2026-10-31-semantic-reset/) repairs a quality/CI issue: the prior standalone `generation.md` was not a valid experiment pack, leaving all-pack validation unable to pass. It now has two matched, shorter lyric variants, a manifest, and an energetic non-cute style prompt. Each of the **four** targets is semantically paired with French across **two** lyrical lines, rather than translating every line.

```bash
python3 scripts/validate_all_experiments.py
python3 -m unittest discover -s tests -v
python3 scripts/prepare_suno_batch.py songs/experiments/2026-10-31-semantic-reset artifacts/suno-semantic-reset
```

This prepares four offline jobs (A/B × two replicates). The exporter spends no credits and does not claim to generate audio. The latest user feedback prioritizes a **45–60 s song**, no didactic intro, natural pronunciation, and a less soft/more driving arrangement. Suno V6 sounded better than mini to the listener; that observation still needs controlled comparison.
