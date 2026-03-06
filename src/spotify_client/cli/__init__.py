"""CLI entry point — Click group with global flags and subcommands."""

import json
import sys

import click

from spotify_client.client import SpotifyClient
from spotify_client.exceptions import SpotifyClientError


def _output(data: object, compact: bool = False) -> None:
    """Print data as JSON to stdout."""
    indent = None if compact else 2
    click.echo(json.dumps(data, indent=indent, default=str))


@click.group()
@click.option("--user-auth", "-u", is_flag=True, default=False, help="Use OAuth user authentication flow.")
@click.option("--limit", "-l", type=int, default=20, help="Max results to return.")
@click.option("--compact", "-c", is_flag=True, default=False, help="Compact JSON output (no indentation).")
@click.pass_context
def cli(ctx: click.Context, user_auth: bool, limit: int, compact: bool) -> None:
    """Spotify CLI — query Spotify data from the terminal."""
    ctx.ensure_object(dict)
    ctx.obj["compact"] = compact
    ctx.obj["limit"] = limit
    try:
        ctx.obj["client"] = SpotifyClient(user_auth=user_auth)
    except SpotifyClientError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)


# Import and register subcommand groups
from spotify_client.cli.track import track  # noqa: E402
from spotify_client.cli.album import album  # noqa: E402
from spotify_client.cli.artist import artist  # noqa: E402
from spotify_client.cli.search import search  # noqa: E402
from spotify_client.cli.audio import audio  # noqa: E402
from spotify_client.cli.recommend import recommend  # noqa: E402
from spotify_client.cli.show import show  # noqa: E402
from spotify_client.cli.episode import episode  # noqa: E402
from spotify_client.cli.audiobook import audiobook  # noqa: E402
from spotify_client.cli.user import user  # noqa: E402
from spotify_client.cli.playlist import playlist  # noqa: E402

cli.add_command(track)
cli.add_command(album)
cli.add_command(artist)
cli.add_command(search)
cli.add_command(audio)
cli.add_command(recommend)
cli.add_command(show)
cli.add_command(episode)
cli.add_command(audiobook)
cli.add_command(user)
cli.add_command(playlist)
