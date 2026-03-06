"""Tests for albums domain."""

from unittest.mock import MagicMock

from spotify_client.domains.albums import Albums
from tests.conftest import make_raw_album, make_raw_track, make_paginated_response


class TestAlbums:
    def test_get(self, mock_sp: MagicMock):
        mock_sp.album.return_value = make_raw_album()
        albums = Albums(mock_sp)
        result = albums.get("album1")
        assert result["id"] == "album1"
        assert result["name"] == "Test Album"

    def test_get_many(self, mock_sp: MagicMock):
        mock_sp.albums.return_value = {
            "albums": [make_raw_album("a1"), make_raw_album("a2")]
        }
        albums = Albums(mock_sp)
        result = albums.get_many(["a1", "a2"])
        assert len(result) == 2

    def test_get_tracks(self, mock_sp: MagicMock):
        mock_sp.album_tracks.return_value = make_paginated_response(
            [make_raw_track("t1"), make_raw_track("t2")]
        )
        albums = Albums(mock_sp)
        result = albums.get_tracks("album1")
        assert len(result) == 2
        assert result[0]["id"] == "t1"

    def test_get_new_releases(self, mock_sp: MagicMock):
        mock_sp.new_releases.return_value = {
            "albums": make_paginated_response([make_raw_album("new1")])
        }
        albums = Albums(mock_sp)
        result = albums.get_new_releases()
        assert len(result) == 1
        assert result[0]["id"] == "new1"
