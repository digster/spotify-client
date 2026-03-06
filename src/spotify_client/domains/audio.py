"""Audio features and analysis operations."""

import spotipy

from spotify_client.helpers import batch_ids, clean_audio_features, retry_on_rate_limit


class Audio:
    """Methods for fetching audio features and analysis."""

    def __init__(self, sp: spotipy.Spotify) -> None:
        self._sp = sp

    @retry_on_rate_limit
    def get_features(self, track_id: str) -> dict:
        """Get audio features for a single track."""
        raw = self._sp.audio_features([track_id])
        if raw and raw[0]:
            return clean_audio_features(raw[0])
        return {}

    @retry_on_rate_limit
    def get_features_many(self, track_ids: list[str]) -> list[dict]:
        """Get audio features for multiple tracks (handles batching for >100 IDs)."""
        results = []
        for batch in batch_ids(track_ids, batch_size=100):
            raw = self._sp.audio_features(batch)
            results.extend(clean_audio_features(f) for f in (raw or []) if f)
        return results

    @retry_on_rate_limit
    def get_analysis(self, track_id: str) -> dict:
        """Get detailed audio analysis for a track.

        Returns the raw analysis — it's too complex for meaningful cleaning.
        """
        return self._sp.audio_analysis(track_id)
