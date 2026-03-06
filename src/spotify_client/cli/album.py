"""CLI: album subcommands."""

import click

from spotify_client.cli import _output


@click.group()
def album() -> None:
    """Album information commands."""


@album.command("get")
@click.argument("album_id")
@click.pass_context
def album_get(ctx: click.Context, album_id: str) -> None:
    """Get album info by ID or URI."""
    client = ctx.obj["client"]
    _output(client.albums.get(album_id), ctx.obj["compact"])


@album.command("get-many")
@click.argument("album_ids", nargs=-1, required=True)
@click.pass_context
def album_get_many(ctx: click.Context, album_ids: tuple[str, ...]) -> None:
    """Get multiple albums by ID."""
    client = ctx.obj["client"]
    _output(client.albums.get_many(list(album_ids)), ctx.obj["compact"])


@album.command("tracks")
@click.argument("album_id")
@click.pass_context
def album_tracks(ctx: click.Context, album_id: str) -> None:
    """Get all tracks from an album."""
    client = ctx.obj["client"]
    _output(client.albums.get_tracks(album_id, limit=ctx.obj["limit"]), ctx.obj["compact"])


@album.command("new-releases")
@click.option("--country", default=None, help="ISO 3166-1 alpha-2 country code.")
@click.pass_context
def album_new_releases(ctx: click.Context, country: str | None) -> None:
    """Get new album releases."""
    client = ctx.obj["client"]
    _output(client.albums.get_new_releases(country=country, limit=ctx.obj["limit"]), ctx.obj["compact"])
