# CLAUDE.md

## Project

spotify-client — Python data access layer for Spotify Web API with CLI.

## Quick Commands

```bash
uv run pytest -v                                    # Run tests
uv run pytest --cov=spotify_client                  # Coverage
uv run spotify --help                               # CLI help
uv run python -c "from spotify_client import SpotifyClient"  # Import check
```

## Key Conventions

- All domain methods return clean dicts (via `helpers.clean_*`), never raw API responses
- Every public domain method is decorated with `@retry_on_rate_limit`
- CLI outputs JSON only — use `--compact` for single-line output
- User-scoped operations require `SpotifyClient(user_auth=True)` or CLI `--user-auth` flag
- Test factories are in `tests/conftest.py` — use `make_raw_*()` for mock data
- Batch endpoints split IDs automatically (50 per request, 20 for albums, 100 for audio features)
