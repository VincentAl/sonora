# Sonora — Generation Spec

## 1. Goal

Create songs that are pleasant enough to play while working and that incidentally teach or reinforce knowledge.

The first POC teaches Spanish vocabulary to a French-speaking learner.

The experience should feel like listening to music first and studying second.

## 2. POC format

### Duration
Target roughly 1 minute per song while iterating.

### Vocabulary density
Use 3–4 targets per song.

Targets should be slightly above the learner's current level:
- not basic textbook vocabulary;
- still inferable from a good context;
- useful or expressive enough to recur naturally.

### Language balance
Spanish dominates.

French should be sparse:
- usually 1–2 French passages per minute;
- short enough not to turn the song into a lesson;
- clearly separated from surrounding Spanish.

## 3. Semantic anchoring

Context alone is insufficient when it permits a plausible but inaccurate interpretation.

Each important target should eventually receive an unambiguous semantic anchor.

Bad:
> desfase — un décalage

This sounds like a glossary.

Better:
> Nos mouvements n'avaient plus le même rythme, il y avait un vrai décalage.

The French line is autonomous and musical while preserving the exact target meaning.

### Key rule

French must not be a direct subtitle of the immediately preceding Spanish line.

Instead:
1. write a natural Spanish lyric;
2. later insert a short French lyric that expresses a related image or idea;
3. ensure that the exact French equivalent of the target occurs naturally in that sentence.

## 4. Bilingual transitions

Avoid rapid word-for-word code switching.

Prefer:
- a complete Spanish phrase or couplet;
- a short pause/break;
- one autonomous French sentence;
- a return to Spanish.

Suno prompt should request:
- slow vocal phrasing;
- spacious delivery;
- clear pauses around French passages;
- minimal Spanish accent on French;
- no rushed bilingual transitions.

## 5. Song structure

A useful 1-minute pattern:

- Verse: introduce targets in Spanish context
- French break: anchor one target
- Chorus: repeat targets naturally in Spanish
- Short post-chorus or second break: anchor another target
- Outro: reuse one or two targets with no translation

Do not force every target into French in every song.

## 6. Musical families

### Intimate folk
Nylon/acoustic guitar, soft piano, light organic percussion, close vocal, restrained dynamics.

### Soft indie pop
Dreamy synths, clean guitar, warm bass, restrained electronic drums, understated hook.

### Minimal Latin/electronic
Soft bass, subtle Latin rhythmic influence, airy synths, hypnotic but background-friendly groove.

## 7. Learning progression

Vocabulary should move through states:

- new
- reinforcing
- familiar
- acquired

A word may appear:
- first with strong contextual support and one exact anchor;
- later in Spanish-only contexts;
- later still as an incidental recurrence.

The long-term system should behave like lightweight spaced repetition embedded in music.

## 8. Quality checks

Before generation, verify:
- Is each target at the intended level?
- Is the exact meaning preserved?
- Could the learner infer a wrong meaning from context?
- Does any French line sound like a dictionary entry?
- Is French sparse enough?
- Are lyrics short enough for slow delivery?
- Does the song remain enjoyable without caring about the learning goal?

After generation, evaluate:
- intelligibility of French;
- Spanish/French pronunciation;
- transition speed;
- musical naturalness;
- recall of target meanings after repeated listening.
