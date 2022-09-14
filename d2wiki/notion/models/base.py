from __future__ import annotations
from abc import ABCMeta, abstractmethod

from d2wiki.types import JSON


class D2JsonModel(metaclass=ABCMeta):
    """
    Base class of D2 Model from Notion API response.
    """
    @classmethod
    @abstractmethod
    def from_json(cls, json: JSON) -> D2JsonModel:
        ...

    @abstractmethod
    def to_json(self) -> JSON:
        ...
