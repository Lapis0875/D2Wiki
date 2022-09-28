from __future__ import annotations
import attr
from discord import Embed
from typing import TYPE_CHECKING

from d2wiki.types import JSON
from .base import D2JsonModel

if TYPE_CHECKING:
    from ..wrapper import D2NotionWrapper

__all__ = ("PartialNotionUser", "NotionUser")


@attr.s(slots=True)
class PartialNotionUser(D2JsonModel):
    id: str = attr.ib(repr=True, eq=True, hash=True)
    __full_user: NotionUser | None = attr.ib(default=None, repr=False, eq=False, hash=False)

    @classmethod
    def from_json(cls, **json: str | D2NotionWrapper) -> PartialNotionUser:
        return cls(nc=json["nc"], id=json["id"])

    def to_json(self) -> JSON:
        return {"id": self.id}

    @property
    def embed(self) -> Embed:
        return Embed(
            title="Partial Notion User",
            description="This is a partial Notion User. Full user object should be retrieved from Notion API."
        ).add_field(
            name="id",
            value=self.id
        )

    async def get_full_user(self) -> NotionUser:
        """
        Get Full Notion User object from Notion API.
        :return: NotionUser object of this Partial Notion User.
        """
        if self.__full_user is None:
            self.__full_user = await self.nc.retrieve_user(self.id)
        return self.__full_user


@attr.s
class NotionUser(D2JsonModel):
    """
    Notion User Model.
    """
    id: str = attr.ib(repr=True, eq=True, hash=True)

    @classmethod
    def from_json(cls, **json: str | D2NotionWrapper) -> NotionUser:
        return cls(
            nc=json["nc"],
            id=json["id"]
        )

    def to_json(self) -> JSON:
        obj = {
            "id": self.id
        }
        return obj

    @property
    def embed(self) -> Embed:
        return Embed(
            title="Notion User",
            description=""
        ).add_field(
            name="id",
            value=self.id
        )
