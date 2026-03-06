"""Recommendation operations."""

from typing import Any

import spotipy

from spotify_client.config import DEFAULT_LIMIT
from spotify_client.helpers import clean_track, retry_on_rate_limit


class Recommendations:
    """Methods for fetching recommendations and genre seeds."""

    def __init__(self, sp: spotipy.Spotify) -> None:
        self._sp = sp

    @retry_on_rate_limit
    def get_recommendations(
        self,
        seed_artists: list[str] | None = None,
        seed_tracks: list[str] | None = None,
        seed_genres: list[str] | None = None,
        limit: int = DEFAULT_LIMIT,
        **kwargs: Any,
    ) -> list[dict]:
        """Get track recommendations based on seeds and tunable attributes.

        Args:
            seed_artists: List of artist IDs (max 5 total seeds).
            seed_tracks: List of track IDs (max 5 total seeds).
            seed_genres: List of genre names (max 5 total seeds).
            limit: Number of recommendations to return.
            **kwargs: Tunable attributes (e.g., target_energy=0.8, min_tempo=120).
        """
        raw = self._sp.recommendations(
            seed_artists=seed_artists,
            seed_tracks=seed_tracks,
            seed_genres=seed_genres,
            limit=min(limit, 100),
            **kwargs,
        )
        return [clean_track(t) for t in raw.get("tracks", []) if t]

    @retry_on_rate_limit
    def get_available_genres(self) -> list[str]:
        """Get a list of available genre seeds for recommendations."""
        raw = self._sp.recommendation_genre_seeds()
        return raw.get("genres", [])
