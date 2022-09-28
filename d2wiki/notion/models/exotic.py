from __future__ import annotations

from typing import cast

import attr
from discord import Embed, Color
from typing import TYPE_CHECKING

from d2wiki.types import JSON
from .base import D2JsonModel
from .armor_category import D2ArmorCategory
from .guardian_class import D2GuardianClass
from .notion_block import NotionParagraph
from .weapon import D2WeaponCategory, D2WeaponSlot
from .rich_text import wrap_diff, ansi_colorize, RichText, flat_rich_text

if TYPE_CHECKING:
    from ..wrapper import D2NotionWrapper

__all__ = ("D2ExoticWeapon", "D2ExoticArmor")

EXOTIC_COLOR = Color.from_rgb(205, 175, 45)


@attr.s
class D2ExoticWeapon(D2JsonModel):
    """
    Exotic Weapon model.
    """
    name: str = attr.ib(repr=True, eq=True, hash=True)
    category: D2WeaponCategory = attr.ib(repr=True, eq=True, hash=True)
    exotic_perk_name: str = attr.ib(repr=True, eq=True, hash=True)
    weapon_slot: D2WeaponSlot = attr.ib(repr=True, eq=True, hash=True)
    page_url: str = attr.ib(repr=False, eq=False, hash=False)
    description: str | None = attr.ib(default=None, repr=False, eq=False, hash=True)
    img_url: str | None = attr.ib(default=None, eq=False, hash=False)

    @classmethod
    def from_json(cls, **json: str | D2NotionWrapper) -> D2ExoticWeapon:
        return cls(
            nc=json["nc"],
            name=json["name"],
            category=D2WeaponCategory(json["category"]),
            exotic_perk_name=json["exotic_perk_name"],
            weapon_slot=D2WeaponSlot(json["weapon_slot"]),
            description=json["description"],
            page_url=json["page_url"],
            img_url=json.get("img_url")
        )

    def to_json(self) -> JSON:
        return {
            "name": self.name,
            "category": self.category.value,
            "exotic_perk_name": self.exotic_perk_name,
            "weapon_slot": self.weapon_slot.value,
            "description": self.description,
            "page_url": self.page_url,
            "img_url": self.img_url
        }

    @property
    def embed(self) -> Embed:
        return Embed(
            title=self.name,
            color=EXOTIC_COLOR
        ).add_field(
            name="무기군",
            value=cast(str, self.category.value),
            inline=True
        ).add_field(
            name="경이 특성",
            value=self.exotic_perk_name,
            inline=False
        ).add_field(
            name="효과",
            value=wrap_diff(self.description),
            inline=False
        )


@attr.s
class D2ExoticArmor(D2JsonModel):
    """
    Exotic Armor model.
    """
    name: list[RichText] = attr.ib(repr=True, eq=True, hash=True)
    exotic_perk_name: list[RichText] = attr.ib(repr=True, eq=True, hash=True)
    guardian_class: D2GuardianClass = attr.ib(repr=True, eq=True, hash=True)
    category: D2ArmorCategory = attr.ib(repr=True, eq=True, hash=True)
    page_url: str = attr.ib(repr=False, eq=False, hash=False)
    description: str | None = attr.ib(default=None, repr=False, eq=False, hash=True)
    img_url: str | None = attr.ib(default=None, eq=False, hash=False)

    @classmethod
    def from_json(cls, **json: str | D2NotionWrapper) -> D2ExoticArmor:
        return cls(
            nc=json["nc"],
            name=[RichText.from_json(**r) for r in json["name"]],
            exotic_perk_name=[RichText.from_json(**r) for r in json["exotic_perk_name"]],
            guardian_class=D2GuardianClass(json["guardian_class"]),
            category=D2ArmorCategory(json["category"]),
            page_url=json["page_url"],
            img_url=json.get("img_url")
        )

    def to_json(self) -> JSON:
        return {
            "name": ansi_colorize(self.name),
            "exotic_perk_name": ansi_colorize(self.exotic_perk_name),
            "guardian_class": cast(str, self.guardian_class.value),
            "category": cast(str, self.category.value),
            "page_url": self.page_url,
            "description": self.description,
            "img_url": self.img_url
        }

    async def resolve_description(self) -> D2ExoticArmor:
        print(f"Resolving description for {self.name}")
        page = await self.nc.retrieve_page(self.nc.get_id(self.page_url))
        await page.retrieve_children()
        # print(f"{self.name} 의 노션 페이지 내 자식 블록 개수 : {len(page.children)}")
        # print(page.children)
        self.description = "\n".join(map(
            lambda b: ansi_colorize(b.data.rich_text),
            filter(
                lambda b: b.type.value == "paragraph",
                page.children
            )
        ))
        # print(f"resolved desc : \n{self.description}")
        return self

    @property
    def embed(self) -> Embed:
        e = Embed(
            title=flat_rich_text(self.name),
            color=EXOTIC_COLOR
        ).add_field(
            name="직업",
            value=cast(str, self.guardian_class.value),
            inline=True
        ).add_field(
            name="부위",
            value=cast(str, self.category.value),
            inline=True
        ).add_field(
            name="경이 특성",
            value=flat_rich_text(self.exotic_perk_name) if self.exotic_perk_name else "아직 작성중입니다.",
            inline=False
        ).add_field(
            name="효과",
            value=self.description or "아직 작성중입니다.",
            inline=False
        )

        if self.img_url is not None:
            e.set_thumbnail(url=self.img_url)

        return e
