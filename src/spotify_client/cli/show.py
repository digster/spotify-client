"""CLI: show/podcast subcommands."""

import click

from spotify_client.cli import _output


@click.group()
def show() -> None:
    """Show/podcast information commands."""


@show.command("get")
@click.argument("show_id")
@click.pass_context
def show_get(ctx: click.Context, show_id: str) -> None:
    """Get show info by ID or URI."""
    client = ctx.obj["client"]
    _output(client.shows.get(show_id), ctx.obj["compact"])


@show.command("get-many")
@click.argument("show_ids", nargs=-1, required=True)
@click.pass_context
def show_get_many(ctx: click.Context, show_ids: tuple[str, ...]) -> None:
    """Get multiple shows by ID."""
    client = ctx.obj["client"]
    _output(client.shows.get_many(list(show_ids)), ctx.obj["compact"])


@show.command("episodes")
@click.argument("show_id")
@click.pass_context
def show_episodes(ctx: click.Context, show_id: str) -> None:
    """Get episodes of a show."""
    client = ctx.obj["client"]
    _output(client.shows.get_episodes(show_id, limit=ctx.obj["limit"]), ctx.obj["compact"])
