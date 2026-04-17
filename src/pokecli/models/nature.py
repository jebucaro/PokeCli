from pydantic import BaseModel, ConfigDict

from pokecli.models.common import NamedResource


class Nature(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    name: str
    decreased_stat: NamedResource | None = None
    increased_stat: NamedResource | None = None
    hates_flavor: NamedResource | None = None
    likes_flavor: NamedResource | None = None
