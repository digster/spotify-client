"""Tests for playlists domain."""

from unittest.mock import MagicMock

from spotify_client.domains.playlists import Playlists
from tests.conftest import make_raw_playlist, make_raw_track, make_paginated_response


class TestPlaylists:
    def test_get(self, mock_sp: MagicMock):
        mock_sp.playlist.return_value = make_raw_playlist()
        playlists = Playlists(mock_sp)
        result = playlists.get("playlist1")
        assert result["id"] == "playlist1"
        assert result["name"] == "Test Playlist"

    def test_get_tracks(self, mock_sp: MagicMock):
        mock_sp.playlist_tracks.return_value = make_paginated_response(
            [{"track": make_raw_track("t1")}, {"track": make_raw_track("t2")}]
        )
        playlists = Playlists(mock_sp)
        result = playlists.get_tracks("playlist1")
        assert len(result) == 2

    def test_get_user_playlists_current(self, mock_sp: MagicMock):
        mock_sp.current_user_playlists.return_value = make_paginated_response(
            [make_raw_playlist("p1")]
        )
        playlists = Playlists(mock_sp)
        result = playlists.get_user_playlists()
        assert len(result) == 1
        mock_sp.current_user_playlists.assert_called_once()

    def test_get_user_playlists_other(self, mock_sp: MagicMock):
        mock_sp.user_playlists.return_value = make_paginated_response(
            [make_raw_playlist("p1")]
        )
        playlists = Playlists(mock_sp)
        result = playlists.get_user_playlists(user_id="otheruser")
        assert len(result) == 1
        mock_sp.user_playlists.assert_called_once()

    def test_create(self, mock_sp: MagicMock):
        mock_sp.current_user.return_value = {"id": "testuser"}
        mock_sp.user_playlist_create.return_value = make_raw_playlist("new1", "New Playlist")
        playlists = Playlists(mock_sp)
        result = playlists.create("New Playlist", description="desc", public=False)
        assert result["id"] == "new1"
        mock_sp.user_playlist_create.assert_called_once_with(
            user="testuser", name="New Playlist", public=False, description="desc"
        )

    def test_add_tracks(self, mock_sp: MagicMock):
        playlists = Playlists(mock_sp)
        playlists.add_tracks("p1", ["spotify:track:t1", "spotify:track:t2"])
        mock_sp.playlist_add_items.assert_called_once_with("p1", ["spotify:track:t1", "spotify:track:t2"])

    def test_remove_tracks(self, mock_sp: MagicMock):
        playlists = Playlists(mock_sp)
        playlists.remove_tracks("p1", ["spotify:track:t1"])
        mock_sp.playlist_remove_all_occurrences_of_items.assert_called_once()

    def test_update_details(self, mock_sp: MagicMock):
        playlists = Playlists(mock_sp)
        playlists.update_details("p1", name="Updated", public=False)
        mock_sp.playlist_change_details.assert_called_once_with(
            "p1", name="Updated", description=None, public=False
        )
