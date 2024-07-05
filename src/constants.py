from enum import StrEnum, auto

import numpy as np

from . import parameters


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
                return parameters.P.NOTHING
            case Rarity.Common:
                return parameters.P.COMMON
            case Rarity.Uncommon:
                return parameters.P.UNCOMMON
            case Rarity.Rare:
                return parameters.P.RARE
            case Rarity.VeryRare:
                return parameters.P.VERY_RARE

    @staticmethod
    def get_ps() -> list[float]:
        return [rar.p for rar in Rarity]


assert np.isclose(sum(Rarity.get_ps()), 1.0)
