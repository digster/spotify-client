# Architecture

## Overview

spotify-client is a Python data access layer for the Spotify Web API, built on `spotipy`. It exposes a **facade pattern** (`SpotifyClient`) that delegates to domain-specific classes, plus a Click-based CLI with full feature parity.

## Key Design Decisions

### Facade Pattern (`client.py`)
`SpotifyClient` is the single entry point. It creates a `spotipy.Spotify` instance via the auth module and injects it into domain classes. This means:
- Consumers never import domain classes directly
- Auth complexity is hidden behind `user_auth=True/False`
- The `_UserAuthGuard` proxy raises `UserScopeRequiredError` on any access to `client.user` when not authenticated

### Domain Separation (`domains/`)
Each Spotify resource type has its own domain class. All domains:
- Receive a `spotipy.Spotify` instance in `__init__`
- Use `@retry_on_rate_limit` decorator on every public method
- Return **clean dicts** via `helpers.clean_*` functions
- Handle batching internally (e.g., splitting 120 IDs into batches of 50)

### Response Cleaning (`helpers.py`)
Raw Spotify API responses are verbose. `clean_*` functions:
- Flatten nested structures (e.g., `track.album.name` → `album`)
- Add computed fields (`duration_str`, `url`)
- Drop unused metadata
- Return `{}` for `None`/empty input (safe chaining)

### Two Auth Flows (`auth.py`)
- **Client Credentials**: Machine-to-machine, no user context. Used for public data (search, track info, etc.)
- **Authorization Code**: Opens browser for OAuth, caches token at `~/.spotify-client/.cache`. Required for user library, playlists, etc.

### Error Hierarchy (`exceptions.py`)
```
SpotifyClientError (base)
├── AuthenticationError     → HTTP 401, missing creds
├── NotFoundError           → HTTP 404
├── RateLimitError          → HTTP 429 after max retries
├── InvalidRequestError     → HTTP 400
└── UserScopeRequiredError  → method needs user_auth=True
```

### CLI Architecture (`cli/`)
- Click group with global flags (`--user-auth`, `--limit`, `--compact`)
- `SpotifyClient` is created once in the root group and stored in `ctx.obj`
- Each subcommand file defines a Click group (e.g., `track`, `album`)
- All output is JSON via `_output()` helper

## Data Flow

```
CLI Command → Click parses args → SpotifyClient.{domain}.{method}()
                                        ↓
                                  spotipy.Spotify.{api_call}()
                                        ↓
                                  @retry_on_rate_limit handles 429
                                        ↓
                                  clean_{type}() normalizes response
                                        ↓
                                  JSON output to stdout
```

## Key Files

| File | Purpose |
|------|---------|
| `src/spotify_client/client.py` | Facade — start here to understand the API |
| `src/spotify_client/helpers.py` | Core utilities — cleaning, pagination, rate limiting |
| `src/spotify_client/auth.py` | Auth flows — Client Credentials vs Authorization Code |
| `src/spotify_client/cli/__init__.py` | CLI entry point — global flags, subcommand registration |
| `tests/conftest.py` | Mock data factories — used by all tests |

## Testing Strategy

- All tests use **mocked spotipy** — no real API calls
- `conftest.py` provides factory functions for raw Spotify responses
- Domain tests verify: correct spotipy method called, response cleaned properly, batching works
- CLI tests use Click's `CliRunner` with mocked `SpotifyClient`
- Coverage target: 80% (currently ~88%)
