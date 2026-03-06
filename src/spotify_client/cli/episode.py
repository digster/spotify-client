"""CLI: episode subcommands."""

import click

from spotify_client.cli import _output


@click.group()
def episode() -> None:
    """Episode information commands."""


@episode.command("get")
@click.argument("episode_id")
@click.pass_context
def episode_get(ctx: click.Context, episode_id: str) -> None:
    """Get episode info by ID or URI."""
    client = ctx.obj["client"]
    _output(client.episodes.get(episode_id), ctx.obj["compact"])


@episode.command("get-many")
@click.argument("episode_ids", nargs=-1, required=True)
@click.pass_context
def episode_get_many(ctx: click.Context, episode_ids: tuple[str, ...]) -> None:
    """Get multiple episodes by ID."""
    client = ctx.obj["client"]
    _output(client.episodes.get_many(list(episode_ids)), ctx.obj["compact"])
