"""Show/podcast operations."""

import spotipy

from spotify_client.config import DEFAULT_LIMIT
from spotify_client.helpers import (
    batch_ids,
    clean_episode,
    clean_show,
    paginate_offset,
    retry_on_rate_limit,
)


class Shows:
    """Methods for fetching show/podcast data."""

    def __init__(self, sp: spotipy.Spotify) -> None:
        self._sp = sp

    @retry_on_rate_limit
    def get(self, show_id: str, market: str | None = None) -> dict:
        """Get a single show by ID or URI."""
        raw = self._sp.show(show_id, market=market)
        return clean_show(raw)

    @retry_on_rate_limit
    def get_many(self, show_ids: list[str], market: str | None = None) -> list[dict]:
        """Get multiple shows (handles batching for >50 IDs)."""
        results = []
        for batch in batch_ids(show_ids):
            raw = self._sp.shows(batch, market=market)
            results.extend(clean_show(s) for s in raw.get("shows", []) if s)
        return results

    @retry_on_rate_limit
    def get_episodes(self, show_id: str, limit: int = DEFAULT_LIMIT, market: str | None = None) -> list[dict]:
        """Get episodes of a show."""
        first_page = self._sp.show_episodes(show_id, limit=min(limit, 50), market=market)
        items = paginate_offset(self._sp, first_page, limit=limit)
        return [clean_episode(e) for e in items if e]
