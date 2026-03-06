"""Configuration: environment variables, constants, and OAuth scopes."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Spotify API credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback")

# Token cache location
CACHE_DIR = Path.home() / ".spotify-client"
CACHE_PATH = CACHE_DIR / ".cache"

# API defaults
DEFAULT_LIMIT = 20
DEFAULT_MARKET = "US"
MAX_IDS_PER_REQUEST = 50
MAX_RETRIES = 3

# All scopes needed for user-authenticated operations
USER_SCOPES = [
    "user-library-read",
    "user-library-modify",
    "user-read-recently-played",
    "user-top-read",
    "user-follow-read",
    "user-follow-modify",
    "playlist-read-private",
    "playlist-read-collaborative",
    "playlist-modify-public",
    "playlist-modify-private",
]

USER_SCOPE_STRING = " ".join(USER_SCOPES)
