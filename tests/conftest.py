"""Shared fixtures and mock data factories for tests."""

from unittest.mock import MagicMock

import pytest
import spotipy


@pytest.fixture
def mock_sp() -> MagicMock:
    """Create a mock spotipy.Spotify instance."""
    return MagicMock(spec=spotipy.Spotify)


# ---------------------------------------------------------------------------
# Raw Spotify API response factories — simulate what spotipy returns
# ---------------------------------------------------------------------------

def make_raw_track(
    track_id: str = "track1",
    name: str = "Test Track",
    artist_name: str = "Test Artist",
    album_name: str = "Test Album",
    duration_ms: int = 200000,
    popularity: int = 75,
) -> dict:
    """Factory for raw Spotify track objects."""
    return {
        "id": track_id,
        "name": name,
        "artists": [{"name": artist_name}],
        "album": {"id": "album1", "name": album_name, "images": []},
        "duration_ms": duration_ms,
        "popularity": popularity,
        "explicit": False,
        "track_number": 1,
        "disc_number": 1,
        "uri": f"spotify:track:{track_id}",
    }


def make_raw_album(
    album_id: str = "album1",
    name: str = "Test Album",
    artist_name: str = "Test Artist",
    total_tracks: int = 12,
) -> dict:
    """Factory for raw Spotify album objects."""
    return {
        "id": album_id,
        "name": name,
        "artists": [{"name": artist_name}],
        "release_date": "2024-01-15",
        "total_tracks": total_tracks,
        "album_type": "album",
        "images": [{"url": "https://i.scdn.co/image/test"}],
        "uri": f"spotify:album:{album_id}",
    }


def make_raw_artist(
    artist_id: str = "artist1",
    name: str = "Test Artist",
    genres: list | None = None,
    popularity: int = 80,
    followers: int = 1000000,
) -> dict:
    """Factory for raw Spotify artist objects."""
    return {
        "id": artist_id,
        "name": name,
        "genres": genres or ["rock", "alternative"],
        "popularity": popularity,
        "followers": {"total": followers},
        "images": [{"url": "https://i.scdn.co/image/artist"}],
        "uri": f"spotify:artist:{artist_id}",
    }


def make_raw_playlist(
    playlist_id: str = "playlist1",
    name: str = "Test Playlist",
    owner_name: str = "testuser",
    total_tracks: int = 50,
) -> dict:
    """Factory for raw Spotify playlist objects."""
    return {
        "id": playlist_id,
        "name": name,
        "description": "A test playlist",
        "owner": {"id": "testuser", "display_name": owner_name},
        "public": True,
        "collaborative": False,
        "tracks": {"total": total_tracks},
        "images": [{"url": "https://i.scdn.co/image/playlist"}],
        "uri": f"spotify:playlist:{playlist_id}",
    }


def make_raw_audio_features(
    track_id: str = "track1",
    danceability: float = 0.7,
    energy: float = 0.8,
    tempo: float = 120.0,
) -> dict:
    """Factory for raw Spotify audio features objects."""
    return {
        "id": track_id,
        "danceability": danceability,
        "energy": energy,
        "key": 5,
        "loudness": -5.5,
        "mode": 1,
        "speechiness": 0.05,
        "acousticness": 0.1,
        "instrumentalness": 0.0,
        "liveness": 0.15,
        "valence": 0.6,
        "tempo": tempo,
        "duration_ms": 200000,
        "time_signature": 4,
    }


def make_raw_user_profile(
    user_id: str = "testuser",
    display_name: str = "Test User",
) -> dict:
    """Factory for raw Spotify user profile objects."""
    return {
        "id": user_id,
        "display_name": display_name,
        "email": "test@example.com",
        "followers": {"total": 42},
        "images": [{"url": "https://i.scdn.co/image/user"}],
        "country": "US",
        "product": "premium",
        "uri": f"spotify:user:{user_id}",
    }


def make_raw_show(
    show_id: str = "show1",
    name: str = "Test Podcast",
    publisher: str = "Test Publisher",
) -> dict:
    """Factory for raw Spotify show objects."""
    return {
        "id": show_id,
        "name": name,
        "publisher": publisher,
        "description": "A test podcast",
        "total_episodes": 100,
        "languages": ["en"],
        "explicit": False,
        "images": [{"url": "https://i.scdn.co/image/show"}],
        "uri": f"spotify:show:{show_id}",
    }


def make_raw_episode(
    episode_id: str = "episode1",
    name: str = "Test Episode",
    show_name: str = "Test Podcast",
    duration_ms: int = 3600000,
) -> dict:
    """Factory for raw Spotify episode objects."""
    return {
        "id": episode_id,
        "name": name,
        "description": "A test episode",
        "duration_ms": duration_ms,
        "release_date": "2024-06-01",
        "show": {"name": show_name},
        "explicit": False,
        "images": [{"url": "https://i.scdn.co/image/episode"}],
        "uri": f"spotify:episode:{episode_id}",
    }


def make_raw_audiobook(
    audiobook_id: str = "audiobook1",
    name: str = "Test Audiobook",
) -> dict:
    """Factory for raw Spotify audiobook objects."""
    return {
        "id": audiobook_id,
        "name": name,
        "authors": [{"name": "Test Author"}],
        "narrators": [{"name": "Test Narrator"}],
        "publisher": "Test Publisher",
        "description": "A test audiobook",
        "total_chapters": 20,
        "languages": ["en"],
        "explicit": False,
        "images": [{"url": "https://i.scdn.co/image/audiobook"}],
        "uri": f"spotify:audiobook:{audiobook_id}",
    }


def make_raw_chapter(
    chapter_id: str = "chapter1",
    name: str = "Chapter 1",
    chapter_number: int = 0,
    duration_ms: int = 1800000,
) -> dict:
    """Factory for raw Spotify chapter objects."""
    return {
        "id": chapter_id,
        "name": name,
        "description": "First chapter",
        "chapter_number": chapter_number,
        "duration_ms": duration_ms,
        "uri": f"spotify:chapter:{chapter_id}",
    }


def make_paginated_response(items: list, total: int | None = None, next_url: str | None = None) -> dict:
    """Wrap items in a paginated Spotify response envelope."""
    return {
        "items": items,
        "total": total or len(items),
        "limit": len(items),
        "offset": 0,
        "next": next_url,
        "previous": None,
    }
