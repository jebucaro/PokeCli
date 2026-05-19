import typer
from pydantic import ValidationError
from rich.console import Console

from pokecli.commands._utils import fetch_list, fetch_resource
from pokecli.config import DEFAULT_LIMIT, DEFAULT_OFFSET
from pokecli.display.common import render_json, render_list
from pokecli.display.location import render_location
from pokecli.models.location import Location

app = typer.Typer(help="Search and browse Locations (towns, routes, dungeons).")
console = Console()
err_console = Console(stderr=True)


@app.command()
def get(
    ctx: typer.Context,
    name_or_id: str = typer.Argument(..., help="Location name or ID"),
    no_cache: bool = typer.Option(False, "--no-cache", help="Skip local cache"),
    format: str = typer.Option(
        "table", "--format", help="Output format: table or json"
    ),
) -> None:
    """Get details about a Location (includes its child areas)."""
    client = ctx.obj["client"]
    data = fetch_resource(client, "location", name_or_id, no_cache, err_console)
    try:
        loc = Location.model_validate(data)
    except ValidationError as e:
        err_console.print(f"[red]Unexpected API response format:[/red]\n{e}")
        raise typer.Exit(2)
    if format == "json":
        render_json(loc.model_dump(), console)
    else:
        render_location(loc, console)


@app.command(name="list")
def list_locations(
    ctx: typer.Context,
    limit: int = typer.Option(DEFAULT_LIMIT, "--limit", help="Number of results"),
    offset: int = typer.Option(DEFAULT_OFFSET, "--offset", help="Pagination offset"),
) -> None:
    """List Locations with pagination."""
    client = ctx.obj["client"]
    render_list(fetch_list(client, "location", limit, offset, err_console), console)
