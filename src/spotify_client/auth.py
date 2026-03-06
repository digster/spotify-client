"""Authentication: Client Credentials and Authorization Code flows."""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

from spotify_client.config import (
    CACHE_DIR,
    CACHE_PATH,
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI,
    USER_SCOPE_STRING,
)
from spotify_client.exceptions import AuthenticationError


def get_client(user_auth: bool = False) -> spotipy.Spotify:
    """Create and return a spotipy.Spotify instance with the appropriate auth flow.

    Args:
        user_auth: If True, use Authorization Code flow (opens browser for OAuth).
                   If False (default), use Client Credentials flow.
    """
    if not CLIENT_ID or not CLIENT_SECRET:
        raise AuthenticationError(
            "SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set. "
            "See .env.example for details."
        )

    if user_auth:
        return _get_user_client()
    return _get_app_client()


def _get_app_client() -> spotipy.Spotify:
    """Create a client using Client Credentials flow (no user context)."""
    auth_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    return spotipy.Spotify(auth_manager=auth_manager)


def _get_user_client() -> spotipy.Spotify:
    """Create a client using Authorization Code flow (full user access)."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=USER_SCOPE_STRING,
        cache_path=str(CACHE_PATH),
    )
    return spotipy.Spotify(auth_manager=auth_manager)
