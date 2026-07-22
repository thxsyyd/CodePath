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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



