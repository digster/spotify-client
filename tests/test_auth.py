"""Tests for auth module."""

from unittest.mock import patch, MagicMock

import pytest

from spotify_client.auth import get_client
from spotify_client.exceptions import AuthenticationError


class TestGetClient:
    @patch("spotify_client.auth.CLIENT_ID", "test_id")
    @patch("spotify_client.auth.CLIENT_SECRET", "test_secret")
    @patch("spotify_client.auth.SpotifyClientCredentials")
    @patch("spotify_client.auth.spotipy.Spotify")
    def test_client_credentials_flow(self, mock_spotify, mock_creds):
        client = get_client(user_auth=False)
        mock_creds.assert_called_once_with(
            client_id="test_id",
            client_secret="test_secret",
        )
        mock_spotify.assert_called_once()

    @patch("spotify_client.auth.CLIENT_ID", "test_id")
    @patch("spotify_client.auth.CLIENT_SECRET", "test_secret")
    @patch("spotify_client.auth.CACHE_DIR")
    @patch("spotify_client.auth.SpotifyOAuth")
    @patch("spotify_client.auth.spotipy.Spotify")
    def test_authorization_code_flow(self, mock_spotify, mock_oauth, mock_cache_dir):
        client = get_client(user_auth=True)
        mock_oauth.assert_called_once()
        mock_spotify.assert_called_once()

    @patch("spotify_client.auth.CLIENT_ID", "")
    @patch("spotify_client.auth.CLIENT_SECRET", "")
    def test_missing_credentials_raises_error(self):
        with pytest.raises(AuthenticationError, match="SPOTIFY_CLIENT_ID"):
            get_client()

    @patch("spotify_client.auth.CLIENT_ID", "test_id")
    @patch("spotify_client.auth.CLIENT_SECRET", "")
    def test_missing_secret_raises_error(self):
        with pytest.raises(AuthenticationError, match="SPOTIFY_CLIENT_ID"):
            get_client()
