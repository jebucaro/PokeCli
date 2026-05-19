import typer
from pydantic import ValidationError
from rich.console import Console

from pokecli.commands._utils import fetch_list, fetch_resource
from pokecli.config import DEFAULT_LIMIT, DEFAULT_OFFSET
from pokecli.display.common import render_json, render_list
from pokecli.display.reference import render_reference
from pokecli.models.reference import SimpleNamedResource

app = typer.Typer(
    help="Search and browse Move Damage Classes (physical/special/status)."
)
console = Console()
err_console = Console(stderr=True)


@app.command()
def get(
    ctx: typer.Context,
    name_or_id: str = typer.Argument(..., help="Damage class name or ID"),
    no_cache: bool = typer.Option(False, "--no-cache", help="Skip local cache"),
    format: str = typer.Option(
        "table", "--format", help="Output format: table or json"
    ),
) -> None:
    """Get details about a Move Damage Class."""
    client = ctx.obj["client"]
    data = fetch_resource(
        client, "move-damage-class", name_or_id, no_cache, err_console
    )
    try:
        resource = SimpleNamedResource.model_validate(data)
    except ValidationError as e:
        err_console.print(f"[red]Unexpected API response format:[/red]\n{e}")
        raise typer.Exit(2)
    if format == "json":
        render_json(resource.model_dump(), console)
    else:
        render_reference(resource, console, "Damage Class")


@app.command(name="list")
def list_damage_classes(
    ctx: typer.Context,
    limit: int = typer.Option(DEFAULT_LIMIT, "--limit", help="Number of results"),
    offset: int = typer.Option(DEFAULT_OFFSET, "--offset", help="Pagination offset"),
) -> None:
    """List Move Damage Classes with pagination."""
    client = ctx.obj["client"]
    render_list(
        fetch_list(client, "move-damage-class", limit, offset, err_console), console
    )
