"""CLI: artist subcommands."""

import click

from spotify_client.cli import _output


@click.group()
def artist() -> None:
    """Artist information commands."""


@artist.command("get")
@click.argument("artist_id")
@click.pass_context
def artist_get(ctx: click.Context, artist_id: str) -> None:
    """Get artist info by ID or URI."""
    client = ctx.obj["client"]
    _output(client.artists.get(artist_id), ctx.obj["compact"])


@artist.command("get-many")
@click.argument("artist_ids", nargs=-1, required=True)
@click.pass_context
def artist_get_many(ctx: click.Context, artist_ids: tuple[str, ...]) -> None:
    """Get multiple artists by ID."""
    client = ctx.obj["client"]
    _output(client.artists.get_many(list(artist_ids)), ctx.obj["compact"])


@artist.command("top-tracks")
@click.argument("artist_id")
@click.option("--market", default="US", help="Market for top tracks.")
@click.pass_context
def artist_top_tracks(ctx: click.Context, artist_id: str, market: str) -> None:
    """Get an artist's top tracks."""
    client = ctx.obj["client"]
    _output(client.artists.get_top_tracks(artist_id, market=market), ctx.obj["compact"])


@artist.command("albums")
@click.argument("artist_id")
@click.option("--include", default="album,single", help="Album types to include (e.g., album,single).")
@click.pass_context
def artist_albums(ctx: click.Context, artist_id: str, include: str) -> None:
    """Get an artist's albums."""
    client = ctx.obj["client"]
    _output(
        client.artists.get_albums(artist_id, include_groups=include, limit=ctx.obj["limit"]),
        ctx.obj["compact"],
    )


@artist.command("related")
@click.argument("artist_id")
@click.pass_context
def artist_related(ctx: click.Context, artist_id: str) -> None:
    """Get related artists."""
    client = ctx.obj["client"]
    _output(client.artists.get_related(artist_id), ctx.obj["compact"])
