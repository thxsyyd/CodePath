"""
Music Recommender Simulation — core logic.

Provides two parallel implementations that share the same scoring idea:

1. Functional API (used by src/main.py):
     - load_songs(csv_path)      -> list of song dicts
     - score_song(user_prefs, song) -> (score, reasons)
     - recommend_songs(user_prefs, songs, k) -> [(song, score, explanation), ...]

2. Object-oriented API (used by tests/test_recommender.py):
     - Song, UserProfile dataclasses
     - Recommender.recommend(user, k)
     - Recommender.explain_recommendation(user, song)

Algorithm Recipe (content-based scoring):
  +2.0  exact genre match
  +1.0  exact mood match
  +2.0 * (1 - |target_energy - song_energy|)   energy closeness
  +0.5  acoustic preference matches (OOP profile only)
"""

import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


# ---------------------------------------------------------------------
# Data classes (used by the OOP API / tests)
# ---------------------------------------------------------------------

@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


# ---------------------------------------------------------------------
# Scoring weights (single source of truth for both APIs)
# ---------------------------------------------------------------------

GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 2.0
ACOUSTIC_WEIGHT = 0.5
ACOUSTIC_THRESHOLD = 0.6  # a song counts as "acoustic" above this value


# ---------------------------------------------------------------------
# Functional API (used by src/main.py)
# ---------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """
    Load songs from a CSV file into a list of dictionaries.

    Numeric columns are converted to float/int so we can do math on them.
    """
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Score a single song against the user's preferences.

    user_prefs keys (all optional): "genre", "mood", "energy"
    Returns (score, reasons) where reasons explains each point contribution.
    """
    score = 0.0
    reasons: List[str] = []

    # Genre match
    if user_prefs.get("genre") and song["genre"] == user_prefs["genre"]:
        score += GENRE_WEIGHT
        reasons.append(f"genre match ({song['genre']}) +{GENRE_WEIGHT}")

    # Mood match
    if user_prefs.get("mood") and song["mood"] == user_prefs["mood"]:
        score += MOOD_WEIGHT
        reasons.append(f"mood match ({song['mood']}) +{MOOD_WEIGHT}")

    # Energy closeness: reward songs whose energy is near the target
    if user_prefs.get("energy") is not None:
        gap = abs(user_prefs["energy"] - song["energy"])
        energy_points = ENERGY_WEIGHT * (1 - gap)
        score += energy_points
        reasons.append(
            f"energy close to {user_prefs['energy']:.2f} "
            f"(gap {gap:.2f}) +{energy_points:.2f}"
        )

    return score, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
) -> List[Tuple[Dict, float, str]]:
    """
    Score every song, then return the top k as (song, score, explanation).
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no strong matches"
        scored.append((song, score, explanation))

    # Sort by score descending
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]


# ---------------------------------------------------------------------
# OOP API (used by tests/test_recommender.py)
# ---------------------------------------------------------------------

class Recommender:
    """Object-oriented wrapper around the same scoring idea."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Score a Song against a UserProfile. Returns (score, reasons)."""
        score = 0.0
        reasons: List[str] = []

        if song.genre == user.favorite_genre:
            score += GENRE_WEIGHT
            reasons.append(f"genre match ({song.genre}) +{GENRE_WEIGHT}")

        if song.mood == user.favorite_mood:
            score += MOOD_WEIGHT
            reasons.append(f"mood match ({song.mood}) +{MOOD_WEIGHT}")

        gap = abs(user.target_energy - song.energy)
        energy_points = ENERGY_WEIGHT * (1 - gap)
        score += energy_points
        reasons.append(
            f"energy close to {user.target_energy:.2f} "
            f"(gap {gap:.2f}) +{energy_points:.2f}"
        )

        is_acoustic = song.acousticness >= ACOUSTIC_THRESHOLD
        if is_acoustic == user.likes_acoustic:
            score += ACOUSTIC_WEIGHT
            match_word = "acoustic" if is_acoustic else "non-acoustic"
            reasons.append(f"acoustic preference matches ({match_word}) +{ACOUSTIC_WEIGHT}")

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Songs, sorted by score descending."""
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was scored."""
        score, reasons = self._score(user, song)
        if not reasons:
            return f"{song.title}: no strong matches (score {score:.2f})"
        return f"{song.title} (score {score:.2f}): " + "; ".join(reasons)
