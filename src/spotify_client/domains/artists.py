"""Artist operations."""

import spotipy

from spotify_client.config import DEFAULT_LIMIT, DEFAULT_MARKET
from spotify_client.helpers import (
    batch_ids,
    clean_album,
    clean_artist,
    clean_track,
    paginate_offset,
    retry_on_rate_limit,
)


class Artists:
    """Methods for fetching artist data."""

    def __init__(self, sp: spotipy.Spotify) -> None:
        self._sp = sp

    @retry_on_rate_limit
    def get(self, artist_id: str) -> dict:
        """Get a single artist by ID or URI."""
        raw = self._sp.artist(artist_id)
        return clean_artist(raw)

    @retry_on_rate_limit
    def get_many(self, artist_ids: list[str]) -> list[dict]:
        """Get multiple artists (handles batching for >50 IDs)."""
        results = []
        for batch in batch_ids(artist_ids):
            raw = self._sp.artists(batch)
            results.extend(clean_artist(a) for a in raw.get("artists", []) if a)
        return results

    @retry_on_rate_limit
    def get_top_tracks(self, artist_id: str, market: str = DEFAULT_MARKET) -> list[dict]:
        """Get an artist's top tracks in a given market."""
        raw = self._sp.artist_top_tracks(artist_id, country=market)
        return [clean_track(t) for t in raw.get("tracks", []) if t]

    @retry_on_rate_limit
    def get_albums(
        self,
        artist_id: str,
        include_groups: str = "album,single",
        limit: int = DEFAULT_LIMIT,
    ) -> list[dict]:
        """Get an artist's albums."""
        first_page = self._sp.artist_albums(
            artist_id, album_type=include_groups, limit=min(limit, 50)
        )
        items = paginate_offset(self._sp, first_page, limit=limit)
        return [clean_album(a) for a in items if a]

    @retry_on_rate_limit
    def get_related(self, artist_id: str) -> list[dict]:
        """Get artists related to a given artist."""
        raw = self._sp.artist_related_artists(artist_id)
        return [clean_artist(a) for a in raw.get("artists", []) if a]
