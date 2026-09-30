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
