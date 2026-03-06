"""Tests for tracks domain."""

from unittest.mock import MagicMock

from spotify_client.domains.tracks import Tracks
from tests.conftest import make_raw_track


class TestTracks:
    def test_get(self, mock_sp: MagicMock):
        mock_sp.track.return_value = make_raw_track()
        tracks = Tracks(mock_sp)
        result = tracks.get("track1")
        assert result["id"] == "track1"
        assert result["name"] == "Test Track"
        mock_sp.track.assert_called_once_with("track1")

    def test_get_many(self, mock_sp: MagicMock):
        mock_sp.tracks.return_value = {
            "tracks": [make_raw_track("t1"), make_raw_track("t2")]
        }
        tracks = Tracks(mock_sp)
        result = tracks.get_many(["t1", "t2"])
        assert len(result) == 2
        assert result[0]["id"] == "t1"

    def test_get_many_batches(self, mock_sp: MagicMock):
        """Test that get_many splits large ID lists into batches."""
        ids = [f"t{i}" for i in range(60)]
        mock_sp.tracks.return_value = {"tracks": [make_raw_track(f"t{i}") for i in range(50)]}
        tracks = Tracks(mock_sp)
        tracks.get_many(ids)
        assert mock_sp.tracks.call_count == 2
