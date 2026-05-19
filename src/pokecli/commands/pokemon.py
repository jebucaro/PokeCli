import httpx
import typer
from pydantic import ValidationError
from rich.console import Console
from typing import Optional

from pokecli.cache.store import CacheStore
from pokecli.commands._utils import fetch_list, fetch_resource
from pokecli.config import DEFAULT_LIMIT, DEFAULT_OFFSET
from pokecli.display.common import render_json, render_list
from pokecli.display.evolution import render_evolution, render_species
from pokecli.display.location import render_encounters
from pokecli.display.pokemon import render_pokemon, render_pokemon_moves
from pokecli.display.pokemon_form import render_pokemon_varieties
from pokecli.models.evolution import EvolutionChain, PokemonSpecies
from pokecli.models.pokemon import Pokemon, PokemonMoveEntry

app = typer.Typer(help="Search and browse Pokemon.")
console = Console()
err_console = Console(stderr=True)


@app.command()
def get(
    ctx: typer.Context,
    name_or_id: str = typer.Argument(..., help="Pokemon name or Pokedex number"),
    no_cache: bool = typer.Option(False, "--no-cache", help="Skip local cache"),
    format: str = typer.Option(
        "table", "--format", help="Output format: table or json"
    ),
) -> None:
    """Get detailed information about a Pokemon."""
    client = ctx.obj["client"]
    data = fetch_resource(client, "pokemon", name_or_id, no_cache, err_console)
    try:
        pokemon = Pokemon.model_validate(data)
    except ValidationError as e:
        err_console.print(f"[red]Unexpected API response format:[/red]\n{e}")
        raise typer.Exit(2)
    if format == "json":
        render_json(pokemon.model_dump(), console)
    else:
        render_pokemon(pokemon, console)


def _extract_moves(raw_moves: list[dict]) -> list[PokemonMoveEntry]:
    """Deduplicate moves across all versions, keeping the most recent learn method."""
    seen: dict[str, PokemonMoveEntry] = {}
    for entry in raw_moves:
        move_name = entry["move"]["name"]
        details = entry.get("version_group_details", [])
        if not details:
            continue
        # Pick the version group with the highest numeric ID (most recent)
        best = max(
            details,
            key=lambda d: int(d["version_group"]["url"].rstrip("/").split("/")[-1]),
        )
        seen[move_name] = PokemonMoveEntry(
            name=move_name,
            learn_method=best["move_learn_method"]["name"],
            level=best["level_learned_at"],
        )
    return sorted(
        seen.values(), key=lambda m: (m.learn_method != "level-up", m.level, m.name)
    )


@app.command()
def moves(
    ctx: typer.Context,
    name_or_id: str = typer.Argument(..., help="Pokemon name or Pokedex number"),
    no_cache: bool = typer.Option(False, "--no-cache", help="Skip local cache"),
    format: str = typer.Option(
        "table", "--format", help="Output format: table or json"
    ),
    move: Optional[str] = typer.Option(
        None, "--move", help="Filter to a specific move name"
    ),
    method: Optional[str] = typer.Option(
        None,
        "--method",
        help="Filter by learn method: level-up, machine, tutor, egg",
    ),
) -> None:
    """List all moves a Pokemon can learn."""
    client = ctx.obj["client"]
    data = fetch_resource(client, "pokemon", name_or_id, no_cache, err_console)
    pokemon_name = data["name"]
    pokemon_moves = _extract_moves(data.get("moves", []))

    if move is not None:
        move_lower = move.lower().replace(" ", "-")
        matched = [m for m in pokemon_moves if m.name == move_lower]
        if format == "json":
            if matched:
                render_json(
                    {
                        "pokemon": pokemon_name,
                        "move": move_lower,
                        "can_learn": True,
                        "method": matched[0].learn_method,
                        "level": matched[0].level,
                    },
                    console,
                )
            else:
                render_json(
                    {"pokemon": pokemon_name, "move": move_lower, "can_learn": False},
                    console,
                )
                raise typer.Exit(1)
        else:
            if matched:
                render_pokemon_moves(
                    pokemon_name, matched, console, move_filter=move_lower
                )
            else:
                err_console.print(
                    f"[yellow]{pokemon_name.capitalize()} cannot learn {move_lower}.[/yellow]"
                )
                raise typer.Exit(1)
        return

    if method is not None:
        pokemon_moves = [m for m in pokemon_moves if m.learn_method == method]

    if format == "json":
        render_json(
            {"name": pokemon_name, "moves": [m.model_dump() for m in pokemon_moves]},
            console,
        )
    else:
        render_pokemon_moves(pokemon_name, pokemon_moves, console, method_filter=method)


@app.command()
def species(
    ctx: typer.Context,
    name_or_id: str = typer.Argument(..., help="Pokemon name or Pokedex number"),
    no_cache: bool = typer.Option(False, "--no-cache", help="Skip local cache"),
    format: str = typer.Option(
        "table", "--format", help="Output format: table or json"
    ),
) -> None:
    """Get species data for a Pokemon (Pokedex entry, egg groups, capture rate, etc.)."""
    client = ctx.obj["client"]
    data = fetch_resource(client, "pokemon-species", name_or_id, no_cache, err_console)
    try:
        poke_species = PokemonSpecies.model_validate(data)
    except ValidationError as e:
        err_console.print(f"[red]Unexpected API response format:[/red]\n{e}")
        raise typer.Exit(2)
    if format == "json":
        render_json(poke_species.model_dump(), console)
    else:
        render_species(poke_species, console)


@app.command()
def evolution(
    ctx: typer.Context,
    name_or_id: str = typer.Argument(..., help="Pokemon name or Pokedex number"),
    no_cache: bool = typer.Option(False, "--no-cache", help="Skip local cache"),
    format: str = typer.Option(
        "table", "--format", help="Output format: table or json"
    ),
) -> None:
    """Show the full evolution chain for a Pokemon."""
    client = ctx.obj["client"]

    # Step 1: fetch species to get evolution chain URL
    species_data = fetch_resource(
        client, "pokemon-species", name_or_id, no_cache, err_console
    )
    chain_url = species_data["evolution_chain"]["url"]
    chain_id = chain_url.rstrip("/").split("/")[-1]

    # Step 2: fetch evolution chain (with caching)
    with CacheStore() as cache:
        key = chain_id
        chain_data = None if no_cache else cache.get("evolution-chain", key)
        if chain_data is None:
            try:
                chain_data = client.get_resource_by_url(chain_url)
            except httpx.HTTPStatusError as e:
                err_console.print(f"[red]API error: {e.response.status_code}[/red]")
                raise typer.Exit(1)
            except (httpx.ConnectError, httpx.TimeoutException):
                err_console.print("[red]Network error: could not reach PokeAPI[/red]")
                raise typer.Exit(1)
            cache.set("evolution-chain", key, chain_data)

    try:
        chain = EvolutionChain.model_validate(chain_data)
    except ValidationError as e:
        err_console.print(f"[red]Unexpected API response format:[/red]\n{e}")
        raise typer.Exit(2)

    if format == "json":
        render_json(chain.model_dump(), console)
    else:
        render_evolution(chain, console)


@app.command()
def encounters(
    ctx: typer.Context,
    name_or_id: str = typer.Argument(..., help="Pokemon name or Pokedex number"),
    format: str = typer.Option(
        "table", "--format", help="Output format: table or json"
    ),
) -> None:
    """Show where a Pokemon can be encountered in the wild."""
    client = ctx.obj["client"]
    # Resolve identifier to canonical pokemon name (handles ID input)
    data = fetch_resource(client, "pokemon", name_or_id, False, err_console)
    pokemon_name = data["name"]
    try:
        result = client.get_subresource("pokemon", pokemon_name, "encounters")
    except httpx.HTTPStatusError as e:
        err_console.print(f"[red]API error: {e.response.status_code}[/red]")
        raise typer.Exit(1)
    except (httpx.ConnectError, httpx.TimeoutException):
        err_console.print("[red]Network error: could not reach PokeAPI[/red]")
        raise typer.Exit(1)

    if format == "json":
        render_json({"pokemon": pokemon_name, "encounters": result}, console)
    else:
        render_encounters(pokemon_name, result, console)


@app.command()
def forms(
    ctx: typer.Context,
    name_or_id: str = typer.Argument(..., help="Pokemon name or Pokedex number"),
    no_cache: bool = typer.Option(False, "--no-cache", help="Skip local cache"),
    format: str = typer.Option(
        "table", "--format", help="Output format: table or json"
    ),
) -> None:
    """List all varieties of a Pokemon species (Mega, Alolan, Gigantamax, etc.)."""
    client = ctx.obj["client"]
    species_data = fetch_resource(
        client, "pokemon-species", name_or_id, no_cache, err_console
    )
    species_name = species_data["name"]
    varieties = species_data.get("varieties", [])

    if format == "json":
        render_json({"species": species_name, "varieties": varieties}, console)
        return

    render_pokemon_varieties(species_name, varieties, console)


@app.command(name="list")
def list_pokemon(
    ctx: typer.Context,
    limit: int = typer.Option(DEFAULT_LIMIT, "--limit", help="Number of results"),
    offset: int = typer.Option(DEFAULT_OFFSET, "--offset", help="Pagination offset"),
) -> None:
    """List Pokemon with pagination."""
    client = ctx.obj["client"]
    render_list(fetch_list(client, "pokemon", limit, offset, err_console), console)
