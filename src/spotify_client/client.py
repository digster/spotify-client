"""SpotifyClient facade — single entry point for all Spotify operations."""

import spotipy

from spotify_client.auth import get_client
from spotify_client.domains import (
    Albums,
    Artists,
    Audio,
    Audiobooks,
    Episodes,
    Playlists,
    Recommendations,
    Search,
    Shows,
    Tracks,
    User,
)
from spotify_client.exceptions import UserScopeRequiredError


class SpotifyClient:
    """Facade for Spotify API operations.

    Usage:
        client = SpotifyClient()                    # Client Credentials (public data)
        client = SpotifyClient(user_auth=True)      # Authorization Code (user data)

        client.tracks.get("track_id")
        client.search.search_tracks("bohemian rhapsody")
        client.user.get_saved_tracks()              # Requires user_auth=True
    """

    def __init__(self, user_auth: bool = False) -> None:
        self._user_auth = user_auth
        self._sp: spotipy.Spotify = get_client(user_auth=user_auth)

        # Initialize all domain classes with the spotipy instance
        self.tracks = Tracks(self._sp)
        self.albums = Albums(self._sp)
        self.artists = Artists(self._sp)
        self.audio = Audio(self._sp)
        self.search = Search(self._sp)
        self.recommendations = Recommendations(self._sp)
        self.shows = Shows(self._sp)
        self.episodes = Episodes(self._sp)
        self.audiobooks = Audiobooks(self._sp)

        # User-scoped domains — lazy guard for auth requirement
        if user_auth:
            self.user = User(self._sp)
            self.playlists = Playlists(self._sp)
        else:
            self.user = _UserAuthGuard()  # type: ignore[assignment]
            self.playlists = Playlists(self._sp)  # Read operations work without user auth

    @property
    def is_user_authenticated(self) -> bool:
        """Check if this client was initialized with user authentication."""
        return self._user_auth


class _UserAuthGuard:
    """Proxy that raises UserScopeRequiredError on any attribute access."""

    def __getattr__(self, name: str) -> None:
        raise UserScopeRequiredError(name)
