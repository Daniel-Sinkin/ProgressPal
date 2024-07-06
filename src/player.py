import time

import numpy as np
import ujson as json

from .constants import Habit, Rarity
from .habit_journaling import HabitJournalingMixin
from .habit_physical import HabitPhysicalMixin
from .util import clear_screen, pulling_sound


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

    def __str__(self) -> str:
        return f"Player '{self._name}' has {self._xp} xp and {self._currency}"

    def __repr__(self) -> str:
        return self.__str__()

    def save(self) -> None:
        print("Saving player data...")
        with open(f"player_{self._name}.json", "w") as f:
            f.write(self.to_json())

    def serialize(self) -> dict[str, any]:
        player_data = {
            "name": self._name,
            "xp": self._xp,
            "currency": self._currency,
            "streak_recovery": self._streak_recovery,
            "obtained_jester_hat": self._obtained_jester_hat,
        }

        # Serialize HabitJournalingMixin data
        habit_journaling_data = {
            "currency": {
                "scroll": self._currency.get("scroll", 0),
                "scroll_fire": self._currency.get("scroll_fire", 0),
                "scroll_earth": self._currency.get("scroll_earth", 0),
                "scroll_water": self._currency.get("scroll_water", 0),
                "scroll_wind": self._currency.get("scroll_wind", 0),
                "scroll_void": self._currency.get("scroll_void", 0),
            },
            "undefined_items": self.habit_journaling_undefined_items,
            "upgrade_tokens": self.habit_journaling_upgrade_tokens,
            "rewards": self.habit_journaling_rewards,
            "corruptions": self.habit_journaling_corruptions,
            "obtained_moleskin_reward": self.habit_journaling_obtained_moleskin_reward,
        }
        player_data["habit_journaling"] = habit_journaling_data

        return player_data

    @classmethod
    def deserialize(cls, data: dict[str, any]) -> "Player":
        player = cls(data["name"])
        player._xp = data["xp"]
        player._currency = data["currency"]
        player._streak_recovery = data["streak_recovery"]
        player._obtained_jester_hat = data["obtained_jester_hat"]

        # Deserialize HabitJournalingMixin data
        hj_data = data["habit_journaling"]
        player._currency.update(hj_data["currency"])
        player.habit_journaling_undefined_items = hj_data["undefined_items"]
        player.habit_journaling_upgrade_tokens = hj_data["upgrade_tokens"]
        player.habit_journaling_rewards = hj_data["rewards"]
        player.habit_journaling_corruptions = hj_data["corruptions"]
        player.habit_journaling_obtained_moleskin_reward = hj_data[
            "obtained_moleskin_reward"
        ]

        return player

    def to_json(self, indent=4) -> str:
        return json.dumps(self.serialize(), indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> "Player":
        data: dict[str, any] = json.loads(json_str)
        return cls.deserialize(data)

    def pull_rarities(self, n: int = 1) -> list[Rarity]:
        return [
            Rarity(c) for c in self._rng.choice(list(Rarity), size=n, p=Rarity.get_ps())
        ]

    def complete_habit(self, habit: Habit) -> None:
        self.increase_xp(10)

        n_dots_max = 50
        for n_dots in range(n_dots_max):
            time.sleep(max(0.25 - 0.005 * (n_dots + 2), 0.025))
            print(
                "+++" if n_dots & 1 == 0 else "---",
                "." * n_dots + " " * (n_dots_max - n_dots - 1) + "|",
                "+++" if n_dots & 1 == 0 else "---",
                end="\r",
            )
            if n_dots == (9 * n_dots_max) // 10:
                pulling_sound.play()
        clear_screen()

        rarity: Rarity = self.pull_rarities(1)[0]
        print(f"Pulled '{rarity.prettify()}'")

        match habit:
            case Habit.Journaling:
                self.habit_journaling(rarity)
            case Habit.Physical:
                self.habit_physical(rarity)
            case _:
                raise RuntimeError(f"Unknown habit {habit=}")

    def increase_currency(self, currency: str, amount: int = 1) -> None:
        current_amount = self._currency[currency]
        print(f"{currency} <- {current_amount + amount} = {current_amount}+{amount}")
        self._currency[currency] += amount

    def decrease_currency(self, currency: str, amount: int) -> None:
        current_amount = int(self._currency[currency])
        new_amount: int = max(0, self._currency[currency] - amount)
        print(f"{currency} <- {new_amount} = {current_amount}-{amount}")
        self._currency[currency] += amount

    def increase_xp(self, amount: int = 10) -> None:
        print(f"XP <- {self._xp + amount} = {self._xp}+{amount}")
        self._xp += amount

    def trade_currency(
        self,
        currency_remove: str,
        amount_remove: int,
        currency_add: str,
        amount_add: int,
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

    def flip_coins(self, n: int = 1) -> list[str]:
        result: list[str] = self._rng.choice(["H", "T"], size=n)
        if n == 1:
            print(f"Flipped a coin and got {result}.")
        else:
            print(f"Flipped {n} coins and got {result}.")
        return result

    def flip_coins_for_heads(self, n: int = 1) -> bool:
        return all(self.flip_coins(n) == ["H"] * n)
