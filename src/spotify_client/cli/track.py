"""CLI: track subcommands."""

import click

from spotify_client.cli import _output


@click.group()
def track() -> None:
    """Track information commands."""


@track.command("get")
@click.argument("track_id")
@click.pass_context
def track_get(ctx: click.Context, track_id: str) -> None:
    """Get track info by ID or URI."""
    client = ctx.obj["client"]
    _output(client.tracks.get(track_id), ctx.obj["compact"])


@track.command("get-many")
@click.argument("track_ids", nargs=-1, required=True)
@click.pass_context
def track_get_many(ctx: click.Context, track_ids: tuple[str, ...]) -> None:
    """Get multiple tracks by ID."""
    client = ctx.obj["client"]
    _output(client.tracks.get_many(list(track_ids)), ctx.obj["compact"])
