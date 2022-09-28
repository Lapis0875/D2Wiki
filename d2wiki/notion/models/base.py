from __future__ import annotations
from abc import abstractmethod

import attr
from discord import Embed

from d2wiki.types import JsonSerializable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..wrapper import D2NotionWrapper


__all__ = ("D2JsonModel", )


@attr.s
class D2JsonModel(JsonSerializable):
    """
    Base class of D2 Model from Notion API response.
    """
    nc: D2NotionWrapper = attr.ib(repr=False, eq=False, hash=False)

    @property
    @abstractmethod
    def embed(self) -> Embed | None:
        """
        Return discord Embed object of this model.
        :return: discord.Embed object or None if this model is not embeddable.
        """
        ...
