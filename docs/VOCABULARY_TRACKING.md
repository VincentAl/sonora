# Vocabulary planning versus actual exposure

The vocabulary registry at `data/vocabulary.csv` is now seeded with the four
targets already used in the two draft lyric experiments. **All appearance counts
are zero.** A word appearing in a lyric draft, a prepared Suno JSON job, or an
unplayed audio file is *not* a learner exposure.

## Definitions

- `status=new` means the learner has not yet logged a completed exposure.
- `appearance_count` counts completed listening sessions in which the target
  was actually encountered, **not** the number of lyric variants or Suno takes.
- `introduced_on` is the date of the first completed exposure.
- `last_used_on` is the most recent completed exposure date.
- `reinforcing`, `familiar`, `acquired` are learner states, not inferred from
  a number of draft appearances. They require evidence from recall checks.
- `translation` uses the exact canonical French meaning declared in the manifests.

Do not auto-increment exposures when generating a track: it may never be heard.
Do not treat a successful generation as proof of learning.

## Draft coverage report

Run:

```sh
python3 scripts/audit_vocabulary.py
```

The audit checks that every target in every experiment manifest exists in the
registry, with the same canonical French translation, and validates exposure
counts and dates. It reports *planned packs*, *planned variants*, *anchored
packs*, and *anchored variants* separately. These are planning metrics only.

The first two packs contain five lyric variants total (3 + 2), with all four
terms present in each variant. Each term is semantically anchored in at least
one pack. This is **not** five listens or a validated memorization outcome.

## Next data step

After actual audio and human listening exist, introduce a dedicated listening
event log with listener ID, take ID, date, and recall result. Derive exposure
counts from those events rather than editing `appearance_count` based on
generated songs. Keep listener IDs pseudonymous and avoid personal data.
