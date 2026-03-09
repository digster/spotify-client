# Spotify Data Access Skill

Query Spotify data using the spotify-client Python library.

## Quick Start

```bash
# Search
uv run spotify search tracks "bohemian rhapsody"
uv run spotify search artists "radiohead"
uv run spotify search albums "dark side of the moon"

# Get specific items
uv run spotify track get <track_id>
uv run spotify album get <album_id>
uv run spotify artist get <artist_id>
uv run spotify artist top-tracks <artist_id>

# Audio analysis
uv run spotify audio features <track_id>

# Recommendations
uv run spotify recommend --seed-genres pop,rock
uv run spotify recommend --seed-tracks <id> --target-energy 0.8
uv run spotify recommend genres

# Shows/Podcasts
uv run spotify show get <show_id>
uv run spotify show episodes <show_id>
uv run spotify episode get <episode_id>

# Audiobooks
uv run spotify audiobook get <audiobook_id>
uv run spotify audiobook chapters <audiobook_id>

# User data (requires -u flag for OAuth)
uv run spotify -u user profile
uv run spotify -u user saved-tracks
uv run spotify -u user top-tracks --time-range short_term
uv run spotify -u user recently-played
uv run spotify -u playlist list
```

## Flags

- `-u` / `--user-auth`: Enable OAuth user authentication (for personal data)
- `-l N` / `--limit N`: Max results (default 20)
- `-c` / `--compact`: Single-line JSON output

## Python API

```python
from spotify_client import SpotifyClient

client = SpotifyClient()
client.tracks.get("track_id")
client.search.search_tracks("query")
client.artists.get_top_tracks("artist_id")
client.audio.get_features("track_id")
client.recommendations.get_recommendations(seed_genres=["pop"])
```

## Requirements

Needs `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` in `.env`.
