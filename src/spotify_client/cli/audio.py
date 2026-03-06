"""CLI: audio subcommands."""

import click

from spotify_client.cli import _output


@click.group()
def audio() -> None:
    """Audio features and analysis commands."""


@audio.command("features")
@click.argument("track_id")
@click.pass_context
def audio_features(ctx: click.Context, track_id: str) -> None:
    """Get audio features for a track."""
    client = ctx.obj["client"]
    _output(client.audio.get_features(track_id), ctx.obj["compact"])


@audio.command("features-many")
@click.argument("track_ids", nargs=-1, required=True)
@click.pass_context
def audio_features_many(ctx: click.Context, track_ids: tuple[str, ...]) -> None:
    """Get audio features for multiple tracks."""
    client = ctx.obj["client"]
    _output(client.audio.get_features_many(list(track_ids)), ctx.obj["compact"])


@audio.command("analysis")
@click.argument("track_id")
@click.pass_context
def audio_analysis(ctx: click.Context, track_id: str) -> None:
    """Get detailed audio analysis for a track."""
    client = ctx.obj["client"]
    _output(client.audio.get_analysis(track_id), ctx.obj["compact"])
