"""Tests for SpotifyClient facade."""

from unittest.mock import patch, MagicMock

import pytest

from spotify_client.client import SpotifyClient
from spotify_client.exceptions import UserScopeRequiredError
from spotify_client.domains.tracks import Tracks
from spotify_client.domains.user import User


class TestSpotifyClient:
    @patch("spotify_client.client.get_client")
    def test_creates_all_domain_instances(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        client = SpotifyClient()
        assert hasattr(client, "tracks")
        assert hasattr(client, "albums")
        assert hasattr(client, "artists")
        assert hasattr(client, "audio")
        assert hasattr(client, "search")
        assert hasattr(client, "recommendations")
        assert hasattr(client, "shows")
        assert hasattr(client, "episodes")
        assert hasattr(client, "audiobooks")
        assert hasattr(client, "playlists")

    @patch("spotify_client.client.get_client")
    def test_user_guard_without_user_auth(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        client = SpotifyClient(user_auth=False)
        with pytest.raises(UserScopeRequiredError):
            client.user.get_profile()

    @patch("spotify_client.client.get_client")
    def test_user_domain_with_user_auth(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        client = SpotifyClient(user_auth=True)
        assert isinstance(client.user, User)

    @patch("spotify_client.client.get_client")
    def test_is_user_authenticated(self, mock_get_client):
        mock_get_client.return_value = MagicMock()
        client = SpotifyClient(user_auth=False)
        assert client.is_user_authenticated is False

        client_auth = SpotifyClient(user_auth=True)
        assert client_auth.is_user_authenticated is True
