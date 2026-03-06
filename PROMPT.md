# Prompts

## 2026-03-06

Implement the full Spotify client project from an implementation plan. Includes:
- Python utility for interfacing with Spotify data (spotipy-based)
- Facade pattern with domain classes for tracks, albums, artists, audio, search, shows, episodes, audiobooks, recommendations, user, playlists
- Click-based CLI with JSON output and full feature parity
- Response cleaning/normalization layer
- Two auth flows (Client Credentials + Authorization Code)
- Custom exception hierarchy with rate limiting
- Full test suite with mock factories (118 tests, 88% coverage)
- Claude Code skill for LLM access
