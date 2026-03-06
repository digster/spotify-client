"""Domain classes for Spotify resource types."""

from spotify_client.domains.albums import Albums
from spotify_client.domains.artists import Artists
from spotify_client.domains.audio import Audio
from spotify_client.domains.audiobooks import Audiobooks
from spotify_client.domains.episodes import Episodes
from spotify_client.domains.playlists import Playlists
from spotify_client.domains.recommendations import Recommendations
from spotify_client.domains.search import Search
from spotify_client.domains.shows import Shows
from spotify_client.domains.tracks import Tracks
from spotify_client.domains.user import User

__all__ = [
    "Albums",
    "Artists",
    "Audio",
    "Audiobooks",
    "Episodes",
    "Playlists",
    "Recommendations",
    "Search",
    "Shows",
    "Tracks",
    "User",
]
