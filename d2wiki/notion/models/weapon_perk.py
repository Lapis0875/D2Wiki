from __future__ import annotations
from typing import TYPE_CHECKING
import attr
from discord import Embed

from d2wiki.types import JSON
from .base import D2JsonModel
from .weapon import D2WeaponCategory
from .rich_text import wrap_diff, RichText, ansi_colorize, flat_rich_text

if TYPE_CHECKING:
    from ..wrapper import D2NotionWrapper


@attr.s
class D2Perk(D2JsonModel):
    """
    D2 Perk Model.
    """
    name: list[RichText] = attr.ib(repr=True, eq=True, hash=True)
    description: list[RichText] = attr.ib(repr=False, eq=False, hash=True)
    page_url: str = attr.ib(eq=True, hash=True)
    img_url: str | None = attr.ib(default=None, eq=False, hash=False)
    valid_weapons: list[D2WeaponCategory] = attr.ib(default=attr.Factory(list), eq=False, hash=False)

    @classmethod
    def from_json(cls, **json: str | D2NotionWrapper | JSON) -> D2Perk:
        return cls(
            nc=json["nc"],
            name=[RichText.from_json(**r) for r in json["name"]],
            description=[RichText.from_json(**r) for r in json["description"]],
            page_url=json["page_url"],
            img_url=json.get("img_url")
        )

    def to_json(self) -> JSON:
        return {
            "name": self.name,
            "description": self.description,
            "page_url": self.page_url,
            "img_url": self.img_url
        }

    @property
    # @cache_first_res
    def embed(self) -> Embed:
        e = Embed(title=flat_rich_text(self.name), description=ansi_colorize(self.description), url=self.page_url)
        e.add_field(name="노션에서 보기", value=f"[클릭]({self.page_url})", inline=False)
        if self.img_url is not None:
            e.set_thumbnail(url=self.img_url)
        return e
