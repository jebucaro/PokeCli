from rich.console import Console
from rich.panel import Panel

from pokecli.display.common import panel_title
from pokecli.models.ability import Ability


def render_ability(ability: Ability, console: Console) -> None:
    header = panel_title(ability.id, ability.name.replace("-", " ").title())
    generation = ability.generation.name.replace("-", " ").title()
    info = (
        f"[bold]Generation:[/bold] {generation}   "
        f"[bold]Pokemon with this ability:[/bold] {len(ability.pokemon)}\n"
    )
    console.print(Panel(header, expand=False))
    console.print(info)

    english_effects = [e for e in ability.effect_entries if e.language.name == "en"]
    if english_effects:
        console.print(f"[bold]Effect:[/bold] {english_effects[0].short_effect}\n")
        console.print(f"[dim]{english_effects[0].effect}[/dim]")
