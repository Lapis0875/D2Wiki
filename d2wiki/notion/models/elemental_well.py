from __future__ import annotations

from enum import Enum
from typing import cast, TYPE_CHECKING

import attr
from discord import Embed

from d2wiki.types import JSON, JSON_VALUES
from d2wiki.utils.functional import cache_first_res
from .base import D2JsonModel
from .rich_text import wrap_diff
from .elements import D2Element

__all__ = ("D2ElementalWellModType", "D2ElementalWell")

if TYPE_CHECKING:
    from .. import D2NotionWrapper


class D2ElementalWellModType(Enum):
    GENERATE = "생성"
    USE = "사용"
    ASSIST = "보조"
    RELIC = "유물"


@attr.s
class D2ElementalWell(D2JsonModel):
    """
    Destiny2 Elemental Well Model.
    원소샘이 Elemntal Well이 맞나?
    """
    id: str = attr.ib(repr=True, eq=True, hash=True)    # notion id.
    name: str = attr.ib(repr=True, eq=True, hash=True)
    element: D2Element = attr.ib(repr=True, eq=True, hash=True)
    mod_type: D2ElementalWellModType = attr.ib(repr=True, eq=True, hash=True)
    cost: int = attr.ib(repr=True, eq=True, hash=True)
    description: str = attr.ib(repr=False, eq=False, hash=True)
    page_url: str = attr.ib(repr=False, eq=False, hash=True)
    footer: str | None = attr.ib(default=None, repr=False, eq=False, hash=False)
    img_url: str | None = attr.ib(default=None, repr=False, eq=False, hash=False)

    @classmethod
    def from_json(cls, nc: D2NotionWrapper, _id: str, **json: JSON_VALUES) -> D2ElementalWell:
        return cls(
            nc=nc,
            id=_id,
            name=json["name"],
            element=cast(D2Element, D2Element(json["element"])),
            mod_type=cast(D2ElementalWellModType, D2ElementalWellModType(json["mod_type"])),
            cost=json["cost"],
            description=json["description"],
            page_url=nc.get_shared_url(_id),
            img_url=json["img_url"]
        )

    def to_json(self) -> JSON:
        return {
            "name": self.name,
            "element": self.element.value,
            "mod_type": self.mod_type.value,
            "cost": self.cost,
            "description": self.description,
            "page_url": self.page_url,
            "img_url": self.img_url
        }

    @property
    @cache_first_res
    def full_description(self) -> str:
        return f"{self.description}\n\n{wrap_diff(self.footer)}" if self.footer is not None else self.description

    @property
    # @cache_first_res
    def embed(self) -> Embed:
        e = Embed(
            title=self.name,
            description=self.full_description,
            url=self.page_url
        ).add_field(
            name="원소 유형",
            value=cast(str, self.element.value),
            inline=False
        ).add_field(
            name="개조부품 유형",
            value=cast(str, self.mod_type.value),
            inline=False
        ).add_field(
            name="개조부품 에너지 사용량",
            value=str(self.cost),
            inline=False
        ).add_field(
            name="노션에서 보기",
            value=f"[클릭]({self.page_url})",
            inline=False
        )

        if self.img_url is not None:
            e.set_thumbnail(url=self.img_url)
        return e
