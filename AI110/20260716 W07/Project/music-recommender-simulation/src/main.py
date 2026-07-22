"""
Command line runner for the Music Recommender Simulation.

Phase 4 stress test: runs several deliberately different listener profiles
through the recommender so we can compare behavior and look for bias.
"""

from recommender import load_songs, recommend_songs


# Three deliberately different listener profiles
PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
}


def run_profile(name: str, user_prefs: dict, songs: list) -> None:
    print("=" * 60)
    print(f"Profile: {name}")
    print(f"  prefs: {user_prefs}")
    print("-" * 60)

    recommendations = recommend_songs(user_prefs, songs, k=5)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  {rank}. {song['title']:22s} ({song['genre']}/{song['mood']})  "
              f"score={score:.2f}")
        print(f"       because: {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, prefs in PROFILES.items():
        run_profile(name, prefs, songs)


if __name__ == "__main__":
    main()
