"""Search operations."""

import spotipy

from spotify_client.config import DEFAULT_LIMIT
from spotify_client.helpers import (
    clean_album,
    clean_artist,
    clean_audiobook,
    clean_episode,
    clean_playlist,
    clean_show,
    clean_track,
    retry_on_rate_limit,
)

# Maps type names to their response keys and cleaner functions
_TYPE_MAP = {
    "track": ("tracks", clean_track),
    "album": ("albums", clean_album),
    "artist": ("artists", clean_artist),
    "playlist": ("playlists", clean_playlist),
    "show": ("shows", clean_show),
    "episode": ("episodes", clean_episode),
    "audiobook": ("audiobooks", clean_audiobook),
}


class Search:
    """Methods for searching Spotify content."""

    def __init__(self, sp: spotipy.Spotify) -> None:
        self._sp = sp

    @retry_on_rate_limit
    def search(
        self,
        query: str,
        types: str = "track",
        limit: int = DEFAULT_LIMIT,
        market: str | None = None,
    ) -> dict:
        """Search Spotify across one or more types.

        Args:
            query: Search query string.
            types: Comma-separated types (e.g., "track,album,artist").
            limit: Max results per type.
            market: ISO 3166-1 alpha-2 country code.

        Returns:
            Dict keyed by type (e.g., {"tracks": [...], "albums": [...]}).
        """
        raw = self._sp.search(q=query, type=types, limit=min(limit, 50), market=market)
        result = {}
        for type_name in types.split(","):
            type_name = type_name.strip()
            if type_name in _TYPE_MAP:
                key, cleaner = _TYPE_MAP[type_name]
                items = raw.get(key, {}).get("items", [])
                result[key] = [cleaner(item) for item in items if item]
        return result

    def search_tracks(self, query: str, limit: int = DEFAULT_LIMIT, market: str | None = None) -> list[dict]:
        """Search for tracks."""
        return self.search(query, types="track", limit=limit, market=market).get("tracks", [])

    def search_albums(self, query: str, limit: int = DEFAULT_LIMIT, market: str | None = None) -> list[dict]:
        """Search for albums."""
        return self.search(query, types="album", limit=limit, market=market).get("albums", [])

    def search_artists(self, query: str, limit: int = DEFAULT_LIMIT, market: str | None = None) -> list[dict]:
        """Search for artists."""
        return self.search(query, types="artist", limit=limit, market=market).get("artists", [])

    def search_playlists(self, query: str, limit: int = DEFAULT_LIMIT, market: str | None = None) -> list[dict]:
        """Search for playlists."""
        return self.search(query, types="playlist", limit=limit, market=market).get("playlists", [])

    def search_shows(self, query: str, limit: int = DEFAULT_LIMIT, market: str | None = None) -> list[dict]:
        """Search for shows/podcasts."""
        return self.search(query, types="show", limit=limit, market=market).get("shows", [])

    def search_episodes(self, query: str, limit: int = DEFAULT_LIMIT, market: str | None = None) -> list[dict]:
        """Search for episodes."""
        return self.search(query, types="episode", limit=limit, market=market).get("episodes", [])

    def search_audiobooks(self, query: str, limit: int = DEFAULT_LIMIT, market: str | None = None) -> list[dict]:
        """Search for audiobooks."""
        return self.search(query, types="audiobook", limit=limit, market=market).get("audiobooks", [])
