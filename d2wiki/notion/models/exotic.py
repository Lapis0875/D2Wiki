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
    id: str = attr.ib(repr=True, eq=True, hash=True)    # notion id.
    name: str = attr.ib(repr=True, eq=True, hash=True)
    category: D2WeaponCategory = attr.ib(repr=True, eq=True, hash=True)
    exotic_perk_name: str = attr.ib(repr=True, eq=True, hash=True)
    weapon_slot: D2WeaponSlot = attr.ib(repr=True, eq=True, hash=True)
    page_url: str = attr.ib(repr=False, eq=False, hash=False)
    description: str | None = attr.ib(default=None, repr=False, eq=False, hash=True)
    img_url: str | None = attr.ib(default=None, eq=False, hash=False)

    @classmethod
    def from_json(cls, nc: D2NotionWrapper, _id: str, **json: str) -> D2ExoticWeapon:
        return cls(
            nc=nc,
            id=_id,
            name=json["name"],
            category=D2WeaponCategory(json["category"]),
            exotic_perk_name=json["exotic_perk_name"],
            weapon_slot=D2WeaponSlot(json["weapon_slot"]),
            description=json["description"],
            page_url=nc.get_shared_url(_id),
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
        e = Embed(
            title=self.name,
            color=EXOTIC_COLOR
        ).add_field(
            name="?????????",
            value=cast(str, self.category.value),
            inline=True
        ).add_field(
            name="?????? ??????",
            value=self.exotic_perk_name,
            inline=False
        ).add_field(
            name="??????",
            value=wrap_diff(self.description),
            inline=False
        ).add_field(
            name="???????????? ??????",
            value=f"[??????]({self.page_url})",
            inline=False
        )

        if self.img_url is not None:
            e.set_thumbnail(url=self.img_url)

        return e


@attr.s
class D2ExoticArmor(D2JsonModel):
    """
    Exotic Armor model.
    """
    id: str = attr.ib(repr=True, eq=True, hash=True)    # notion id.
    name: list[RichText] = attr.ib(repr=True, eq=True, hash=True)
    exotic_perk_name: list[RichText] = attr.ib(repr=True, eq=True, hash=True)
    guardian_class: D2GuardianClass = attr.ib(repr=True, eq=True, hash=True)
    category: D2ArmorCategory = attr.ib(repr=True, eq=True, hash=True)
    page_url: str = attr.ib(repr=False, eq=False, hash=False)
    description: str | None = attr.ib(default=None, repr=False, eq=False, hash=True)
    img_url: str | None = attr.ib(default=None, eq=False, hash=False)

    @classmethod
    def from_json(cls, nc: D2NotionWrapper, _id: str, **json: str | dict) -> D2ExoticArmor:
        return cls(
            nc=nc,
            id=_id,
            name=[RichText.from_json(**r) for r in json["name"]],
            exotic_perk_name=[RichText.from_json(**r) for r in json["exotic_perk_name"]],
            guardian_class=D2GuardianClass(json["guardian_class"]),
            category=D2ArmorCategory(json["category"]),
            page_url=nc.get_shared_url(_id),
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
        page = await self.nc.retrieve_page(self.id)
        await page.retrieve_children()
        # print(f"{self.name} ??? ?????? ????????? ??? ?????? ?????? ?????? : {len(page.children)}")
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
            name="??????",
            value=cast(str, self.guardian_class.value),
            inline=True
        ).add_field(
            name="??????",
            value=cast(str, self.category.value),
            inline=True
        ).add_field(
            name="?????? ??????",
            value=flat_rich_text(self.exotic_perk_name) if self.exotic_perk_name else "?????? ??????????????????.",
            inline=False
        ).add_field(
            name="??????",
            value=self.description or "?????? ??????????????????.",
            inline=False
        ).add_field(
            name="???????????? ??????",
            value=f"[??????]({self.page_url})",
            inline=False
        )

        if self.img_url is not None:
            e.set_thumbnail(url=self.img_url)

        return e
