"""CLI integration tests using Click's CliRunner."""

import json
from unittest.mock import patch, MagicMock

from click.testing import CliRunner

from spotify_client.cli import cli
from tests.conftest import make_raw_track, make_raw_album, make_raw_artist, make_raw_show


@patch("spotify_client.cli.SpotifyClient")
class TestCLI:
    """Test CLI commands by mocking SpotifyClient."""

    def _run(self, mock_client_cls, args: list[str]) -> tuple:
        """Helper: run CLI command and return (result, parsed_json)."""
        runner = CliRunner()
        result = runner.invoke(cli, args)
        parsed = None
        if result.output.strip():
            try:
                parsed = json.loads(result.output)
            except json.JSONDecodeError:
                parsed = result.output.strip()
        return result, parsed

    def test_help(self, mock_client_cls):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Spotify CLI" in result.output

    def test_track_get(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.tracks.get.return_value = {"id": "t1", "name": "Track"}
        result, data = self._run(mock_client_cls, ["track", "get", "t1"])
        assert result.exit_code == 0
        assert data["id"] == "t1"

    def test_track_get_many(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.tracks.get_many.return_value = [{"id": "t1"}, {"id": "t2"}]
        result, data = self._run(mock_client_cls, ["track", "get-many", "t1", "t2"])
        assert result.exit_code == 0
        assert len(data) == 2

    def test_album_get(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.albums.get.return_value = {"id": "a1", "name": "Album"}
        result, data = self._run(mock_client_cls, ["album", "get", "a1"])
        assert result.exit_code == 0
        assert data["id"] == "a1"

    def test_album_new_releases(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.albums.get_new_releases.return_value = [{"id": "nr1"}]
        result, data = self._run(mock_client_cls, ["album", "new-releases", "--country", "US"])
        assert result.exit_code == 0
        assert len(data) == 1

    def test_artist_get(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.artists.get.return_value = {"id": "ar1", "name": "Artist"}
        result, data = self._run(mock_client_cls, ["artist", "get", "ar1"])
        assert result.exit_code == 0
        assert data["name"] == "Artist"

    def test_artist_top_tracks(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.artists.get_top_tracks.return_value = [{"id": "t1"}]
        result, data = self._run(mock_client_cls, ["artist", "top-tracks", "ar1"])
        assert result.exit_code == 0
        assert len(data) == 1

    def test_search_query(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.search.search.return_value = {"tracks": [{"id": "t1"}]}
        result, data = self._run(mock_client_cls, ["search", "query", "test query"])
        assert result.exit_code == 0
        assert "tracks" in data

    def test_search_tracks_subcommand(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.search.search_tracks.return_value = [{"id": "t1"}]
        result, data = self._run(mock_client_cls, ["search", "tracks", "test"])
        assert result.exit_code == 0
        assert len(data) == 1

    def test_audio_features(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.audio.get_features.return_value = {"id": "t1", "energy": 0.8}
        result, data = self._run(mock_client_cls, ["audio", "features", "t1"])
        assert result.exit_code == 0
        assert data["energy"] == 0.8

    def test_recommend_genres(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.recommendations.get_available_genres.return_value = ["pop", "rock"]
        result, data = self._run(mock_client_cls, ["recommend", "genres"])
        assert result.exit_code == 0
        assert "pop" in data

    def test_recommend_by_genre(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.recommendations.get_recommendations.return_value = [{"id": "t1"}]
        result, data = self._run(mock_client_cls, ["recommend", "--seed-genres", "pop,rock"])
        assert result.exit_code == 0
        assert len(data) == 1

    def test_show_get(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.shows.get.return_value = {"id": "s1", "name": "Podcast"}
        result, data = self._run(mock_client_cls, ["show", "get", "s1"])
        assert result.exit_code == 0
        assert data["name"] == "Podcast"

    def test_episode_get(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.episodes.get.return_value = {"id": "e1", "name": "Episode"}
        result, data = self._run(mock_client_cls, ["episode", "get", "e1"])
        assert result.exit_code == 0
        assert data["name"] == "Episode"

    def test_audiobook_get(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.audiobooks.get.return_value = {"id": "ab1", "name": "Book"}
        result, data = self._run(mock_client_cls, ["audiobook", "get", "ab1"])
        assert result.exit_code == 0
        assert data["name"] == "Book"

    def test_playlist_get(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.playlists.get.return_value = {"id": "p1", "name": "Playlist"}
        result, data = self._run(mock_client_cls, ["playlist", "get", "p1"])
        assert result.exit_code == 0
        assert data["name"] == "Playlist"

    def test_playlist_create(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.playlists.create.return_value = {"id": "p1", "name": "My Playlist"}
        result, data = self._run(mock_client_cls, ["playlist", "create", "My Playlist", "--desc", "desc"])
        assert result.exit_code == 0
        assert data["name"] == "My Playlist"

    def test_compact_output(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.tracks.get.return_value = {"id": "t1"}
        runner = CliRunner()
        result = runner.invoke(cli, ["-c", "track", "get", "t1"])
        assert result.exit_code == 0
        assert "\n" not in result.output.strip()  # Compact = single line

    def test_limit_flag(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.search.search_tracks.return_value = []
        runner = CliRunner()
        result = runner.invoke(cli, ["-l", "5", "search", "tracks", "test"])
        assert result.exit_code == 0
        mock_client.search.search_tracks.assert_called_once_with("test", limit=5)

    def test_user_profile(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.user.get_profile.return_value = {"id": "user1", "display_name": "User"}
        result, data = self._run(mock_client_cls, ["user", "profile"])
        assert result.exit_code == 0
        assert data["id"] == "user1"
