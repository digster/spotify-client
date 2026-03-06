"""Tests for shows domain."""

from unittest.mock import MagicMock

from spotify_client.domains.shows import Shows
from tests.conftest import make_raw_show, make_raw_episode, make_paginated_response


class TestShows:
    def test_get(self, mock_sp: MagicMock):
        mock_sp.show.return_value = make_raw_show()
        shows = Shows(mock_sp)
        result = shows.get("show1")
        assert result["id"] == "show1"
        assert result["name"] == "Test Podcast"

    def test_get_many(self, mock_sp: MagicMock):
        mock_sp.shows.return_value = {
            "shows": [make_raw_show("s1"), make_raw_show("s2")]
        }
        shows = Shows(mock_sp)
        result = shows.get_many(["s1", "s2"])
        assert len(result) == 2

    def test_get_episodes(self, mock_sp: MagicMock):
        mock_sp.show_episodes.return_value = make_paginated_response(
            [make_raw_episode("e1"), make_raw_episode("e2")]
        )
        shows = Shows(mock_sp)
        result = shows.get_episodes("show1")
        assert len(result) == 2
