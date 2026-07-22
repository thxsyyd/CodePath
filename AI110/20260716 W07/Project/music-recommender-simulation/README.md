# 🎵 Music Recommender Simulation

## Project Summary

This project is a **content-based music recommender**. It represents each song as a
set of attributes (genre, mood, energy, and so on) and represents a listener as a
"taste profile." It scores every song against that profile with a weighted rule,
ranks the results, and returns the top matches along with a human-readable reason
for each pick. The goal is not to train a machine-learning model, but to show how
simple data plus a scoring rule can already behave like a recommender — and where
that simple approach breaks down.

---

## How The System Works

### How real recommenders work

Large platforms like Spotify and YouTube mainly use two strategies. **Collaborative
filtering** predicts what you'll like based on *other users' behavior* — "people who
listen to what you listen to also liked X" — using signals like likes, skips, and
shared playlists. **Content-based filtering** ignores other users and instead looks
at the *attributes of the songs themselves* (genre, tempo, mood, energy) and finds
songs similar to the ones you already like. Real products blend both; this project
implements the content-based half, because it works from song attributes alone and
needs no large user-behavior dataset.

### What my version prioritizes

My recommender is purely content-based. It prioritizes an exact **genre** match most
heavily, then **mood**, then how close a song's **energy** is to the listener's target,
with a small bonus for matching their **acoustic** preference. Energy is scored by
*closeness* rather than "higher is better," because a listener who wants to relax wants
*low* energy, not maximum energy.

### Features used

**`Song`** uses: `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`,
`valence`, `danceability`, `acousticness`. The scoring logic actively uses `genre`,
`mood`, `energy`, and `acousticness`; the rest are available for display or future
extensions.

**`UserProfile`** stores: `favorite_genre`, `favorite_mood`, `target_energy`, and
`likes_acoustic`.

### Algorithm Recipe

- **+2.0** exact genre match
- **+1.0** exact mood match
- **+2.0 × (1 − |target_energy − song_energy|)** — energy closeness
- **+0.5** acoustic preference matches

The system uses a **Scoring Rule** (score one song) and a separate **Ranking Rule**
(sort all scored songs and take the top *k*). Splitting them keeps "how relevant is
this song?" separate from "which songs win?", so each can be tested and changed
independently.

### Expected bias

Because genre is weighted highest and the catalog is small and pop-heavy, the system
is likely to over-recommend popular genres and create a "filter bubble" — repeatedly
surfacing songs very similar to what the profile already prefers, and rarely
introducing anything new.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output from `python -m src.main`, which runs three deliberately different
profiles through the recommender:

```
============================================================
Profile: High-Energy Pop
  prefs: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9}
------------------------------------------------------------
  1. Sunrise City           (pop/happy)      score=4.84
  2. Gym Hero               (pop/intense)    score=3.94
  3. Festival Skies         (edm/happy)      score=2.96
  4. Rooftop Lights         (indie pop/happy) score=2.72
  5. Storm Runner           (rock/intense)   score=1.98

============================================================
Profile: Chill Lofi
  prefs: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35}
------------------------------------------------------------
  1. Library Rain           (lofi/chill)     score=5.00
  2. Midnight Coding        (lofi/chill)     score=4.86
  3. Focus Flow             (lofi/focused)   score=3.90
  4. Spacewalk Thoughts     (ambient/chill)  score=2.86
  5. Coffee Shop Stories    (jazz/relaxed)   score=1.96

============================================================
Profile: Deep Intense Rock
  prefs: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9}
------------------------------------------------------------
  1. Storm Runner           (rock/intense)   score=4.98
  2. Gym Hero               (pop/intense)    score=2.94
  3. Concrete Rhymes        (hip-hop/intense) score=2.80
  4. Festival Skies         (edm/happy)      score=1.96
  5. Neon Overdrive         (edm/energetic)  score=1.90
```

Each profile's top pick scores near the maximum (~5.0) because it matches on
genre, mood, and energy at once. Lower-ranked songs win on energy closeness
alone.

---

## Experiments You Tried

**Experiment: comparing three profiles.** Running High-Energy Pop, Chill Lofi,
and Deep Intense Rock side by side showed the system responds sensibly to
different tastes — each profile's #1 song matched on all three signals (genre +
mood + energy) and scored close to the 5.0 maximum.

**Experiment: what dominates the ranking.** Because genre is weighted highest
(+2.0), songs sharing the profile's genre reliably occupy the top slots. For the
Chill Lofi profile, the top three results were all `lofi`; for High-Energy Pop,
the top two were both `pop`. Energy closeness (up to +2.0) mainly decides the
*lower* ranks, where several different-genre songs tie on "near the target
energy."

**What changing the genre weight would do.** If genre were lowered from 2.0 to,
say, 0.5, energy and mood would drive ranking instead, so results would become
more genre-diverse but less aligned with the listener's stated favorite genre —
a direct precision-vs-diversity tradeoff.

---

## Limitations and Risks

- **Filter bubble.** Because genre is weighted most heavily, the recommender
  keeps surfacing the listener's existing favorite genre and rarely introduces
  anything new. The Chill Lofi profile got three lofi songs in a row.
- **Tiny catalog.** With only 15 songs, "top 5" is a third of the entire
  library, so recommendations aren't very selective.
- **No understanding of meaning.** It matches genre/mood labels exactly and does
  math on energy; it has no notion of lyrics, language, or actual audio.
- **Exact-match brittleness.** `indie pop` and `pop` are treated as completely
  unrelated genres, even though a listener would hear them as close.

These are explored further in the model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



