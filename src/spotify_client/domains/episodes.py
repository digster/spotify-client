"""Episode operations."""

import spotipy

from spotify_client.helpers import batch_ids, clean_episode, retry_on_rate_limit


class Episodes:
    """Methods for fetching episode data."""

    def __init__(self, sp: spotipy.Spotify) -> None:
        self._sp = sp

    @retry_on_rate_limit
    def get(self, episode_id: str, market: str | None = None) -> dict:
        """Get a single episode by ID or URI."""
        raw = self._sp.episode(episode_id, market=market)
        return clean_episode(raw)

    @retry_on_rate_limit
    def get_many(self, episode_ids: list[str], market: str | None = None) -> list[dict]:
        """Get multiple episodes (handles batching for >50 IDs)."""
        results = []
        for batch in batch_ids(episode_ids):
            raw = self._sp.episodes(batch, market=market)
            results.extend(clean_episode(e) for e in raw.get("episodes", []) if e)
        return results
