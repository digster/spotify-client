"""CLI: search subcommands."""

import click

from spotify_client.cli import _output


@click.group()
def search() -> None:
    """Search Spotify content.

    \b
    Examples:
      spotify search query "bohemian rhapsody"
      spotify search query --type track,album "queen"
      spotify search tracks "queen"
    """


@search.command("query")
@click.argument("query")
@click.option("--type", "search_type", default="track", help="Comma-separated types (track,album,artist,playlist,show,episode,audiobook).")
@click.pass_context
def search_query(ctx: click.Context, query: str, search_type: str) -> None:
    """General search across one or more types."""
    client = ctx.obj["client"]
    _output(client.search.search(query, types=search_type, limit=ctx.obj["limit"]), ctx.obj["compact"])


@search.command("tracks")
@click.argument("query")
@click.pass_context
def search_tracks(ctx: click.Context, query: str) -> None:
    """Search for tracks."""
    client = ctx.obj["client"]
    _output(client.search.search_tracks(query, limit=ctx.obj["limit"]), ctx.obj["compact"])


@search.command("albums")
@click.argument("query")
@click.pass_context
def search_albums(ctx: click.Context, query: str) -> None:
    """Search for albums."""
    client = ctx.obj["client"]
    _output(client.search.search_albums(query, limit=ctx.obj["limit"]), ctx.obj["compact"])


@search.command("artists")
@click.argument("query")
@click.pass_context
def search_artists(ctx: click.Context, query: str) -> None:
    """Search for artists."""
    client = ctx.obj["client"]
    _output(client.search.search_artists(query, limit=ctx.obj["limit"]), ctx.obj["compact"])


@search.command("playlists")
@click.argument("query")
@click.pass_context
def search_playlists(ctx: click.Context, query: str) -> None:
    """Search for playlists."""
    client = ctx.obj["client"]
    _output(client.search.search_playlists(query, limit=ctx.obj["limit"]), ctx.obj["compact"])


@search.command("shows")
@click.argument("query")
@click.pass_context
def search_shows(ctx: click.Context, query: str) -> None:
    """Search for shows/podcasts."""
    client = ctx.obj["client"]
    _output(client.search.search_shows(query, limit=ctx.obj["limit"]), ctx.obj["compact"])


@search.command("episodes")
@click.argument("query")
@click.pass_context
def search_episodes(ctx: click.Context, query: str) -> None:
    """Search for episodes."""
    client = ctx.obj["client"]
    _output(client.search.search_episodes(query, limit=ctx.obj["limit"]), ctx.obj["compact"])


@search.command("audiobooks")
@click.argument("query")
@click.pass_context
def search_audiobooks(ctx: click.Context, query: str) -> None:
    """Search for audiobooks."""
    client = ctx.obj["client"]
    _output(client.search.search_audiobooks(query, limit=ctx.obj["limit"]), ctx.obj["compact"])
