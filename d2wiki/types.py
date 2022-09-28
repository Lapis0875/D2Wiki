from __future__ import annotations

from abc import ABCMeta
from typing import Union, Callable, Any, Coroutine

JSON_VALUES = Union[str, int, bool, float, list, dict, None]
JSON = dict[str, JSON_VALUES]
Function = Callable[[Any, ...], Any]
CoroutineFunction = Callable[[Any, ...], Coroutine[Any, Any, Any]]


class JsonSerializable(metaclass=ABCMeta):
    @classmethod
    def from_json(cls, **json: JSON_VALUES) -> JsonSerializable: ...
    def to_json(self) -> JSON: ...
