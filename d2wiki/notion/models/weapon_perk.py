from __future__ import annotations
import attr

from d2wiki.notion.models.base import D2JsonModel
from d2wiki.types import JSON


@attr.s
class D2Perk(D2JsonModel):
    """
    D2 Perk Model.
    """
    name: str = attr.ib(repr=True, eq=True, hash=True)
    description: str = attr.ib(repr=False, eq=False, hash=True)
    img_url: str | None = attr.ib(default=None, eq=False, hash=False)

    @classmethod
    def from_json(cls, **json: str) -> D2Perk:
        return cls(name=json["name"], description=json["description"], img_url=json.get("img_url"))

    def to_json(self) -> JSON:
        return {
            "name": self.name,
            "description": self.description,
            "img_url": self.img_url
        }
