"""Custom exception hierarchy for spotify-client."""


class SpotifyClientError(Exception):
    """Base exception for all spotify-client errors."""


class AuthenticationError(SpotifyClientError):
    """Raised on 401 responses or missing credentials."""


class NotFoundError(SpotifyClientError):
    """Raised when a requested resource is not found (404)."""


class RateLimitError(SpotifyClientError):
    """Raised when rate limit is exceeded and retries are exhausted (429)."""


class InvalidRequestError(SpotifyClientError):
    """Raised on 400 responses or bad parameters."""


class UserScopeRequiredError(SpotifyClientError):
    """Raised when a method requires user authentication but client credentials were used."""

    def __init__(self, method_name: str = ""):
        msg = "This method requires user authentication. Use SpotifyClient(user_auth=True)."
        if method_name:
            msg = f"'{method_name}' requires user authentication. Use SpotifyClient(user_auth=True)."
        super().__init__(msg)
