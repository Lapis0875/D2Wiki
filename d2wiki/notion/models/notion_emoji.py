from __future__ import annotations
import attr
from discord import Embed, Color
from d2wiki.types import JSON

__all__ = ("NotionEmoji", )


@attr.s(slots=True)
class NotionEmoji:
    """
    Notion Emoji Model.
    """
    emoji: str = attr.ib(repr=True, eq=True, hash=True)  # emoji string

    @classmethod
    def from_json(cls, **json: str) -> NotionEmoji:
        return cls(emoji=json["emoji"])

    def to_json(self) -> JSON:
        return {"emoji": self.emoji}

    @property
    def embed(self) -> Embed:
        return Embed(title="Notion Emoji", color=Color.brand_green()).add_field(name="emoji", value=self.emoji)
