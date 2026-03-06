"""Album operations."""

import spotipy

from spotify_client.config import DEFAULT_LIMIT
from spotify_client.helpers import (
    batch_ids,
    clean_album,
    clean_track,
    paginate_offset,
    retry_on_rate_limit,
)


class Albums:
    """Methods for fetching album data."""

    def __init__(self, sp: spotipy.Spotify) -> None:
        self._sp = sp

    @retry_on_rate_limit
    def get(self, album_id: str) -> dict:
        """Get a single album by ID or URI."""
        raw = self._sp.album(album_id)
        return clean_album(raw)

    @retry_on_rate_limit
    def get_many(self, album_ids: list[str]) -> list[dict]:
        """Get multiple albums (handles batching for >20 IDs)."""
        results = []
        # Spotify albums endpoint accepts max 20 IDs
        for batch in batch_ids(album_ids, batch_size=20):
            raw = self._sp.albums(batch)
            results.extend(clean_album(a) for a in raw.get("albums", []) if a)
        return results

    @retry_on_rate_limit
    def get_tracks(self, album_id: str, limit: int = DEFAULT_LIMIT) -> list[dict]:
        """Get all tracks from an album."""
        first_page = self._sp.album_tracks(album_id, limit=min(limit, 50))
        items = paginate_offset(self._sp, first_page, limit=limit)
        return [clean_track(t) for t in items if t]

    @retry_on_rate_limit
    def get_new_releases(self, country: str | None = None, limit: int = DEFAULT_LIMIT) -> list[dict]:
        """Get new album releases."""
        raw = self._sp.new_releases(country=country, limit=min(limit, 50))
        albums_page = raw.get("albums", {})
        items = paginate_offset(self._sp, albums_page, limit=limit)
        return [clean_album(a) for a in items if a]
