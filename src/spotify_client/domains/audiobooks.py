"""Audiobook operations."""

import spotipy

from spotify_client.config import DEFAULT_LIMIT
from spotify_client.helpers import (
    batch_ids,
    clean_audiobook,
    clean_chapter,
    paginate_offset,
    retry_on_rate_limit,
)


class Audiobooks:
    """Methods for fetching audiobook data."""

    def __init__(self, sp: spotipy.Spotify) -> None:
        self._sp = sp

    @retry_on_rate_limit
    def get(self, audiobook_id: str, market: str | None = None) -> dict:
        """Get a single audiobook by ID or URI."""
        raw = self._sp.get_audiobook(audiobook_id, market=market)
        return clean_audiobook(raw)

    @retry_on_rate_limit
    def get_many(self, audiobook_ids: list[str], market: str | None = None) -> list[dict]:
        """Get multiple audiobooks (handles batching for >50 IDs)."""
        results = []
        for batch in batch_ids(audiobook_ids):
            raw = self._sp.get_audiobooks(batch, market=market)
            results.extend(clean_audiobook(a) for a in raw.get("audiobooks", []) if a)
        return results

    @retry_on_rate_limit
    def get_chapters(self, audiobook_id: str, limit: int = DEFAULT_LIMIT, market: str | None = None) -> list[dict]:
        """Get chapters of an audiobook."""
        first_page = self._sp.get_audiobook_chapters(audiobook_id, limit=min(limit, 50), market=market)
        items = paginate_offset(self._sp, first_page, limit=limit)
        return [clean_chapter(c) for c in items if c]
