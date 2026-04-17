from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from pokecli.models.common import NamedResource


class EvolutionDetail(BaseModel):
    model_config = ConfigDict(extra="ignore")

    trigger: NamedResource
    min_level: int | None = None
    item: NamedResource | None = None
    held_item: NamedResource | None = None
    known_move: NamedResource | None = None
    min_happiness: int | None = None
    min_beauty: int | None = None
    min_affection: int | None = None
    time_of_day: str = ""
    location: NamedResource | None = None
    needs_overworld_rain: bool = False
    turn_upside_down: bool = False


class ChainLink(BaseModel):
    model_config = ConfigDict(extra="ignore")

    species: NamedResource
    evolution_details: list[EvolutionDetail]
    evolves_to: list[ChainLink]


class EvolutionChain(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    chain: ChainLink


class PokemonSpecies(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    name: str
    generation: NamedResource
    color: NamedResource
    shape: NamedResource | None = None
    habitat: NamedResource | None = None
    capture_rate: int
    base_happiness: int | None = None
    gender_rate: int
    egg_groups: list[NamedResource]
    growth_rate: NamedResource
    evolution_chain: dict
    flavor_text_entries: list[dict]
    genera: list[dict]
    is_legendary: bool
    is_mythical: bool
