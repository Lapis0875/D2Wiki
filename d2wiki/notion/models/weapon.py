from enum import Enum

__all__ = ("D2WeaponAmmo", "D2WeaponSlot", "D2WeaponCategory")


class D2WeaponAmmo(Enum):
    """
    Destiny2 Weapon Ammo
    """
    MAIN = "주 무기"
    SPECIAL = "특수"
    POWER = "중화기"


class D2WeaponSlot(Enum):
    """
    Destiny2 Weapon Slot
    """
    KINETIC_OR_STASIS = SLOT1 = "물리/시공"
    ENERGY = SLOT2 = "에너지"
    POWER = SLOT3 = "중화기"


class D2WeaponCategory(Enum):
    """
    Destiny2 Weapon Category.
    """
    AUTO_RIFLE = "자동 소총"
    HAND_CANNON = "핸드 캐논"
    PULSE_RIFLE = "파동 소총"
    SCOUT_RIFLE = "정찰 소총"
    SIDEARM = "보조 무기"
    SUB_MACHINE_GUN = SMG = "기관단총"
    SHOTGUN = "산탄총"
    PRECISION_SLUG_SHOTGUN = "정밀 납탄 산탄총"
    SNIPER_RIFLE = "저격 소총"
    FUSION_RIFLE = "융합 소총"
    LINEAR_FUSION_RIFLE = "선형 융합 소총"
    ROCKET_LAUNCHER = "로켓 발사기"
    BOW = "활"
    SPECIAL_AMMO_GRENADE_LAUNCHER = "특수 탄약 유탄 발사기"
    HEAVY_AMMO_GRENADE_LAUNCHER = "중화기 탄약 유탄 발사기"
    TRACE_RIFLE = "추적 소총"
    Sword = "검"
    MACHINE_GUN = "기관총"


