"""Utilities: response cleaning, pagination, rate limiting, and batching."""

import functools
import logging
import time
from typing import Any, Callable

import spotipy

from spotify_client.config import DEFAULT_LIMIT, MAX_IDS_PER_REQUEST, MAX_RETRIES
from spotify_client.exceptions import (
    AuthenticationError,
    InvalidRequestError,
    NotFoundError,
    RateLimitError,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Rate limit retry decorator
# ---------------------------------------------------------------------------

def retry_on_rate_limit(func: Callable) -> Callable:
    """Decorator that retries on HTTP 429 (rate limit), respecting Retry-After header."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        for attempt in range(MAX_RETRIES + 1):
            try:
                return func(*args, **kwargs)
            except spotipy.SpotifyException as exc:
                _handle_spotify_exception(exc, attempt)
    return wrapper


def _handle_spotify_exception(exc: spotipy.SpotifyException, attempt: int) -> None:
    """Handle spotipy exceptions, raising our custom types or retrying on 429."""
    status = exc.http_status

    if status == 429:
        if attempt >= MAX_RETRIES:
            raise RateLimitError(f"Rate limited after {MAX_RETRIES} retries") from exc
        retry_after = int(exc.headers.get("Retry-After", 1)) if exc.headers else 1
        logger.warning("Rate limited. Retrying in %ds (attempt %d/%d)", retry_after, attempt + 1, MAX_RETRIES)
        time.sleep(retry_after)
        return  # Allow retry

    if status == 401:
        raise AuthenticationError(str(exc)) from exc
    if status == 404:
        raise NotFoundError(str(exc)) from exc
    if status == 400:
        raise InvalidRequestError(str(exc)) from exc

    raise exc


# ---------------------------------------------------------------------------
# Pagination helpers
# ---------------------------------------------------------------------------

def paginate_offset(sp: spotipy.Spotify, first_page: dict, limit: int = DEFAULT_LIMIT) -> list[dict]:
    """Collect all items from an offset-paginated Spotify response."""
    items = list(first_page.get("items", []))
    while first_page.get("next"):
        first_page = sp.next(first_page)
        items.extend(first_page.get("items", []))
        if limit and len(items) >= limit:
            return items[:limit]
    return items


def paginate_cursor(sp: spotipy.Spotify, first_page: dict, limit: int = DEFAULT_LIMIT) -> list[dict]:
    """Collect all items from a cursor-paginated Spotify response (e.g., followed artists)."""
    container = first_page.get("artists", first_page)
    items = list(container.get("items", []))
    while container.get("cursors") and container["cursors"].get("after"):
        # For cursor pagination, we use sp.next on the container
        next_page = sp.next(container)
        container = next_page.get("artists", next_page)
        items.extend(container.get("items", []))
        if limit and len(items) >= limit:
            return items[:limit]
    return items


# ---------------------------------------------------------------------------
# Batch helper
# ---------------------------------------------------------------------------

def batch_ids(ids: list[str], batch_size: int = MAX_IDS_PER_REQUEST) -> list[list[str]]:
    """Split a list of IDs into batches of the given size."""
    return [ids[i:i + batch_size] for i in range(0, len(ids), batch_size)]


# ---------------------------------------------------------------------------
# Response cleaning helpers
# ---------------------------------------------------------------------------

def _ms_to_duration(ms: int) -> str:
    """Convert milliseconds to human-readable duration string (e.g., '5:54')."""
    total_seconds = ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:02d}"


def _spotify_url(resource_type: str, resource_id: str) -> str:
    """Build a Spotify open URL."""
    return f"https://open.spotify.com/{resource_type}/{resource_id}"


def _extract_artist_names(artists: list[dict]) -> list[str]:
    """Extract artist names from a list of artist objects."""
    return [a["name"] for a in (artists or [])]


def _extract_image_url(images: list[dict] | None) -> str | None:
    """Extract the first (largest) image URL."""
    if images:
        return images[0].get("url")
    return None


def clean_track(track: dict) -> dict:
    """Clean a raw Spotify track object into a concise dict."""
    if not track:
        return {}
    album = track.get("album", {})
    return {
        "id": track["id"],
        "name": track["name"],
        "artists": _extract_artist_names(track.get("artists", [])),
        "album": album.get("name", ""),
        "album_id": album.get("id", ""),
        "duration_ms": track.get("duration_ms", 0),
        "duration_str": _ms_to_duration(track.get("duration_ms", 0)),
        "popularity": track.get("popularity", 0),
        "explicit": track.get("explicit", False),
        "track_number": track.get("track_number", 0),
        "disc_number": track.get("disc_number", 0),
        "uri": track.get("uri", ""),
        "url": _spotify_url("track", track["id"]),
    }


def clean_album(album: dict) -> dict:
    """Clean a raw Spotify album object into a concise dict."""
    if not album:
        return {}
    return {
        "id": album["id"],
        "name": album["name"],
        "artists": _extract_artist_names(album.get("artists", [])),
        "release_date": album.get("release_date", ""),
        "total_tracks": album.get("total_tracks", 0),
        "album_type": album.get("album_type", ""),
        "image_url": _extract_image_url(album.get("images")),
        "uri": album.get("uri", ""),
        "url": _spotify_url("album", album["id"]),
    }


def clean_artist(artist: dict) -> dict:
    """Clean a raw Spotify artist object into a concise dict."""
    if not artist:
        return {}
    return {
        "id": artist["id"],
        "name": artist["name"],
        "genres": artist.get("genres", []),
        "popularity": artist.get("popularity", 0),
        "followers": artist.get("followers", {}).get("total", 0),
        "image_url": _extract_image_url(artist.get("images")),
        "uri": artist.get("uri", ""),
        "url": _spotify_url("artist", artist["id"]),
    }


def clean_audio_features(features: dict) -> dict:
    """Clean a raw Spotify audio features object."""
    if not features:
        return {}
    keys = [
        "id", "danceability", "energy", "key", "loudness", "mode",
        "speechiness", "acousticness", "instrumentalness", "liveness",
        "valence", "tempo", "duration_ms", "time_signature",
    ]
    result = {k: features.get(k) for k in keys}
    result["duration_str"] = _ms_to_duration(features.get("duration_ms", 0))
    return result


def clean_playlist(playlist: dict) -> dict:
    """Clean a raw Spotify playlist object."""
    if not playlist:
        return {}
    owner = playlist.get("owner", {})
    return {
        "id": playlist["id"],
        "name": playlist["name"],
        "description": playlist.get("description", ""),
        "owner": owner.get("display_name", owner.get("id", "")),
        "public": playlist.get("public"),
        "collaborative": playlist.get("collaborative", False),
        "total_tracks": playlist.get("tracks", {}).get("total", 0),
        "image_url": _extract_image_url(playlist.get("images")),
        "uri": playlist.get("uri", ""),
        "url": _spotify_url("playlist", playlist["id"]),
    }


def clean_user_profile(user: dict) -> dict:
    """Clean a raw Spotify user profile object."""
    if not user:
        return {}
    return {
        "id": user.get("id", ""),
        "display_name": user.get("display_name", ""),
        "email": user.get("email"),
        "followers": user.get("followers", {}).get("total", 0),
        "image_url": _extract_image_url(user.get("images")),
        "country": user.get("country"),
        "product": user.get("product"),
        "uri": user.get("uri", ""),
        "url": _spotify_url("user", user.get("id", "")),
    }


def clean_show(show: dict) -> dict:
    """Clean a raw Spotify show/podcast object."""
    if not show:
        return {}
    return {
        "id": show["id"],
        "name": show["name"],
        "publisher": show.get("publisher", ""),
        "description": show.get("description", ""),
        "total_episodes": show.get("total_episodes", 0),
        "languages": show.get("languages", []),
        "explicit": show.get("explicit", False),
        "image_url": _extract_image_url(show.get("images")),
        "uri": show.get("uri", ""),
        "url": _spotify_url("show", show["id"]),
    }


def clean_episode(episode: dict) -> dict:
    """Clean a raw Spotify episode object."""
    if not episode:
        return {}
    return {
        "id": episode["id"],
        "name": episode["name"],
        "description": episode.get("description", ""),
        "duration_ms": episode.get("duration_ms", 0),
        "duration_str": _ms_to_duration(episode.get("duration_ms", 0)),
        "release_date": episode.get("release_date", ""),
        "show_name": episode.get("show", {}).get("name", ""),
        "explicit": episode.get("explicit", False),
        "image_url": _extract_image_url(episode.get("images")),
        "uri": episode.get("uri", ""),
        "url": _spotify_url("episode", episode["id"]),
    }


def clean_audiobook(audiobook: dict) -> dict:
    """Clean a raw Spotify audiobook object."""
    if not audiobook:
        return {}
    return {
        "id": audiobook["id"],
        "name": audiobook["name"],
        "authors": [a.get("name", "") for a in audiobook.get("authors", [])],
        "narrators": [n.get("name", "") for n in audiobook.get("narrators", [])],
        "publisher": audiobook.get("publisher", ""),
        "description": audiobook.get("description", ""),
        "total_chapters": audiobook.get("total_chapters", 0),
        "languages": audiobook.get("languages", []),
        "explicit": audiobook.get("explicit", False),
        "image_url": _extract_image_url(audiobook.get("images")),
        "uri": audiobook.get("uri", ""),
        "url": _spotify_url("audiobook", audiobook["id"]),
    }


def clean_chapter(chapter: dict) -> dict:
    """Clean a raw Spotify audiobook chapter object."""
    if not chapter:
        return {}
    return {
        "id": chapter["id"],
        "name": chapter["name"],
        "description": chapter.get("description", ""),
        "chapter_number": chapter.get("chapter_number", 0),
        "duration_ms": chapter.get("duration_ms", 0),
        "duration_str": _ms_to_duration(chapter.get("duration_ms", 0)),
        "uri": chapter.get("uri", ""),
        "url": _spotify_url("chapter", chapter["id"]),
    }
