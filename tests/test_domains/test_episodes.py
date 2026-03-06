"""Tests for episodes domain."""

from unittest.mock import MagicMock

from spotify_client.domains.episodes import Episodes
from tests.conftest import make_raw_episode


class TestEpisodes:
    def test_get(self, mock_sp: MagicMock):
        mock_sp.episode.return_value = make_raw_episode()
        episodes = Episodes(mock_sp)
        result = episodes.get("episode1")
        assert result["id"] == "episode1"
        assert result["name"] == "Test Episode"

    def test_get_many(self, mock_sp: MagicMock):
        mock_sp.episodes.return_value = {
            "episodes": [make_raw_episode("e1"), make_raw_episode("e2")]
        }
        episodes = Episodes(mock_sp)
        result = episodes.get_many(["e1", "e2"])
        assert len(result) == 2
