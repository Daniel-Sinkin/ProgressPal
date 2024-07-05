from enum import StrEnum, auto
from typing import TypedDict

import numpy as np


class Rarity(StrEnum):
    Nothing = auto()
    Common = auto()
    Uncommon = auto()
    Rare = auto()
    VeryRare = auto()

    def __lt__(self, other):
        if not isinstance(other, Rarity):
            return NotImplemented
        if self == other:
            return False
        match self:
            case Rarity.Nothing:
                return True
            case Rarity.Common:
                return other in [Rarity.Uncommon, Rarity.Rare, Rarity.VeryRare]
            case Rarity.Uncommon:
                return other in [Rarity.Rare, Rarity.VeryRare]
            case Rarity.Rare:
                return other in [Rarity.VeryRare]
            case Rarity.VeryRare:
                return False
            case _:
                raise RuntimeError

    def __eq__(self, other):
        if not isinstance(other, Rarity):
            return NotImplemented
        return self._value_ == other._value_

    def prettify(self) -> str:
        match self:
            case Rarity.Nothing:
                return "...a dud..."
            case Rarity.Common:
                return "[Common]"
            case Rarity.Uncommon:
                return "🔷Uncommon"
            case Rarity.Rare:
                return "💫 Rare 💫"
            case Rarity.VeryRare:
                return "🌟🌟🌟 VeryRare 🌟🌟🌟"

    @property
    def p(self) -> float:
        match self:
            case Rarity.Nothing:
                return 50 / 100
            case Rarity.Common:
                return 35 / 100
            case Rarity.Uncommon:
                return 11 / 100
            case Rarity.Rare:
                return 3 / 100
            case Rarity.VeryRare:
                return 1 / 100

    @staticmethod
    def get_ps() -> list[float]:
        return [rar.p for rar in Rarity]


assert np.isclose(sum([rar.p for rar in Rarity]), 1.0)


class CurrencyDict(TypedDict):
    scroll: int
    scroll_fire: int
    scroll_earth: int
    scroll_water: int
    scroll_wind: int
    scroll_void: int
    adventure_token_bronze: int
    adventure_token_silver: int
    adventure_token_gold: int
    insight: int
    insight_eldritch: int
