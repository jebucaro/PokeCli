from pydantic import BaseModel, ConfigDict

from pokecli.models.common import NamedResource


class AbilityEffect(BaseModel):
    model_config = ConfigDict(extra="ignore")

    effect: str
    short_effect: str
    language: NamedResource


class Ability(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    name: str
    generation: NamedResource
    effect_entries: list[AbilityEffect]
    pokemon: list[dict]
