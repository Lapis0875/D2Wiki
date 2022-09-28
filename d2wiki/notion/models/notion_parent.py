from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

import attr

from d2wiki.types import JSON
from .base import D2JsonModel

if TYPE_CHECKING:
    from ..wrapper import D2NotionWrapper
    from .notion_block import NotionBlock
    from .notion_page import NotionPage
    from .notion_database import NotionDatabase
    PARENT_TYPE = NotionBlock | NotionDatabase | NotionPage

__all__ = ("NotionParentType", "NotionParent")


class NotionParentType(Enum):
    """
    Notion Parent Type Enum.
    """
    DATABASE = "database_id"
    PAGE = "page_id"
    BLOCK = "block_id"
    WORKSPACE = "workspace"


@attr.s
class NotionParent(D2JsonModel):
    """
    Notion Parent Model.
    """
    type: NotionParentType = attr.ib(repr=True, eq=False, hash=False)
    page_id: str | None = attr.ib(default=None, repr=True, eq=False, hash=False)
    database_id: str | None = attr.ib(default=None, repr=True, eq=False, hash=False)
    workspace: bool | None = attr.ib(default=None, repr=True, eq=False, hash=False)

    @classmethod
    def from_json(cls, **json: str | D2NotionWrapper) -> NotionParent:
        return cls(
            nc=json["nc"],
            type=NotionParentType(json["type"]),
            page_id=json["page_id"] if json["type"] == "page_id" else None,
            database_id=json["database_id"] if json["type"] == "database_id" else None,
            workspace=json["workspace"] if json["type"] == "workspace" else None
        )

    def to_json(self) -> JSON:
        obj = {
            "type": self.type.value
        }
        match self.type:
            case NotionParentType.PAGE:
                obj["page_id"] = self.page_id
            case NotionParentType.DATABASE:
                obj["database_id"] = self.database_id
            case NotionParentType.WORKSPACE:
                obj["workspace"] = self.workspace
        return obj

    @property
    def embed(self) -> None:
        """
        Not Embeddable model.
        """
        return None

    async def retrieve_parent(self) -> PARENT_TYPE:
        """
        Retrieve parent object as python model.
        :return: full model based on id of parent object.
        """
        match self.type:
            case NotionParentType.PAGE:
                return await self.nc.retrieve_page(self.page_id)
            case NotionParentType.DATABASE:
                return await self.nc.retrieve_database(self.database_id)
            case NotionParentType.WORKSPACE:
                return await self.nc.get_workspace()