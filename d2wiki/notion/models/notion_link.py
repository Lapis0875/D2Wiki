from __future__ import annotations
from typing import Literal

import attr

from d2wiki.types import JsonSerializable, JSON_VALUES, JSON

__all__ = ("NotionLink", )


@attr.s(slots=True)
class NotionLink(JsonSerializable):
    """
    Notion Link object.
    Reference : https://developers.notion.com/reference/rich-text#link-objects
    """
    url: str = attr.ib(repr=True, eq=True, hash=True)
    type: Literal["url"] = attr.ib(default="url", repr=True, eq=True, hash=True)

    @classmethod
    def from_json(cls, **json: JSON_VALUES) -> NotionLink:
        return cls(url=json["url"])

    def to_json(self) -> JSON:
        return {
            "type": self.type,
            "url": self.url
        }
