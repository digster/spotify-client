"""Playlist operations."""

import spotipy

from spotify_client.config import DEFAULT_LIMIT
from spotify_client.helpers import (
    clean_playlist,
    clean_track,
    paginate_offset,
    retry_on_rate_limit,
)


class Playlists:
    """Methods for playlist operations. Write operations require user auth."""

    def __init__(self, sp: spotipy.Spotify) -> None:
        self._sp = sp

    @retry_on_rate_limit
    def get(self, playlist_id: str) -> dict:
        """Get a playlist by ID or URI."""
        raw = self._sp.playlist(playlist_id)
        return clean_playlist(raw)

    @retry_on_rate_limit
    def get_tracks(self, playlist_id: str, limit: int = DEFAULT_LIMIT) -> list[dict]:
        """Get tracks from a playlist."""
        first_page = self._sp.playlist_tracks(playlist_id, limit=min(limit, 100))
        items = paginate_offset(self._sp, first_page, limit=limit)
        return [clean_track(item["track"]) for item in items if item and item.get("track")]

    @retry_on_rate_limit
    def get_user_playlists(self, user_id: str | None = None, limit: int = DEFAULT_LIMIT) -> list[dict]:
        """Get playlists for a user. If no user_id, returns current user's playlists."""
        if user_id:
            first_page = self._sp.user_playlists(user_id, limit=min(limit, 50))
        else:
            first_page = self._sp.current_user_playlists(limit=min(limit, 50))
        items = paginate_offset(self._sp, first_page, limit=limit)
        return [clean_playlist(p) for p in items if p]

    @retry_on_rate_limit
    def create(
        self,
        name: str,
        description: str = "",
        public: bool = True,
    ) -> dict:
        """Create a new playlist for the current user."""
        user = self._sp.current_user()
        raw = self._sp.user_playlist_create(
            user=user["id"],
            name=name,
            public=public,
            description=description,
        )
        return clean_playlist(raw)

    @retry_on_rate_limit
    def add_tracks(self, playlist_id: str, track_uris: list[str]) -> None:
        """Add tracks to a playlist."""
        self._sp.playlist_add_items(playlist_id, track_uris)

    @retry_on_rate_limit
    def remove_tracks(self, playlist_id: str, track_uris: list[str]) -> None:
        """Remove tracks from a playlist."""
        self._sp.playlist_remove_all_occurrences_of_items(playlist_id, track_uris)

    @retry_on_rate_limit
    def update_details(
        self,
        playlist_id: str,
        name: str | None = None,
        description: str | None = None,
        public: bool | None = None,
    ) -> None:
        """Update playlist name, description, or visibility."""
        self._sp.playlist_change_details(
            playlist_id, name=name, description=description, public=public
        )
