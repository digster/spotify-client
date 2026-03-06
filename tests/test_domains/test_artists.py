"""Tests for artists domain."""

from unittest.mock import MagicMock

from spotify_client.domains.artists import Artists
from tests.conftest import make_raw_artist, make_raw_track, make_raw_album, make_paginated_response


class TestArtists:
    def test_get(self, mock_sp: MagicMock):
        mock_sp.artist.return_value = make_raw_artist()
        artists = Artists(mock_sp)
        result = artists.get("artist1")
        assert result["id"] == "artist1"
        assert result["genres"] == ["rock", "alternative"]

    def test_get_many(self, mock_sp: MagicMock):
        mock_sp.artists.return_value = {
            "artists": [make_raw_artist("a1"), make_raw_artist("a2")]
        }
        artists = Artists(mock_sp)
        result = artists.get_many(["a1", "a2"])
        assert len(result) == 2

    def test_get_top_tracks(self, mock_sp: MagicMock):
        mock_sp.artist_top_tracks.return_value = {
            "tracks": [make_raw_track("t1"), make_raw_track("t2")]
        }
        artists = Artists(mock_sp)
        result = artists.get_top_tracks("artist1")
        assert len(result) == 2

    def test_get_albums(self, mock_sp: MagicMock):
        mock_sp.artist_albums.return_value = make_paginated_response(
            [make_raw_album("al1")]
        )
        artists = Artists(mock_sp)
        result = artists.get_albums("artist1")
        assert len(result) == 1

    def test_get_related(self, mock_sp: MagicMock):
        mock_sp.artist_related_artists.return_value = {
            "artists": [make_raw_artist("r1")]
        }
        artists = Artists(mock_sp)
        result = artists.get_related("artist1")
        assert len(result) == 1
        assert result[0]["id"] == "r1"
