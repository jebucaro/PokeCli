from pydantic import BaseModel, ConfigDict

from pokecli.models.common import NamedResource


class TypeDamageRelations(BaseModel):
    model_config = ConfigDict(extra="ignore")

    no_damage_to: list[NamedResource]
    half_damage_to: list[NamedResource]
    double_damage_to: list[NamedResource]
    no_damage_from: list[NamedResource]
    half_damage_from: list[NamedResource]
    double_damage_from: list[NamedResource]


class PokemonType(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    name: str
    damage_relations: TypeDamageRelations
    pokemon: list[dict]
    moves: list[NamedResource]
