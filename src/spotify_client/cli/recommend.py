"""CLI: recommend subcommands."""

import click

from spotify_client.cli import _output


@click.group(invoke_without_command=True)
@click.option("--seed-tracks", default=None, help="Comma-separated track IDs.")
@click.option("--seed-artists", default=None, help="Comma-separated artist IDs.")
@click.option("--seed-genres", default=None, help="Comma-separated genre names.")
@click.option("--target-energy", type=float, default=None, help="Target energy (0.0-1.0).")
@click.option("--target-danceability", type=float, default=None, help="Target danceability (0.0-1.0).")
@click.option("--target-valence", type=float, default=None, help="Target valence/positivity (0.0-1.0).")
@click.option("--min-tempo", type=float, default=None, help="Minimum tempo (BPM).")
@click.option("--max-tempo", type=float, default=None, help="Maximum tempo (BPM).")
@click.pass_context
def recommend(
    ctx: click.Context,
    seed_tracks: str | None,
    seed_artists: str | None,
    seed_genres: str | None,
    target_energy: float | None,
    target_danceability: float | None,
    target_valence: float | None,
    min_tempo: float | None,
    max_tempo: float | None,
) -> None:
    """Get track recommendations. Use 'recommend genres' to list available genres."""
    if ctx.invoked_subcommand is not None:
        return

    if not any([seed_tracks, seed_artists, seed_genres]):
        click.echo("Error: At least one seed (--seed-tracks, --seed-artists, or --seed-genres) is required.", err=True)
        return

    client = ctx.obj["client"]

    # Build tunable kwargs
    kwargs: dict = {}
    if target_energy is not None:
        kwargs["target_energy"] = target_energy
    if target_danceability is not None:
        kwargs["target_danceability"] = target_danceability
    if target_valence is not None:
        kwargs["target_valence"] = target_valence
    if min_tempo is not None:
        kwargs["min_tempo"] = min_tempo
    if max_tempo is not None:
        kwargs["max_tempo"] = max_tempo

    _output(
        client.recommendations.get_recommendations(
            seed_artists=seed_artists.split(",") if seed_artists else None,
            seed_tracks=seed_tracks.split(",") if seed_tracks else None,
            seed_genres=seed_genres.split(",") if seed_genres else None,
            limit=ctx.obj["limit"],
            **kwargs,
        ),
        ctx.obj["compact"],
    )


@recommend.command("genres")
@click.pass_context
def recommend_genres(ctx: click.Context) -> None:
    """List available genre seeds for recommendations."""
    client = ctx.obj["client"]
    _output(client.recommendations.get_available_genres(), ctx.obj["compact"])
