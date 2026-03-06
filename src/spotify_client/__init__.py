"""spotify-client: Python utility for interfacing with Spotify data."""

__version__ = "0.1.0"

from spotify_client.client import SpotifyClient
from spotify_client.exceptions import (
    AuthenticationError,
    InvalidRequestError,
    NotFoundError,
    RateLimitError,
    SpotifyClientError,
    UserScopeRequiredError,
)

__all__ = [
    "SpotifyClient",
    "SpotifyClientError",
    "AuthenticationError",
    "NotFoundError",
    "RateLimitError",
    "InvalidRequestError",
    "UserScopeRequiredError",
]
