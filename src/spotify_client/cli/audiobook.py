"""CLI: audiobook subcommands."""

import click

from spotify_client.cli import _output


@click.group()
def audiobook() -> None:
    """Audiobook information commands."""


@audiobook.command("get")
@click.argument("audiobook_id")
@click.pass_context
def audiobook_get(ctx: click.Context, audiobook_id: str) -> None:
    """Get audiobook info by ID or URI."""
    client = ctx.obj["client"]
    _output(client.audiobooks.get(audiobook_id), ctx.obj["compact"])


@audiobook.command("get-many")
@click.argument("audiobook_ids", nargs=-1, required=True)
@click.pass_context
def audiobook_get_many(ctx: click.Context, audiobook_ids: tuple[str, ...]) -> None:
    """Get multiple audiobooks by ID."""
    client = ctx.obj["client"]
    _output(client.audiobooks.get_many(list(audiobook_ids)), ctx.obj["compact"])


@audiobook.command("chapters")
@click.argument("audiobook_id")
@click.pass_context
def audiobook_chapters(ctx: click.Context, audiobook_id: str) -> None:
    """Get chapters of an audiobook."""
    client = ctx.obj["client"]
    _output(client.audiobooks.get_chapters(audiobook_id, limit=ctx.obj["limit"]), ctx.obj["compact"])
