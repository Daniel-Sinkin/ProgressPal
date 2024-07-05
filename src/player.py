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


class HabitJournalingMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_init_habit_journaling()

    def on_init_habit_journaling(self):
        self.habit_journaling_undefined_items = {rar.value: 0 for rar in Rarity}
        self.habit_journaling_undefined_items.update(
            {"legendary_tzeentch": 0, "legendary_arcane": 0, "legendary_necromancer": 0}
        )
        self.habit_journaling_undefined_lores = 0
        self.habit_journaling_undefined_themes = 0
        self.habit_journaling_undefined_physical_reward = 0
        self.habit_journaling_upgrade_tokens = {
            Rarity.Nothing.value: 0,
            Rarity.Common.value: 0,
            Rarity.Uncommon.value: 0,
            Rarity.Rare.value: 0,
        }
        self.habit_journaling_tzeentchian_scroll = 0
        self.habit_journaling_tzeentchian_corruption = 0
        self.habit_journaling_arcane_corruption = 0
        self.habit_journaling_necromancer_corruption = 0
        self.habit_journaling_obtained_moleskin_reward = False

    def habit_journaling(self, rarity: Rarity):
        match rarity:
            case Rarity.Nothing:
                pass
            case Rarity.Common:
                self._habit_journaling_common()
            case Rarity.Uncommon:
                self._habit_journaling_uncommon()
            case Rarity.Rare:
                self._habit_journaling_flip_coins_for_item(Rarity.Rare, 2)
                self.habit_journaling_undefined_themes += 1

                self._habit_journaling_rare_roll_reward()
            case Rarity.VeryRare:
                self.habit_journaling_obtained_moleskin_reward = True
                if not self._obtained_jester_hat and self._rng.choice(
                    [True, False], p=[0.05, 0.95]
                ):
                    self._obtained_jester_hat = True
                    return

                self._habit_journaling_flip_coins_for_item(Rarity.VeryRare, 2)
                self._habit_journaling_add_item(Rarity.Rare)
                self._habit_journaling_flip_coins_for_item(Rarity.Uncommon)
                for _ in range(3):
                    self._habit_journaling_flip_coins_for_item(Rarity.Common, 2)
                match self._rng.choice([1, 2, 3]):
                    case 1:
                        self._habit_journaling_add_item("legendary_tzeentch")
                        self.habit_journaling_tzeentchian_corruption += 10
                    case 2:
                        self._habit_journaling_add_item("legendary_arcane")
                        self.habit_journaling_arcane_corruption += 10
                    case 3:
                        self._habit_journaling_add_item("legendary_necromancer")
                        self.habit_journaling_necromancer_corruption += 10
                    case _:
                        raise RuntimeError
            case _:
                raise RuntimeError

    def _habit_journaling_uncommon(self):
        self.habit_journaling_undefined_lores += 1
        self._habit_journaling_flip_coins_for_item(Rarity.Uncommon, 2)
        match self._rng.choice([1, 2, 3]):
            case 1:
                self._habit_journaling_flip_coins_for_item(Rarity.Common)
                input_ = input(
                    "\n".join(
                        [
                            "1.) 5 Scrolls -> 1 random elemental scroll",
                            "2.) 8 Scrolls -> 1 particular elemental scroll",
                            "3.) +4 Scrolls",
                        ]
                    )
                )
                try:
                    input_ = int(input_)
                except ValueError:
                    print(
                        "Couldn't convert {input_=} to an int, choosing +4 Scrolls as a fallback."
                    )
                    input_ = 3
                self._habit_journaling_uncommon_match_input(input_)
            case 2:
                elem_scroll = self._habit_journaling_get_random_elemental_scroll()
                self.increase_currency(elem_scroll)
                if self.flip_coins_for_heads(1):
                    self.habit_journaling_upgrade_tokens[Rarity.Common.value]
            case 3:
                self._habit_journaling_flip_coins_for_item(Rarity.Common)
                self._habit_journaling_flip_coins_for_item(Rarity.Common)

    def _habit_journaling_uncommon_match_input(self, input_):
        match input_:
            case 1:
                elem_scroll = self._habit_journaling_get_random_elemental_scroll()
                self.trade_currency("scroll", 5, elem_scroll, 1)
            case 2:
                elem_scrolls = [
                    "scroll_" + x for x in ["fire", "earth", "water", "wind", "void"]
                ]
                elem_scroll = input(
                    f"Enter an elemental scroll {'\n'.join(elem_scrolls)}"
                )
                if elem_scroll not in elem_scrolls:
                    print(
                        f"Invalid input {elem_scroll} for elemental scroll, falling back to 'scroll_fire'"
                    )
                    elem_scroll = "scroll_fire"
                self.increase_currency(elem_scroll)
            case 3:
                self.increase_currency("scroll", 4)
            case _:
                raise RuntimeError

    def _habit_journaling_common(self):
        self._habit_journaling_flip_coins_for_item(Rarity.Common, 2)

        match self._rng.choice([1, 2, 3, 4], p=[1 / 3, 1 / 3, 1 / 6, 1 / 6]):
            case 1:
                self.increase_currency("scroll", 4)
            case 2:
                elem_scroll = self._habit_journaling_get_random_elemental_scroll()
                self.increase_currency(elem_scroll)
            case 3:
                self._habit_journaling_flip_coins_for_item(Rarity.Uncommon, 2)
            case 4:
                self._habit_journaling_flip_coins_for_item(Rarity.Common)
            case _:
                raise RuntimeError

    def _habit_journaling_rare_roll_reward(self):
        match self._rng.choice([1, 2, 3, 4], p=[1 / 4, 1 / 2, 1 / 8, 1 / 8]):
            case 1:
                self.habit_journaling_tzeentchian_scroll += 1
                self.habit_journaling_tzeentchian_corruption += 3
            case 2:
                self.habit_journaling_undefined_physical_reward += 1
            case 3:
                self.habit_journaling_upgrade_tokens[Rarity.VeryRare.value] += 1
            case 4:
                self._streak_recovery += 1
                self._habit_journaling_rare_roll_reward()

    def _habit_journaling_add_item(self, rarity: Rarity) -> None:
        self.habit_journaling_undefined_items[rarity.value] += 1

    def _habit_journaling_flip_coins_for_item(self, rarity: Rarity, n: int = 1) -> None:
        if self.flip_coins_for_heads(n):
            self._habit_journaling_add_item(rarity)

    def _habit_journaling_get_random_elemental_scroll(self) -> str:
        return str(
            self._rng.choice(
                [
                    "scroll_fire",
                    "scroll_earth",
                    "scroll_water",
                    "scroll_wind",
                    "scroll_void",
                ],
                p=[0.24] * 4 + [0.04],
            )
        )


class Player(HabitJournalingMixin):
    _rng = np.random.default_rng()

    def __init__(self, name: str):
        self._name: str = name
        self.on_init()

    def on_init(self):
        self._xp: int = 0
        self._currency: CurrencyDict = CurrencyDict(
            scroll=0,
            scroll_fire=0,
            scroll_earth=0,
            scroll_water=0,
            scroll_wind=0,
            scroll_void=0,
            adventure_token_bronze=0,
            adventure_token_silver=0,
            adventure_token_gold=0,
            insight=0,
            insight_eldritch=0,
        )
        self._streak_recovery = 0
        self._obtained_jester_hat = False

    def pull_rarities(self, n: int = 1) -> Rarity | list[Rarity]:
        return self._rng.choice(list(Rarity), size=n, p=Rarity.get_ps())

    def increase_currency(self, currency: str, amount: int = 1) -> None:
        current_amount = self._currency[currency]
        print(f"{currency} <- {current_amount + amount} = {current_amount}+{amount}")
        self._currency[currency] += amount

    def decrease_currency(self, currency: str, amount: int) -> None:
        current_amount = self._currency[currency]
        new_amount = max(0, self._currency[currency] - amount)
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

        self.decrease_currency(currency_remove, amount_remove)
        self.increase_currency(currency_add, amount_add)
        return True

    def flip_coins(self, n) -> None:
        return self._rng.choice(["H", "T"], size=n)

    def flip_coins_for_heads(self, n) -> bool:
        return all(self.flip_coins(n) == ["H"] * n)

    def roll_for_jester_hat(self) -> None:
        if not self._obtained_jester_hat and self._rng.choice(
            [True, False], p=[0.95, 0.05]
        ):
            self._obtained_jester_hat = True
