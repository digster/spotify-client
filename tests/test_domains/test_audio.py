"""Tests for audio domain."""

from unittest.mock import MagicMock

from spotify_client.domains.audio import Audio
from tests.conftest import make_raw_audio_features


class TestAudio:
    def test_get_features(self, mock_sp: MagicMock):
        mock_sp.audio_features.return_value = [make_raw_audio_features()]
        audio = Audio(mock_sp)
        result = audio.get_features("track1")
        assert result["id"] == "track1"
        assert result["danceability"] == 0.7

    def test_get_features_empty(self, mock_sp: MagicMock):
        mock_sp.audio_features.return_value = [None]
        audio = Audio(mock_sp)
        result = audio.get_features("track1")
        assert result == {}

    def test_get_features_many(self, mock_sp: MagicMock):
        mock_sp.audio_features.return_value = [
            make_raw_audio_features("t1"),
            make_raw_audio_features("t2"),
        ]
        audio = Audio(mock_sp)
        result = audio.get_features_many(["t1", "t2"])
        assert len(result) == 2

    def test_get_analysis(self, mock_sp: MagicMock):
        mock_sp.audio_analysis.return_value = {"meta": {}, "track": {}, "bars": []}
        audio = Audio(mock_sp)
        result = audio.get_analysis("track1")
        assert "meta" in result
