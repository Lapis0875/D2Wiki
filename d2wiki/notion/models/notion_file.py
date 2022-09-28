from __future__ import annotations
from datetime import datetime
from enum import Enum

import attr
from discord import Embed

from d2wiki.types import JSON

__all__ = ("NotionFileType", "NotionFileProperty", "NotionExternalProperty", "NotionFile")


class NotionFileType(Enum):
    """
    Notion File Type Enum.
    """
    EXTERNAL = "external"
    FILE = "file"


@attr.s
class NotionFileProperty:
    """
    Property for files hosted by Notion.
    """
    url: str = attr.ib(repr=True, eq=False, hash=False) # Authenticated S3 URL to the file. The file URL will be valid for 1 hour but updated links can be requested if required.
    expiry_time: datetime = attr.ib(repr=True, eq=False, hash=False)

    @classmethod
    def from_json(cls, **json: str) -> NotionFileProperty:
        return cls(url=json["url"], expiry_time=datetime.fromisoformat(json["expiry_time"]))

    def to_json(self) -> JSON:
        return {
            "url": self.url,
            "expiry_time": self.expiry_time.isoformat()
        }


@attr.s
class NotionExternalProperty:
    """
    Property for externally hosted files.
    """
    url: str = attr.ib(repr=True, eq=False, hash=False) # Link to the externally hosted content.

    @classmethod
    def from_json(cls, **json) -> NotionExternalProperty:
        return cls(url=json["url"])

    def to_json(self) -> JSON:
        return {
            "url": self.url
        }


@attr.s(slots=True)
class NotionFile:
    """
    Notion File Model.
    """
    type: NotionFileType = attr.ib(repr=True, eq=True, hash=True)
    file: NotionFileProperty | None = attr.ib(default=None, repr=True, eq=False, hash=False)
    external: NotionExternalProperty | None = attr.ib(default=None, repr=True, eq=False, hash=False)

    @classmethod
    def from_json(cls, **json: str | JSON) -> NotionFile:
        return cls(
            type=NotionFileType(json["type"]),
            file=NotionFileProperty.from_json(**json["file"]) if json["type"] == NotionFileType.FILE.value else None,
            external=NotionExternalProperty.from_json(**json["external"]) if json["type"] == NotionFileType.EXTERNAL.value else None
        )

    def to_json(self) -> JSON:
        obj = {
            "type": self.type.value
        }
        if self.type == NotionFileType.FILE:
            obj["file"] = self.file.to_json()
        else:
            obj["external"] = self.external.to_json()
        return obj

    @property
    def embed(self) -> Embed | None:
        return None

    @property
    def property(self) -> NotionFileProperty | NotionExternalProperty:
        """
        Return property based on file type.
        :return:
        """
        return self.external if self.type == NotionFileType.EXTERNAL else self.file
