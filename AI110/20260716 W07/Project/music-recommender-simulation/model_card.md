# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0** — a content-based music recommender.

---

## 2. Intended Use

VibeFinder recommends songs from a small catalog based on a listener's stated
taste profile (favorite genre, favorite mood, target energy level, and whether
they prefer acoustic music). It generates a ranked top-k list with a plain-language
reason for each pick.

It assumes the user can describe their taste as a handful of attributes and that
their preference is stable during a session. **This is a classroom exploration
tool, not a production system** — it exists to show how simple data plus a scoring
rule can behave like a recommender, and to make the resulting biases visible.

---

## 3. How the Model Works

VibeFinder looks at attributes of each song and compares them to what the listener
says they want. For each song it awards points: a big bonus if the genre matches,
a smaller bonus if the mood matches, points for how close the song's energy is to
the listener's target (closer is better), and a small bonus if the song's acoustic
level matches their preference. It adds these up into a single score, then sorts
all songs from highest to lowest and returns the top few.

The key idea is that energy is scored by *closeness*, not "more is better" — a
listener who wants to relax wants low energy, so a song is rewarded for being
*near* the target rather than high.

Compared to the starter code (which returned the first few songs unchanged), I
implemented the full scoring rule, the ranking step, an explanation for each pick,
and a second acoustic-preference signal in the object-oriented version.

---

## 4. Data

The catalog has **15 songs**, stored in `data/songs.csv`. It started with 10 and I
added 5 to widen the variety.

- **Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop,
  edm, r&b, hip-hop, classical.
- **Moods represented:** happy, chill, intense, relaxed, moody, focused,
  energetic, romantic, sad.
- **Each song has:** genre, mood, energy, tempo, valence, danceability, acousticness.

**What's missing:** the catalog is still tiny and pop/lofi-leaning, with only one
or two songs per newer genre. Whole regions of musical taste (folk, metal, country,
world music, non-English music) are absent, so a listener with those tastes would
get poor matches.

---

## 5. Strengths

- **Clear, sensible top picks.** For every profile tested, the #1 song matched on
  genre, mood, and energy simultaneously and scored close to the 5.0 maximum
  (e.g., Chill Lofi → "Library Rain" at 5.00).
- **Transparent reasoning.** Every recommendation lists exactly why it was chosen
  (which signals contributed how many points), so results are easy to audit.
- **Energy closeness works well.** Low-energy profiles correctly pulled up calm
  songs and pushed down loud ones, matching intuition.

---

## 6. Limitations and Bias

- **Filter bubble.** Genre is weighted most heavily, so the system keeps
  recommending the listener's existing favorite genre. The Chill Lofi profile
  returned three lofi songs in its top three — it never introduces anything new.
- **Exact-match brittleness.** `indie pop` and `pop` are treated as unrelated,
  even though a human hears them as close, so near-miss genres are unfairly ignored.
- **Popularity/representation bias.** Genres with more songs in the catalog (pop,
  lofi) have more chances to appear; underrepresented genres rarely surface even
  for listeners who might like them.
- **No semantics.** It matches labels and does arithmetic on numbers; it has no
  understanding of lyrics, language, or how a song actually sounds.

---

## 7. Evaluation

I tested three deliberately different profiles: **High-Energy Pop**
(pop/happy/0.9), **Chill Lofi** (lofi/chill/0.35), and **Deep Intense Rock**
(rock/intense/0.9). For each, I checked whether the top pick matched the stated
taste and whether the ranking made intuitive sense.

I also ran the two starter pytest tests (sorting by score, non-empty explanation)
and both pass. What surprised me most was how quickly the filter bubble appeared —
with only a +2 genre weight and 15 songs, the top results already collapsed onto a
single genre, which is exactly the kind of bias real recommenders are criticized for.

---

## 8. Future Work

- **Genre similarity instead of exact match**, so `pop` and `indie pop` count as
  partially related rather than unrelated.
- **A diversity rule** that penalizes returning too many songs of the same genre,
  to pop the filter bubble.
- **More features** (tempo, valence, danceability) and richer profiles, plus a
  larger, more balanced catalog.
- **Embedding-based similarity** (like the semantic search idea from the RAG
  lesson) so songs are compared by learned "vibe" rather than exact labels.

---

## 9. Personal Reflection

The biggest thing I learned is that a "recommender" doesn't need machine learning
to feel like one — a simple weighted scoring rule over a few attributes already
produces convincing, explainable results. The surprising part was watching bias
emerge on its own: I didn't design a filter bubble, but weighting genre highest
created one immediately, which made the Week 6 lessons about bias-as-a-system-
property concrete. AI help was useful for reasoning through the scoring design and
the closeness formula, but I had to double-check the ranking behavior myself by
reading the actual output rather than trusting that it "looked right." It changed
how I think about apps like Spotify: the recommendations that feel magical are also
quietly deciding what you'll never be shown.
