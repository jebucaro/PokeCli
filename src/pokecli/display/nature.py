from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from pokecli.models.nature import Nature


def render_nature(nature: Nature, console: Console) -> None:
    header = f"[bold]#{nature.id}  {nature.name.capitalize()} Nature[/bold]"
    console.print(Panel(header, expand=False))

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Key", style="bold dim")
    table.add_column("Value", style="white")

    if nature.increased_stat and nature.decreased_stat:
        increased = nature.increased_stat.name.replace("-", " ").title()
        decreased = nature.decreased_stat.name.replace("-", " ").title()
        table.add_row(
            "Stat Modifier",
            f"[green]+10% {increased}[/green]  [red]-10% {decreased}[/red]",
        )
    else:
        table.add_row("Stat Modifier", "[dim]Neutral (no change)[/dim]")

    if nature.likes_flavor:
        table.add_row("Likes Flavor", nature.likes_flavor.name.capitalize())
    if nature.hates_flavor:
        table.add_row("Hates Flavor", nature.hates_flavor.name.capitalize())

    console.print(table)
