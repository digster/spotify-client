"""Tests for search domain."""

from unittest.mock import MagicMock

from spotify_client.domains.search import Search
from tests.conftest import make_raw_track, make_raw_album, make_raw_artist


class TestSearch:
    def test_search_tracks(self, mock_sp: MagicMock):
        mock_sp.search.return_value = {
            "tracks": {"items": [make_raw_track()]}
        }
        search = Search(mock_sp)
        result = search.search_tracks("test query")
        assert len(result) == 1
        assert result[0]["name"] == "Test Track"

    def test_search_albums(self, mock_sp: MagicMock):
        mock_sp.search.return_value = {
            "albums": {"items": [make_raw_album()]}
        }
        search = Search(mock_sp)
        result = search.search_albums("test query")
        assert len(result) == 1

    def test_search_artists(self, mock_sp: MagicMock):
        mock_sp.search.return_value = {
            "artists": {"items": [make_raw_artist()]}
        }
        search = Search(mock_sp)
        result = search.search_artists("test query")
        assert len(result) == 1

    def test_multi_type_search(self, mock_sp: MagicMock):
        mock_sp.search.return_value = {
            "tracks": {"items": [make_raw_track()]},
            "albums": {"items": [make_raw_album()]},
        }
        search = Search(mock_sp)
        result = search.search("test", types="track,album")
        assert "tracks" in result
        assert "albums" in result

    def test_search_with_market(self, mock_sp: MagicMock):
        mock_sp.search.return_value = {"tracks": {"items": []}}
        search = Search(mock_sp)
        search.search_tracks("test", market="US")
        mock_sp.search.assert_called_once_with(q="test", type="track", limit=20, market="US")
