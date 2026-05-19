import typer
from pydantic import ValidationError
from rich.console import Console

from pokecli.commands._utils import fetch_list, fetch_resource
from pokecli.config import DEFAULT_LIMIT, DEFAULT_OFFSET
from pokecli.display.common import render_json, render_list
from pokecli.display.game import render_pokedex
from pokecli.models.game import Pokedex

app = typer.Typer(help="Search and browse Pokedexes (regional and national).")
console = Console()
err_console = Console(stderr=True)


@app.command()
def get(
    ctx: typer.Context,
    name_or_id: str = typer.Argument(..., help="Pokedex name or ID"),
    no_cache: bool = typer.Option(False, "--no-cache", help="Skip local cache"),
    format: str = typer.Option(
        "table", "--format", help="Output format: table or json"
    ),
) -> None:
    """Get a Pokedex with its full entries list."""
    client = ctx.obj["client"]
    data = fetch_resource(client, "pokedex", name_or_id, no_cache, err_console)
    try:
        pdx = Pokedex.model_validate(data)
    except ValidationError as e:
        err_console.print(f"[red]Unexpected API response format:[/red]\n{e}")
        raise typer.Exit(2)
    if format == "json":
        render_json(pdx.model_dump(), console)
    else:
        render_pokedex(pdx, console)


@app.command(name="list")
def list_pokedexes(
    ctx: typer.Context,
    limit: int = typer.Option(DEFAULT_LIMIT, "--limit", help="Number of results"),
    offset: int = typer.Option(DEFAULT_OFFSET, "--offset", help="Pagination offset"),
) -> None:
    """List Pokedexes with pagination."""
    client = ctx.obj["client"]
    render_list(fetch_list(client, "pokedex", limit, offset, err_console), console)
