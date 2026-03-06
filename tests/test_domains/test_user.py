"""Tests for user domain."""

from unittest.mock import MagicMock

from spotify_client.domains.user import User
from tests.conftest import (
    make_raw_track,
    make_raw_album,
    make_raw_artist,
    make_raw_show,
    make_raw_user_profile,
    make_paginated_response,
)


class TestUser:
    def test_get_profile_current(self, mock_sp: MagicMock):
        mock_sp.current_user.return_value = make_raw_user_profile()
        user = User(mock_sp)
        result = user.get_profile()
        assert result["id"] == "testuser"
        mock_sp.current_user.assert_called_once()

    def test_get_profile_other(self, mock_sp: MagicMock):
        mock_sp.user.return_value = make_raw_user_profile("other")
        user = User(mock_sp)
        result = user.get_profile("other")
        assert result["id"] == "other"
        mock_sp.user.assert_called_once_with("other")

    def test_get_saved_tracks(self, mock_sp: MagicMock):
        mock_sp.current_user_saved_tracks.return_value = make_paginated_response(
            [{"track": make_raw_track("t1")}, {"track": make_raw_track("t2")}]
        )
        user = User(mock_sp)
        result = user.get_saved_tracks()
        assert len(result) == 2
        assert result[0]["id"] == "t1"

    def test_save_tracks(self, mock_sp: MagicMock):
        user = User(mock_sp)
        user.save_tracks(["t1", "t2"])
        mock_sp.current_user_saved_tracks_add.assert_called_once_with(["t1", "t2"])

    def test_remove_saved_tracks(self, mock_sp: MagicMock):
        user = User(mock_sp)
        user.remove_saved_tracks(["t1"])
        mock_sp.current_user_saved_tracks_delete.assert_called_once_with(["t1"])

    def test_check_saved_tracks(self, mock_sp: MagicMock):
        mock_sp.current_user_saved_tracks_contains.return_value = [True, False]
        user = User(mock_sp)
        result = user.check_saved_tracks(["t1", "t2"])
        assert result == [True, False]

    def test_get_saved_albums(self, mock_sp: MagicMock):
        mock_sp.current_user_saved_albums.return_value = make_paginated_response(
            [{"album": make_raw_album("a1")}]
        )
        user = User(mock_sp)
        result = user.get_saved_albums()
        assert len(result) == 1

    def test_get_saved_shows(self, mock_sp: MagicMock):
        mock_sp.current_user_saved_shows.return_value = make_paginated_response(
            [{"show": make_raw_show("s1")}]
        )
        user = User(mock_sp)
        result = user.get_saved_shows()
        assert len(result) == 1

    def test_get_top_tracks(self, mock_sp: MagicMock):
        mock_sp.current_user_top_tracks.return_value = {
            "items": [make_raw_track("t1")]
        }
        user = User(mock_sp)
        result = user.get_top_tracks(time_range="short_term")
        assert len(result) == 1
        mock_sp.current_user_top_tracks.assert_called_once_with(limit=20, time_range="short_term")

    def test_get_top_artists(self, mock_sp: MagicMock):
        mock_sp.current_user_top_artists.return_value = {
            "items": [make_raw_artist("a1")]
        }
        user = User(mock_sp)
        result = user.get_top_artists()
        assert len(result) == 1

    def test_get_recently_played(self, mock_sp: MagicMock):
        mock_sp.current_user_recently_played.return_value = {
            "items": [{"track": make_raw_track("t1"), "played_at": "2024-01-01T12:00:00Z"}]
        }
        user = User(mock_sp)
        result = user.get_recently_played()
        assert len(result) == 1
        assert result[0]["played_at"] == "2024-01-01T12:00:00Z"

    def test_get_followed_artists(self, mock_sp: MagicMock):
        mock_sp.current_user_followed_artists.return_value = {
            "artists": {
                "items": [make_raw_artist("a1")],
                "cursors": {"after": None},
            }
        }
        user = User(mock_sp)
        result = user.get_followed_artists()
        assert len(result) == 1
