from __future__ import annotations
import attr
from typing import TYPE_CHECKING

from d2wiki.types import JSON
from .base import D2JsonModel

if TYPE_CHECKING:
    from ..wrapper import D2NotionWrapper

__all__ = ("NotionDatabase", )


@attr.s
class NotionDatabase(D2JsonModel):
    id: str = attr.ib(repr=True, eq=True, hash=True)

    @classmethod
    def from_json(cls, **json: str | D2NotionWrapper) -> NotionDatabase:
        return cls(
            nc=json["nc"],
            id=json["id"],
        )

    def to_json(self) -> JSON:
        obj = {
            "id": self.id
        }
        return obj

    @property
    def embed(self) -> None:
        """
        Not Embeddable model
        """
        return None
