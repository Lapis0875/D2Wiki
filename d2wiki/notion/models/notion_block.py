from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, cast

import attr

from d2wiki.types import JSON, JSON_VALUES, JsonSerializable
from d2wiki.utils.dtutil import notion2dt
from .base import D2JsonModel
from .notion_color import NotionColor
from .rich_text import RichText
from .notion_user import PartialNotionUser
from .notion_parent import NotionParent

if TYPE_CHECKING:
    from ..wrapper import D2NotionWrapper
    from . import NotionPage
    BLOCK_PARENT_TYPE = NotionPage | NotionParent

__all__ = ("NotionBlockType", "NotionBlock")


class NotionBlockType(Enum):
    """
    Notion Block Type
    """
    PARAGRAPH = "paragraph"
    HEADING_1 = "heading_1"
    HEADING_2 = "heading_2"
    HEADING_3 = "heading_3"
    BULLETED_LIST_ITEM = "bulleted_list_item"
    NUMBERED_LIST_ITEM = "numbered_list_item"
    TO_DO = "to_do"
    TOGGLE = "toggle"
    CHILD_PAGE = "child_page"
    EMBED = "embed"
    IMAGE = "image"
    VIDEO = "video"
    FILE = "file"
    PDF = "pdf"
    BOOKMARK = "bookmark"
    CALL_OUT = "callout"
    QUOTE = "quote"
    EQUATION = "equation"
    DIVIDER = "divider"
    TABLE_OF_CONTENTS = TOC = "table_of_contents"
    COLUMN = "column"
    COLUMN_LIST = "column_list"
    LINK_PREVIEW = "link_preview"
    SYNCED_BLOCK = "synced_block"
    TEMPLATE = "template"
    LINK_TO_PAGE = "link_to_page"
    TABLE = "table"
    TABLE_ROW = "table_row"
    UNSUPPORTED = "unsupported"
    CODE = "code"       # why this is not listed in docs?


class NotionBlockData(JsonSerializable):
    """
    Base class of all types of Notion Block Data.
    """


@attr.s
class NotionParagraph(NotionBlockData):
    rich_text: list[RichText] = attr.ib(repr=True, eq=False, hash=False)
    color: NotionColor = attr.ib(repr=True, eq=False, hash=False)
    children: list[NotionBlock] = attr.ib(repr=False, eq=False, hash=False)

    @classmethod
    def from_json(cls, **json: str | bool | JSON) -> NotionParagraph:
        return cls(
            rich_text=[RichText.from_json(**i) for i in json["rich_text"]],
            color=NotionColor(json["color"]),
            children=[NotionBlock.from_json(**block) for block in json["children"]] if "children" in json else []
        )

    def to_json(self) -> JSON:
        return {
            "rich_text": [i.to_json() for i in self.rich_text],
            "color": self.color.value,
            "children": [i.to_json() for i in self.children]
        }


def parse_notion_data(block_type: NotionBlockType, json: JSON_VALUES) -> NotionBlockData | None:
    match block_type:
        case NotionBlockType.PARAGRAPH:
            return NotionParagraph.from_json(**json)
        case _:
            return None


@attr.define(slots=True)
class NotionBlock(D2JsonModel):
    id: str = attr.ib(repr=True, eq=True, hash=True)
    parent: NotionParent = attr.ib(repr=True, eq=False, hash=False)
    type: NotionBlockType = attr.ib(repr=True, eq=False, hash=False)
    created_time: datetime = attr.ib(repr=True, eq=False, hash=False)
    created_by: PartialNotionUser = attr.ib(repr=True, eq=False, hash=False)
    last_edited_time: datetime = attr.ib(repr=True, eq=False, hash=False)
    last_edited_by: PartialNotionUser = attr.ib(repr=True, eq=False, hash=False)
    archived: bool = attr.ib(repr=True, eq=False, hash=False)
    has_children: bool = attr.ib(repr=True, eq=False, hash=False)
    children: list[NotionBlock] = attr.ib(repr=True, eq=False, hash=False)
    data: NotionBlockData = attr.ib(repr=True, eq=False, hash=False)
    full_parent: BLOCK_PARENT_TYPE | None = attr.ib(init=True, repr=True, eq=False, hash=False)

    @classmethod
    def from_json(cls, _parent: BLOCK_PARENT_TYPE = None, _children: list[NotionBlock] = None, **json: str | bool | D2NotionWrapper | JSON) -> NotionBlock:
        if _parent is not None:
            json_parent = json["parent"]
            assert _parent.id == (json_parent.get("page_id") or json_parent.get("block_id")), "Invalid parent object passed."
        block_type = NotionBlockType(json["type"])
        data = parse_notion_data(block_type, json[cast(str, block_type.value)])
        assert data is not None, "Invalid block data. This should not happen."

        nc = json["nc"]
        return cls(
            nc=nc,
            id=json["id"],
            parent=NotionParent.from_json(nc=nc, **json["parent"]),
            type=block_type,
            created_time=notion2dt(json["created_time"]),
            created_by=PartialNotionUser.from_json(nc=nc, **json["created_by"]),
            last_edited_time=notion2dt(json["last_edited_time"]),
            last_edited_by=PartialNotionUser.from_json(nc=nc, **json["last_edited_by"]),
            archived=json["archived"],
            has_children=json["has_children"],
            children=[] if _children is None else _children,
            data=data,
            full_parent=_parent
        )

    def to_json(self) -> JSON:
        obj = {
            "id": self.id,
            "parent": self.parent.to_json(),
            "type": self.type.value,
            "created_time": self.created_time.isoformat(),
            "created_by": self.created_by.to_json(),
            "last_edited_time": self.last_edited_time.isoformat(),
            "last_edited_by": self.last_edited_by.to_json(),
            "archived": self.archived,
            "has_children": self.has_children
        }
        if len(self.children) > 0:
            obj["children"] = [child.to_json() for child in self.children]
        return obj

    @property
    def embed(self) -> None:
        """
        Not Embeddable model.
        """
        return None

    def set_parent(self, parent: BLOCK_PARENT_TYPE) -> NotionBlock:
        """
        Set parent of this Notion Block.
        :param parent: Parent object of this NotionBlock. Either NotionPage or NotionBlock.
        :return: NotionBlock object itself for method chaining.
        """
        self.__parent = parent
        return self

    async def full_parent(self) -> BLOCK_PARENT_TYPE:
        """
        Return Full object of this block's parent.
        """
        if self.__parent is None:
            self.__parent = await self.parent.retrieve_parent()
        return self.__parent

    async def retrieve_children(self) -> NotionBlock:
        """
        Retrieve children of this block.
        :return: NotionBlock object itself for method chaining.
        """
        if self.has_children:
            await self.nc.retrieve_child_blocks(self)
        return self
