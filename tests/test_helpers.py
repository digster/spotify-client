"""Tests for helpers module — response cleaning, pagination, batching."""

import time
from unittest.mock import MagicMock, patch

import pytest
import spotipy

from spotify_client.helpers import (
    _ms_to_duration,
    batch_ids,
    clean_album,
    clean_artist,
    clean_audio_features,
    clean_audiobook,
    clean_chapter,
    clean_episode,
    clean_playlist,
    clean_show,
    clean_track,
    clean_user_profile,
    paginate_offset,
    retry_on_rate_limit,
)
from spotify_client.exceptions import (
    AuthenticationError,
    InvalidRequestError,
    NotFoundError,
    RateLimitError,
)
from tests.conftest import (
    make_raw_album,
    make_raw_artist,
    make_raw_audio_features,
    make_raw_audiobook,
    make_raw_chapter,
    make_raw_episode,
    make_raw_playlist,
    make_raw_show,
    make_raw_track,
    make_raw_user_profile,
)


class TestMsToDuration:
    def test_standard(self):
        assert _ms_to_duration(354947) == "5:54"

    def test_zero(self):
        assert _ms_to_duration(0) == "0:00"

    def test_under_minute(self):
        assert _ms_to_duration(45000) == "0:45"

    def test_exact_minute(self):
        assert _ms_to_duration(60000) == "1:00"

    def test_long_duration(self):
        assert _ms_to_duration(3600000) == "60:00"


class TestBatchIds:
    def test_small_list(self):
        ids = ["a", "b", "c"]
        assert batch_ids(ids) == [["a", "b", "c"]]

    def test_exact_batch_size(self):
        ids = [str(i) for i in range(50)]
        batches = batch_ids(ids)
        assert len(batches) == 1
        assert len(batches[0]) == 50

    def test_multiple_batches(self):
        ids = [str(i) for i in range(120)]
        batches = batch_ids(ids)
        assert len(batches) == 3
        assert len(batches[0]) == 50
        assert len(batches[1]) == 50
        assert len(batches[2]) == 20

    def test_empty_list(self):
        assert batch_ids([]) == []

    def test_custom_batch_size(self):
        ids = [str(i) for i in range(10)]
        batches = batch_ids(ids, batch_size=3)
        assert len(batches) == 4


class TestCleanTrack:
    def test_basic(self):
        raw = make_raw_track()
        result = clean_track(raw)
        assert result["id"] == "track1"
        assert result["name"] == "Test Track"
        assert result["artists"] == ["Test Artist"]
        assert result["album"] == "Test Album"
        assert result["duration_str"] == "3:20"
        assert result["url"] == "https://open.spotify.com/track/track1"

    def test_empty_input(self):
        assert clean_track({}) == {}
        assert clean_track(None) == {}


class TestCleanAlbum:
    def test_basic(self):
        raw = make_raw_album()
        result = clean_album(raw)
        assert result["id"] == "album1"
        assert result["name"] == "Test Album"
        assert result["artists"] == ["Test Artist"]
        assert result["release_date"] == "2024-01-15"
        assert result["total_tracks"] == 12
        assert result["image_url"] == "https://i.scdn.co/image/test"

    def test_empty_input(self):
        assert clean_album({}) == {}


class TestCleanArtist:
    def test_basic(self):
        raw = make_raw_artist()
        result = clean_artist(raw)
        assert result["id"] == "artist1"
        assert result["name"] == "Test Artist"
        assert result["genres"] == ["rock", "alternative"]
        assert result["followers"] == 1000000

    def test_empty_input(self):
        assert clean_artist({}) == {}


class TestCleanAudioFeatures:
    def test_basic(self):
        raw = make_raw_audio_features()
        result = clean_audio_features(raw)
        assert result["id"] == "track1"
        assert result["danceability"] == 0.7
        assert result["energy"] == 0.8
        assert result["tempo"] == 120.0
        assert result["duration_str"] == "3:20"

    def test_empty_input(self):
        assert clean_audio_features({}) == {}


class TestCleanPlaylist:
    def test_basic(self):
        raw = make_raw_playlist()
        result = clean_playlist(raw)
        assert result["id"] == "playlist1"
        assert result["owner"] == "testuser"
        assert result["total_tracks"] == 50

    def test_empty_input(self):
        assert clean_playlist({}) == {}


class TestCleanUserProfile:
    def test_basic(self):
        raw = make_raw_user_profile()
        result = clean_user_profile(raw)
        assert result["id"] == "testuser"
        assert result["display_name"] == "Test User"
        assert result["followers"] == 42
        assert result["product"] == "premium"

    def test_empty_input(self):
        assert clean_user_profile({}) == {}


class TestCleanShow:
    def test_basic(self):
        raw = make_raw_show()
        result = clean_show(raw)
        assert result["id"] == "show1"
        assert result["name"] == "Test Podcast"
        assert result["publisher"] == "Test Publisher"
        assert result["total_episodes"] == 100

    def test_empty_input(self):
        assert clean_show({}) == {}


class TestCleanEpisode:
    def test_basic(self):
        raw = make_raw_episode()
        result = clean_episode(raw)
        assert result["id"] == "episode1"
        assert result["name"] == "Test Episode"
        assert result["duration_str"] == "60:00"
        assert result["show_name"] == "Test Podcast"

    def test_empty_input(self):
        assert clean_episode({}) == {}


class TestCleanAudiobook:
    def test_basic(self):
        raw = make_raw_audiobook()
        result = clean_audiobook(raw)
        assert result["id"] == "audiobook1"
        assert result["authors"] == ["Test Author"]
        assert result["narrators"] == ["Test Narrator"]
        assert result["total_chapters"] == 20

    def test_empty_input(self):
        assert clean_audiobook({}) == {}


class TestCleanChapter:
    def test_basic(self):
        raw = make_raw_chapter()
        result = clean_chapter(raw)
        assert result["id"] == "chapter1"
        assert result["duration_str"] == "30:00"
        assert result["chapter_number"] == 0

    def test_empty_input(self):
        assert clean_chapter({}) == {}


class TestPaginateOffset:
    def test_single_page(self):
        sp = MagicMock()
        page = {"items": [{"id": "1"}, {"id": "2"}], "next": None}
        result = paginate_offset(sp, page)
        assert len(result) == 2
        sp.next.assert_not_called()

    def test_multiple_pages(self):
        sp = MagicMock()
        page1 = {"items": [{"id": "1"}], "next": "http://next"}
        page2 = {"items": [{"id": "2"}], "next": None}
        sp.next.return_value = page2
        result = paginate_offset(sp, page1)
        assert len(result) == 2

    def test_respects_limit(self):
        sp = MagicMock()
        page = {"items": [{"id": str(i)} for i in range(10)], "next": "http://next"}
        result = paginate_offset(sp, page, limit=5)
        assert len(result) == 5


class TestRetryOnRateLimit:
    @patch("spotify_client.helpers.time.sleep")
    def test_retries_on_429(self, mock_sleep):
        call_count = 0

        @retry_on_rate_limit
        def flaky_func():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                exc = spotipy.SpotifyException(429, "", "rate limited")
                exc.headers = {"Retry-After": "1"}
                raise exc
            return "success"

        result = flaky_func()
        assert result == "success"
        assert call_count == 2
        mock_sleep.assert_called_once_with(1)

    def test_raises_auth_error_on_401(self):
        @retry_on_rate_limit
        def unauthorized():
            raise spotipy.SpotifyException(401, "", "unauthorized")

        with pytest.raises(AuthenticationError):
            unauthorized()

    def test_raises_not_found_on_404(self):
        @retry_on_rate_limit
        def not_found():
            raise spotipy.SpotifyException(404, "", "not found")

        with pytest.raises(NotFoundError):
            not_found()

    def test_raises_invalid_request_on_400(self):
        @retry_on_rate_limit
        def bad_request():
            raise spotipy.SpotifyException(400, "", "bad request")

        with pytest.raises(InvalidRequestError):
            bad_request()

    @patch("spotify_client.helpers.time.sleep")
    def test_raises_rate_limit_after_max_retries(self, mock_sleep):
        @retry_on_rate_limit
        def always_rate_limited():
            exc = spotipy.SpotifyException(429, "", "rate limited")
            exc.headers = {"Retry-After": "1"}
            raise exc

        with pytest.raises(RateLimitError):
            always_rate_limited()
