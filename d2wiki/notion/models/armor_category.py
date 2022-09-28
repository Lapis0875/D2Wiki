from enum import Enum


__all__ = ("D2ArmorCategory", )


class D2ArmorCategory(Enum):
    """
    Destiny2 Armor Category.
    """
    HEAD = "머리"
    ARM = "팔"
    CHEST = "가슴"
    LEG = "다리"
    CLASS = "직업"
