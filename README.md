# spotify-client

Python utility for interfacing with Spotify data programmatically. Primary consumers are LLMs (via Claude Code skill) and developers. Not a music player — a data access layer with a CLI for quick terminal queries.

## Setup

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for project management
- Spotify Developer credentials ([get them here](https://developer.spotify.com/dashboard))

### Installation

```bash
# Clone and install
git clone <repo-url>
cd spotify-client
uv sync

# Configure credentials
cp .env.example .env
# Edit .env with your Spotify Client ID and Secret
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SPOTIFY_CLIENT_ID` | Yes | — | Spotify app client ID |
| `SPOTIFY_CLIENT_SECRET` | Yes | — | Spotify app client secret |
| `SPOTIFY_REDIRECT_URI` | No | `http://localhost:8888/callback` | OAuth redirect URI |

## Usage

### As a Python Library

```python
from spotify_client import SpotifyClient

# Public data (Client Credentials flow)
client = SpotifyClient()
track = client.tracks.get("4uLU6hMCjMI75M1A2tKUQC")
results = client.search.search_tracks("bohemian rhapsody")
features = client.audio.get_features("4uLU6hMCjMI75M1A2tKUQC")
genres = client.recommendations.get_available_genres()

# User data (Authorization Code flow — opens browser for OAuth)
client = SpotifyClient(user_auth=True)
saved = client.user.get_saved_tracks()
top = client.user.get_top_artists(time_range="short_term")
client.playlists.create("My Playlist", description="Created via API")
```

### CLI

All commands output JSON. Global flags: `--user-auth` / `-u`, `--limit N` / `-l`, `--compact` / `-c`.

```bash
# Tracks
spotify track get <id>
spotify track get-many <id1> <id2>

# Albums
spotify album get <id>
spotify album tracks <id>
spotify album new-releases --country US

# Artists
spotify artist get <id>
spotify artist top-tracks <id>
spotify artist albums <id> --include album,single
spotify artist related <id>

# Search
spotify search query "bohemian rhapsody"
spotify search tracks "queen"
spotify search albums "dark side of the moon"
spotify search artists "radiohead"
spotify search playlists "workout"
spotify search shows "podcast name"
spotify search episodes "episode title"
spotify search audiobooks "book title"

# Audio Features
spotify audio features <id>
spotify audio features-many <id1> <id2>
spotify audio analysis <id>

# Shows / Episodes / Audiobooks
spotify show get <id>
spotify show episodes <id>
spotify episode get <id>
spotify audiobook get <id>
spotify audiobook chapters <id>

# Recommendations
spotify recommend --seed-genres pop,rock
spotify recommend --seed-tracks <id> --target-energy 0.8
spotify recommend genres

# User (requires -u flag)
spotify -u user profile
spotify -u user saved-tracks
spotify -u user top-tracks --time-range short_term
spotify -u user recently-played

# Playlists
spotify playlist get <id>
spotify playlist tracks <id>
spotify -u playlist list
spotify -u playlist create "My Playlist" --desc "Description"
spotify -u playlist add-tracks <playlist_id> <track_uri1> <track_uri2>
```

## Development

```bash
# Run tests
uv run pytest -v

# Run with coverage
uv run pytest --cov=spotify_client --cov-report=term-missing

# Import check
uv run python -c "from spotify_client import SpotifyClient; print('OK')"

# CLI help
uv run spotify --help
```

## Project Structure

```
src/spotify_client/
├── __init__.py          # Version, re-exports
├── auth.py              # Client Credentials + Authorization Code flows
├── client.py            # SpotifyClient facade
├── config.py            # Env vars, constants, scopes
├── exceptions.py        # Custom exception hierarchy
├── helpers.py           # Pagination, rate limiting, response cleaning
├── cli/                 # Click-based CLI
│   ├── __init__.py      # Click group + global flags
│   ├── track.py         # track subcommands
│   ├── album.py         # album subcommands
│   ├── artist.py        # artist subcommands
│   ├── search.py        # search subcommands
│   ├── audio.py         # audio subcommands
│   ├── recommend.py     # recommendation subcommands
│   ├── show.py          # show/podcast subcommands
│   ├── episode.py       # episode subcommands
│   ├── audiobook.py     # audiobook subcommands
│   ├── user.py          # user subcommands
│   └── playlist.py      # playlist subcommands
└── domains/             # Domain classes (one per resource type)
    ├── tracks.py
    ├── albums.py
    ├── artists.py
    ├── audio.py
    ├── search.py
    ├── recommendations.py
    ├── shows.py
    ├── episodes.py
    ├── audiobooks.py
    ├── user.py
    └── playlists.py
```
