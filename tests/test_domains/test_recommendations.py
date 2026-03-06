"""Tests for recommendations domain."""

from unittest.mock import MagicMock

from spotify_client.domains.recommendations import Recommendations
from tests.conftest import make_raw_track


class TestRecommendations:
    def test_get_recommendations(self, mock_sp: MagicMock):
        mock_sp.recommendations.return_value = {
            "tracks": [make_raw_track("r1"), make_raw_track("r2")]
        }
        recs = Recommendations(mock_sp)
        result = recs.get_recommendations(seed_genres=["pop", "rock"])
        assert len(result) == 2
        mock_sp.recommendations.assert_called_once_with(
            seed_artists=None,
            seed_tracks=None,
            seed_genres=["pop", "rock"],
            limit=20,
        )

    def test_get_recommendations_with_tunables(self, mock_sp: MagicMock):
        mock_sp.recommendations.return_value = {"tracks": [make_raw_track()]}
        recs = Recommendations(mock_sp)
        result = recs.get_recommendations(
            seed_tracks=["t1"],
            target_energy=0.8,
            min_tempo=120,
        )
        assert len(result) == 1
        mock_sp.recommendations.assert_called_once_with(
            seed_artists=None,
            seed_tracks=["t1"],
            seed_genres=None,
            limit=20,
            target_energy=0.8,
            min_tempo=120,
        )

    def test_get_available_genres(self, mock_sp: MagicMock):
        mock_sp.recommendation_genre_seeds.return_value = {
            "genres": ["pop", "rock", "jazz"]
        }
        recs = Recommendations(mock_sp)
        result = recs.get_available_genres()
        assert result == ["pop", "rock", "jazz"]
