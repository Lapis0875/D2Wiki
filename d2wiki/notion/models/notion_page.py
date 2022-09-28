from __future__ import annotations

from datetime import datetime

import attr
from typing import TYPE_CHECKING

from d2wiki.types import JSON
from d2wiki.utils.dtutil import notion2dt
from .base import D2JsonModel
from .notion_emoji import NotionEmoji
from .notion_file import NotionFile
from .notion_parent import NotionParent
from .notion_user import PartialNotionUser, NotionUser

if TYPE_CHECKING:
    from ..wrapper import D2NotionWrapper
    from . import NotionBlock

__all__ = ("NotionPage", )


@attr.s(slots=True)
class NotionPage(D2JsonModel):
    """
    Notion Page Model.
    """
    id: str = attr.ib(repr=True, eq=True, hash=True)
    created_time: datetime = attr.ib(repr=True, eq=False, hash=False)
    created_by: PartialNotionUser = attr.ib(repr=True, eq=False, hash=False)
    last_edited_time: datetime = attr.ib(repr=True, eq=False, hash=False)
    last_edited_by: PartialNotionUser = attr.ib(repr=True, eq=False, hash=False)
    archived: bool = attr.ib(repr=True, eq=False, hash=False)
    icon: NotionFile | NotionEmoji | None = attr.ib(repr=True, eq=False, hash=False)
    cover: NotionFile = attr.ib(repr=True, eq=False, hash=False)    # only NotionFileType.EXTERNAL is supported
    properties: object = attr.ib(repr=True, eq=False, hash=False)   # page only have title property.
    parent: NotionParent = attr.ib(repr=True, eq=False, hash=False)
    url: str = attr.ib(repr=True, eq=False, hash=False)
    children: list[NotionBlock] = attr.ib(repr=True, eq=False, hash=False)
    __full_creator: NotionUser | None = attr.ib(default=None, repr=False, eq=False, hash=False)
    __full_last_editor: NotionUser | None = attr.ib(default=None, repr=False, eq=False, hash=False)

    @classmethod
    def from_json(cls, _children: list[NotionBlock] = None, **json: str | bool | D2NotionWrapper | JSON) -> NotionPage:
        if json["icon"] is None:
            icon = None
        elif json["icon"]["type"] == "emoji":     # emoji
            icon = NotionEmoji.from_json(**json["icon"])
        else:   # file
            icon = NotionFile.from_json(**json["icon"])

        return cls(
            nc=json["nc"],
            id=json["id"],
            created_time=notion2dt(json["created_time"]),
            created_by=PartialNotionUser.from_json(nc=json["nc"], **json["created_by"]),
            last_edited_time=notion2dt(json["last_edited_time"]),
            last_edited_by=PartialNotionUser.from_json(nc=json["nc"], **json["last_edited_by"]),
            archived=json["archived"],
            icon=icon,
            cover=None if json["cover"] is None else NotionFile.from_json(**json["cover"]),
            properties=json["properties"],
            parent=NotionParent.from_json(nc=json["nc"], **json["parent"]),
            url=json["url"],
            children=[] if _children is None else _children
        )

    def to_json(self) -> JSON:
        return {
            "id": self.id,
            "created_time": self.created_time.isoformat(timespec="milliseconds"),
            "created_by": self.created_by.to_json(),
            "last_edited_time": self.last_edited_time.isoformat(timespec="milliseconds"),
            "last_edited_by": self.last_edited_by.to_json(),
            "archived": self.archived,
            "icon": self.icon.to_json(),
            "cover": self.cover.to_json(),
            "properties": self.properties,
            "parent": self.parent.to_json(),
            "url": self.url
        }

    @property
    def embed(self) -> None:
        """
        Not Embeddable model.
        """
        return None

    async def full_creator(self) -> NotionUser:
        """
        Retrieve Full Notion User object of 'created_by' field.
        :return:
        """
        if self.__full_creator is None:
            self.__full_creator = await self.nc.retrieve_user(self.created_by.id)
        return self.__full_creator

    async def full_last_editor(self) -> NotionUser:
        """
        Retrieve Full Notion User object of 'last_edited_by' field.
        :return:
        """
        if self.__full_last_editor is None:
            self.__full_last_editor = await self.nc.retrieve_user(self.last_edited_by.id)
        return self.__full_last_editor

    async def retrieve_children(self) -> NotionPage:
        """
        Resolve page contents.
        :return: NotionPage itself.
        """
        await self.nc.retrieve_child_blocks(self)
        return self

