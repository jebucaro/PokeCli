import typer

from pokecli.api.client import PokeAPIClient
from pokecli.commands import (
    ability,
    berry,
    cache,
    egg_group,
    evolution_chain,
    evolution_trigger,
    generation,
    growth_rate,
    image,
    install,
    item,
    location,
    location_area,
    machine,
    move,
    move_damage_class,
    move_learn_method,
    nature,
    pokedex,
    pokemon,
    pokemon_form,
    region,
    type as type_cmd,
    version,
    version_group,
)

app = typer.Typer(
    name="pokecli",
    help="A Pokemon CLI powered by PokeAPI with local caching.",
    no_args_is_help=True,
)


@app.callback()
def root(ctx: typer.Context) -> None:
    ctx.ensure_object(dict)
    ctx.obj["client"] = ctx.with_resource(PokeAPIClient())


app.add_typer(install.app, name="install")
app.add_typer(pokemon.app, name="pokemon")
app.add_typer(ability.app, name="ability")
app.add_typer(nature.app, name="nature")
app.add_typer(type_cmd.app, name="type")
app.add_typer(berry.app, name="berry")
app.add_typer(item.app, name="item")
app.add_typer(move.app, name="move")
app.add_typer(egg_group.app, name="egg-group")
app.add_typer(growth_rate.app, name="growth-rate")
app.add_typer(evolution_trigger.app, name="evolution-trigger")
app.add_typer(move_damage_class.app, name="move-damage-class")
app.add_typer(move_learn_method.app, name="move-learn-method")
app.add_typer(version.app, name="version")
app.add_typer(version_group.app, name="version-group")
app.add_typer(machine.app, name="machine")
app.add_typer(pokemon_form.app, name="pokemon-form")
app.add_typer(region.app, name="region")
app.add_typer(location.app, name="location")
app.add_typer(location_area.app, name="location-area")
app.add_typer(generation.app, name="generation")
app.add_typer(pokedex.app, name="pokedex")
app.add_typer(evolution_chain.app, name="evolution-chain")
app.add_typer(image.app, name="image")
app.add_typer(cache.app, name="cache")
