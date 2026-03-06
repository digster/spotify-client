"""CLI: user subcommands (all require --user-auth)."""

import click

from spotify_client.cli import _output


@click.group()
def user() -> None:
    """User library and profile commands (require --user-auth / -u)."""


# -- Profile --

@user.command("profile")
@click.argument("user_id", required=False, default=None)
@click.pass_context
def user_profile(ctx: click.Context, user_id: str | None) -> None:
    """Get user profile. Pass a user_id for public profiles, or omit for current user."""
    client = ctx.obj["client"]
    _output(client.user.get_profile(user_id), ctx.obj["compact"])


# -- Saved Tracks --

@user.command("saved-tracks")
@click.pass_context
def user_saved_tracks(ctx: click.Context) -> None:
    """Get saved/liked tracks."""
    client = ctx.obj["client"]
    _output(client.user.get_saved_tracks(limit=ctx.obj["limit"]), ctx.obj["compact"])


@user.command("save-tracks")
@click.argument("track_ids", nargs=-1, required=True)
@click.pass_context
def user_save_tracks(ctx: click.Context, track_ids: tuple[str, ...]) -> None:
    """Save tracks to library."""
    client = ctx.obj["client"]
    client.user.save_tracks(list(track_ids))
    click.echo(f"Saved {len(track_ids)} track(s).")


@user.command("remove-tracks")
@click.argument("track_ids", nargs=-1, required=True)
@click.pass_context
def user_remove_tracks(ctx: click.Context, track_ids: tuple[str, ...]) -> None:
    """Remove tracks from library."""
    client = ctx.obj["client"]
    client.user.remove_saved_tracks(list(track_ids))
    click.echo(f"Removed {len(track_ids)} track(s).")


@user.command("check-tracks")
@click.argument("track_ids", nargs=-1, required=True)
@click.pass_context
def user_check_tracks(ctx: click.Context, track_ids: tuple[str, ...]) -> None:
    """Check if tracks are saved in library."""
    client = ctx.obj["client"]
    results = client.user.check_saved_tracks(list(track_ids))
    _output(dict(zip(track_ids, results)), ctx.obj["compact"])


# -- Saved Albums --

@user.command("saved-albums")
@click.pass_context
def user_saved_albums(ctx: click.Context) -> None:
    """Get saved albums."""
    client = ctx.obj["client"]
    _output(client.user.get_saved_albums(limit=ctx.obj["limit"]), ctx.obj["compact"])


@user.command("save-albums")
@click.argument("album_ids", nargs=-1, required=True)
@click.pass_context
def user_save_albums(ctx: click.Context, album_ids: tuple[str, ...]) -> None:
    """Save albums to library."""
    client = ctx.obj["client"]
    client.user.save_albums(list(album_ids))
    click.echo(f"Saved {len(album_ids)} album(s).")


@user.command("remove-albums")
@click.argument("album_ids", nargs=-1, required=True)
@click.pass_context
def user_remove_albums(ctx: click.Context, album_ids: tuple[str, ...]) -> None:
    """Remove albums from library."""
    client = ctx.obj["client"]
    client.user.remove_saved_albums(list(album_ids))
    click.echo(f"Removed {len(album_ids)} album(s).")


# -- Saved Shows --

@user.command("saved-shows")
@click.pass_context
def user_saved_shows(ctx: click.Context) -> None:
    """Get saved shows/podcasts."""
    client = ctx.obj["client"]
    _output(client.user.get_saved_shows(limit=ctx.obj["limit"]), ctx.obj["compact"])


@user.command("save-shows")
@click.argument("show_ids", nargs=-1, required=True)
@click.pass_context
def user_save_shows(ctx: click.Context, show_ids: tuple[str, ...]) -> None:
    """Save shows to library."""
    client = ctx.obj["client"]
    client.user.save_shows(list(show_ids))
    click.echo(f"Saved {len(show_ids)} show(s).")


@user.command("remove-shows")
@click.argument("show_ids", nargs=-1, required=True)
@click.pass_context
def user_remove_shows(ctx: click.Context, show_ids: tuple[str, ...]) -> None:
    """Remove shows from library."""
    client = ctx.obj["client"]
    client.user.remove_saved_shows(list(show_ids))
    click.echo(f"Removed {len(show_ids)} show(s).")


# -- Following --

@user.command("followed-artists")
@click.pass_context
def user_followed_artists(ctx: click.Context) -> None:
    """Get followed artists."""
    client = ctx.obj["client"]
    _output(client.user.get_followed_artists(limit=ctx.obj["limit"]), ctx.obj["compact"])


@user.command("follow-artists")
@click.argument("artist_ids", nargs=-1, required=True)
@click.pass_context
def user_follow_artists(ctx: click.Context, artist_ids: tuple[str, ...]) -> None:
    """Follow artists."""
    client = ctx.obj["client"]
    client.user.follow_artists(list(artist_ids))
    click.echo(f"Followed {len(artist_ids)} artist(s).")


@user.command("unfollow-artists")
@click.argument("artist_ids", nargs=-1, required=True)
@click.pass_context
def user_unfollow_artists(ctx: click.Context, artist_ids: tuple[str, ...]) -> None:
    """Unfollow artists."""
    client = ctx.obj["client"]
    client.user.unfollow_artists(list(artist_ids))
    click.echo(f"Unfollowed {len(artist_ids)} artist(s).")


# -- Top Items --

@user.command("top-tracks")
@click.option("--time-range", default="medium_term", help="short_term, medium_term, or long_term.")
@click.pass_context
def user_top_tracks(ctx: click.Context, time_range: str) -> None:
    """Get top tracks."""
    client = ctx.obj["client"]
    _output(client.user.get_top_tracks(limit=ctx.obj["limit"], time_range=time_range), ctx.obj["compact"])


@user.command("top-artists")
@click.option("--time-range", default="medium_term", help="short_term, medium_term, or long_term.")
@click.pass_context
def user_top_artists(ctx: click.Context, time_range: str) -> None:
    """Get top artists."""
    client = ctx.obj["client"]
    _output(client.user.get_top_artists(limit=ctx.obj["limit"], time_range=time_range), ctx.obj["compact"])


# -- Recently Played --

@user.command("recently-played")
@click.pass_context
def user_recently_played(ctx: click.Context) -> None:
    """Get recently played tracks."""
    client = ctx.obj["client"]
    _output(client.user.get_recently_played(limit=ctx.obj["limit"]), ctx.obj["compact"])
