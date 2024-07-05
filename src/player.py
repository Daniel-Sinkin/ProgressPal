import numpy as np

from .constants import Rarity
from .habit_journaling import HabitJournalingMixin
from .habit_physical import HabitPhysicalMixin


class Player(HabitJournalingMixin, HabitPhysicalMixin):
    _rng = np.random.default_rng()

    def __init__(self, name: str):
        self._name: str = name
        self.on_init()
        super().on_init()

    def on_init(self) -> None:
        self._xp: int = 0
        self._currency: dict[str, int] = {}
        self._streak_recovery = 0
        self._obtained_jester_hat = False

    def pull_rarities(self, n: int = 1) -> list[Rarity]:
        return [
            Rarity(c) for c in self._rng.choice(list(Rarity), size=n, p=Rarity.get_ps())
        ]

    def increase_currency(self, currency: str, amount: int = 1) -> None:
        current_amount = self._currency[currency]
        print(f"{currency} <- {current_amount + amount} = {current_amount}+{amount}")
        self._currency[currency] += amount

    def decrease_currency(self, currency: str, amount: int) -> None:
        current_amount = int(self._currency[currency])
        new_amount: int = max(0, self._currency[currency] - amount)
        print(f"{currency} <- {new_amount} = {current_amount}-{amount}")
        self._currency[currency] += amount

    def trade_currency(
        self, currency_remove: str, amount_remove: int, currency_add: str, amount_add
    ) -> bool:
        """Returns True if trade successful and False else"""
        if currency_remove == currency_add:
            raise RuntimeError(f"{currency_remove=}==currency2")
        if amount_remove <= 0 or amount_add <= 0:
            raise RuntimeError(
                f"Improper trade amounts {amount_remove=}, {amount_add=}"
            )
        if self._currency[currency_remove] < amount_remove:
            return False

        print(
            "Traded {amount_remove} {currency_remove} for {amount_add} {currency_add}"
        )
        self.decrease_currency(currency_remove, amount_remove)
        self.increase_currency(currency_add, amount_add)
        return True

    def flip_coins(self, n) -> list[str]:
        result: list[str] = self._rng.choice(["H", "T"], size=n)
        print(f"Flipped {n} coin(s) and got {result}")
        return result

    def flip_coins_for_heads(self, n) -> bool:
        return all(self.flip_coins(n) == ["H"] * n)
