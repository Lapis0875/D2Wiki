from enum import Enum, auto
from typing import Any


class NotionColor(Enum):
    """
    Notion Colors
    """
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
        return name.lower()

    DEFAULT = auto()
    GRAY = auto()
    BROWN = auto()
    ORANGE = auto()
    YELLOW = auto()
    GREEN = auto()
    BLUE = auto()
    PURPLE = auto()
    PINK = auto()
    RED = auto()
    GRAY_BACKGROUND = auto()
    BROWN_BACKGROUND = auto()
    ORANGE_BACKGROUND = auto()
    YELLOW_BACKGROUND = auto()
    GREEN_BACKGROUND = auto()
    BLUE_BACKGROUND = auto()
    PURPLE_BACKGROUND = auto()
    PINK_BACKGROUND = auto()
    RED_BACKGROUND = auto()
