"""CLI: playlist subcommands."""

import click

from spotify_client.cli import _output


@click.group()
def playlist() -> None:
    """Playlist commands."""


@playlist.command("get")
@click.argument("playlist_id")
@click.pass_context
def playlist_get(ctx: click.Context, playlist_id: str) -> None:
    """Get playlist details."""
    client = ctx.obj["client"]
    _output(client.playlists.get(playlist_id), ctx.obj["compact"])


@playlist.command("tracks")
@click.argument("playlist_id")
@click.pass_context
def playlist_tracks(ctx: click.Context, playlist_id: str) -> None:
    """Get tracks from a playlist."""
    client = ctx.obj["client"]
    _output(client.playlists.get_tracks(playlist_id, limit=ctx.obj["limit"]), ctx.obj["compact"])


@playlist.command("list")
@click.option("--user-id", default=None, help="User ID (default: current user, requires --user-auth).")
@click.pass_context
def playlist_list(ctx: click.Context, user_id: str | None) -> None:
    """List user's playlists."""
    client = ctx.obj["client"]
    _output(client.playlists.get_user_playlists(user_id=user_id, limit=ctx.obj["limit"]), ctx.obj["compact"])


@playlist.command("create")
@click.argument("name")
@click.option("--desc", default="", help="Playlist description.")
@click.option("--private", "is_private", is_flag=True, default=False, help="Make playlist private.")
@click.pass_context
def playlist_create(ctx: click.Context, name: str, desc: str, is_private: bool) -> None:
    """Create a new playlist (requires --user-auth)."""
    client = ctx.obj["client"]
    result = client.playlists.create(name=name, description=desc, public=not is_private)
    _output(result, ctx.obj["compact"])


@playlist.command("add-tracks")
@click.argument("playlist_id")
@click.argument("track_uris", nargs=-1, required=True)
@click.pass_context
def playlist_add_tracks(ctx: click.Context, playlist_id: str, track_uris: tuple[str, ...]) -> None:
    """Add tracks to a playlist (requires --user-auth)."""
    client = ctx.obj["client"]
    client.playlists.add_tracks(playlist_id, list(track_uris))
    click.echo(f"Added {len(track_uris)} track(s) to playlist.")


@playlist.command("remove-tracks")
@click.argument("playlist_id")
@click.argument("track_uris", nargs=-1, required=True)
@click.pass_context
def playlist_remove_tracks(ctx: click.Context, playlist_id: str, track_uris: tuple[str, ...]) -> None:
    """Remove tracks from a playlist (requires --user-auth)."""
    client = ctx.obj["client"]
    client.playlists.remove_tracks(playlist_id, list(track_uris))
    click.echo(f"Removed {len(track_uris)} track(s) from playlist.")


@playlist.command("update")
@click.argument("playlist_id")
@click.option("--name", default=None, help="New playlist name.")
@click.option("--desc", default=None, help="New description.")
@click.option("--public/--private", default=None, help="Set visibility.")
@click.pass_context
def playlist_update(ctx: click.Context, playlist_id: str, name: str | None, desc: str | None, public: bool | None) -> None:
    """Update playlist details (requires --user-auth)."""
    client = ctx.obj["client"]
    client.playlists.update_details(playlist_id, name=name, description=desc, public=public)
    click.echo("Playlist updated.")
