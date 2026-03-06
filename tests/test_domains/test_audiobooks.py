"""Tests for audiobooks domain."""

from unittest.mock import MagicMock

from spotify_client.domains.audiobooks import Audiobooks
from tests.conftest import make_raw_audiobook, make_raw_chapter, make_paginated_response


class TestAudiobooks:
    def test_get(self, mock_sp: MagicMock):
        mock_sp.get_audiobook.return_value = make_raw_audiobook()
        audiobooks = Audiobooks(mock_sp)
        result = audiobooks.get("audiobook1")
        assert result["id"] == "audiobook1"
        assert result["authors"] == ["Test Author"]

    def test_get_many(self, mock_sp: MagicMock):
        mock_sp.get_audiobooks.return_value = {
            "audiobooks": [make_raw_audiobook("ab1"), make_raw_audiobook("ab2")]
        }
        audiobooks = Audiobooks(mock_sp)
        result = audiobooks.get_many(["ab1", "ab2"])
        assert len(result) == 2

    def test_get_chapters(self, mock_sp: MagicMock):
        mock_sp.get_audiobook_chapters.return_value = make_paginated_response(
            [make_raw_chapter("ch1"), make_raw_chapter("ch2")]
        )
        audiobooks = Audiobooks(mock_sp)
        result = audiobooks.get_chapters("audiobook1")
        assert len(result) == 2
        assert result[0]["id"] == "ch1"
