"""User library and profile operations (requires user auth)."""

import spotipy

from spotify_client.config import DEFAULT_LIMIT
from spotify_client.helpers import (
    clean_album,
    clean_artist,
    clean_show,
    clean_track,
    clean_user_profile,
    paginate_cursor,
    paginate_offset,
    retry_on_rate_limit,
)


class User:
    """Methods for user-scoped operations. All require user authentication."""

    def __init__(self, sp: spotipy.Spotify) -> None:
        self._sp = sp

    # -- Profile --

    @retry_on_rate_limit
    def get_profile(self, user_id: str | None = None) -> dict:
        """Get user profile. If no user_id, returns current authenticated user."""
        if user_id:
            raw = self._sp.user(user_id)
        else:
            raw = self._sp.current_user()
        return clean_user_profile(raw)

    # -- Saved Tracks --

    @retry_on_rate_limit
    def get_saved_tracks(self, limit: int = DEFAULT_LIMIT) -> list[dict]:
        """Get current user's saved/liked tracks."""
        first_page = self._sp.current_user_saved_tracks(limit=min(limit, 50))
        items = paginate_offset(self._sp, first_page, limit=limit)
        return [clean_track(item["track"]) for item in items if item and item.get("track")]

    @retry_on_rate_limit
    def save_tracks(self, track_ids: list[str]) -> None:
        """Save tracks to the current user's library."""
        self._sp.current_user_saved_tracks_add(track_ids)

    @retry_on_rate_limit
    def remove_saved_tracks(self, track_ids: list[str]) -> None:
        """Remove tracks from the current user's library."""
        self._sp.current_user_saved_tracks_delete(track_ids)

    @retry_on_rate_limit
    def check_saved_tracks(self, track_ids: list[str]) -> list[bool]:
        """Check if tracks are in the current user's library."""
        return self._sp.current_user_saved_tracks_contains(track_ids)

    # -- Saved Albums --

    @retry_on_rate_limit
    def get_saved_albums(self, limit: int = DEFAULT_LIMIT) -> list[dict]:
        """Get current user's saved albums."""
        first_page = self._sp.current_user_saved_albums(limit=min(limit, 50))
        items = paginate_offset(self._sp, first_page, limit=limit)
        return [clean_album(item["album"]) for item in items if item and item.get("album")]

    @retry_on_rate_limit
    def save_albums(self, album_ids: list[str]) -> None:
        """Save albums to the current user's library."""
        self._sp.current_user_saved_albums_add(album_ids)

    @retry_on_rate_limit
    def remove_saved_albums(self, album_ids: list[str]) -> None:
        """Remove albums from the current user's library."""
        self._sp.current_user_saved_albums_delete(album_ids)

    # -- Saved Shows --

    @retry_on_rate_limit
    def get_saved_shows(self, limit: int = DEFAULT_LIMIT) -> list[dict]:
        """Get current user's saved shows/podcasts."""
        first_page = self._sp.current_user_saved_shows(limit=min(limit, 50))
        items = paginate_offset(self._sp, first_page, limit=limit)
        return [clean_show(item["show"]) for item in items if item and item.get("show")]

    @retry_on_rate_limit
    def save_shows(self, show_ids: list[str]) -> None:
        """Save shows to the current user's library."""
        self._sp.current_user_saved_shows_add(show_ids)

    @retry_on_rate_limit
    def remove_saved_shows(self, show_ids: list[str]) -> None:
        """Remove shows from the current user's library."""
        self._sp.current_user_saved_shows_delete(show_ids)

    # -- Following --

    @retry_on_rate_limit
    def get_followed_artists(self, limit: int = DEFAULT_LIMIT) -> list[dict]:
        """Get artists the current user follows."""
        first_page = self._sp.current_user_followed_artists(limit=min(limit, 50))
        items = paginate_cursor(self._sp, first_page, limit=limit)
        return [clean_artist(a) for a in items if a]

    @retry_on_rate_limit
    def follow_artists(self, artist_ids: list[str]) -> None:
        """Follow artists."""
        self._sp.user_follow_artists(artist_ids)

    @retry_on_rate_limit
    def unfollow_artists(self, artist_ids: list[str]) -> None:
        """Unfollow artists."""
        self._sp.user_unfollow_artists(artist_ids)

    # -- Top Items --

    @retry_on_rate_limit
    def get_top_tracks(self, limit: int = DEFAULT_LIMIT, time_range: str = "medium_term") -> list[dict]:
        """Get current user's top tracks.

        Args:
            time_range: 'short_term' (~4 weeks), 'medium_term' (~6 months), 'long_term' (years).
        """
        raw = self._sp.current_user_top_tracks(limit=min(limit, 50), time_range=time_range)
        return [clean_track(t) for t in raw.get("items", []) if t]

    @retry_on_rate_limit
    def get_top_artists(self, limit: int = DEFAULT_LIMIT, time_range: str = "medium_term") -> list[dict]:
        """Get current user's top artists."""
        raw = self._sp.current_user_top_artists(limit=min(limit, 50), time_range=time_range)
        return [clean_artist(a) for a in raw.get("items", []) if a]

    # -- Recently Played --

    @retry_on_rate_limit
    def get_recently_played(self, limit: int = DEFAULT_LIMIT) -> list[dict]:
        """Get current user's recently played tracks."""
        raw = self._sp.current_user_recently_played(limit=min(limit, 50))
        items = raw.get("items", [])
        results = []
        for item in items:
            track = clean_track(item.get("track", {}))
            if track:
                track["played_at"] = item.get("played_at", "")
                results.append(track)
        return results[:limit]
