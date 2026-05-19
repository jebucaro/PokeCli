import typer
from pydantic import ValidationError
from rich.console import Console

from pokecli.commands._utils import fetch_list, fetch_resource
from pokecli.config import DEFAULT_LIMIT, DEFAULT_OFFSET
from pokecli.display.common import render_json, render_list
from pokecli.display.game import render_version_group
from pokecli.models.game import VersionGroup

app = typer.Typer(
    help="Search and browse Version Groups (e.g., red-blue, sword-shield)."
)
console = Console()
err_console = Console(stderr=True)


@app.command()
def get(
    ctx: typer.Context,
    name_or_id: str = typer.Argument(..., help="Version group name or ID"),
    no_cache: bool = typer.Option(False, "--no-cache", help="Skip local cache"),
    format: str = typer.Option(
        "table", "--format", help="Output format: table or json"
    ),
) -> None:
    """Get details about a Version Group."""
    client = ctx.obj["client"]
    data = fetch_resource(client, "version-group", name_or_id, no_cache, err_console)
    try:
        vg = VersionGroup.model_validate(data)
    except ValidationError as e:
        err_console.print(f"[red]Unexpected API response format:[/red]\n{e}")
        raise typer.Exit(2)
    if format == "json":
        render_json(vg.model_dump(), console)
    else:
        render_version_group(vg, console)


@app.command(name="list")
def list_version_groups(
    ctx: typer.Context,
    limit: int = typer.Option(DEFAULT_LIMIT, "--limit", help="Number of results"),
    offset: int = typer.Option(DEFAULT_OFFSET, "--offset", help="Pagination offset"),
) -> None:
    """List Version Groups with pagination."""
    client = ctx.obj["client"]
    render_list(
        fetch_list(client, "version-group", limit, offset, err_console), console
    )
