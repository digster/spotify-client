"""Track operations."""

import spotipy

from spotify_client.helpers import batch_ids, clean_track, retry_on_rate_limit


class Tracks:
    """Methods for fetching track data."""

    def __init__(self, sp: spotipy.Spotify) -> None:
        self._sp = sp

    @retry_on_rate_limit
    def get(self, track_id: str) -> dict:
        """Get a single track by ID or URI."""
        raw = self._sp.track(track_id)
        return clean_track(raw)

    @retry_on_rate_limit
    def get_many(self, track_ids: list[str]) -> list[dict]:
        """Get multiple tracks (handles batching for >50 IDs)."""
        results = []
        for batch in batch_ids(track_ids):
            raw = self._sp.tracks(batch)
            results.extend(clean_track(t) for t in raw.get("tracks", []) if t)
        return results
