from . import parameters
from .constants import Rarity
from .parameters import DEBUG


class HabitJournalingMixin:
    def on_init(self) -> None:
        self._currency["scroll"] = 0
        self._currency["scroll_fire"] = 0
        self._currency["scroll_earth"] = 0
        self._currency["scroll_water"] = 0
        self._currency["scroll_wind"] = 0
        self._currency["scroll_void"] = 0
        self.habit_journaling_undefined_items = {rar.value: 0 for rar in Rarity}
        self.habit_journaling_upgrade_tokens = {
            rar.value: 0 for rar in Rarity if rar != Rarity.VeryRare
        }
        self.habit_journaling_rewards: dict[str, int] = {
            "undefined_lores": 0,
            "undefined_themes": 0,
            "undefined_physical_reward": 0,
            "tzeentchian_scroll": 0,
            "tzeentchian_corruption": 0,
            "arcane_corruption": 0,
            "necromancer_corruption": 0,
            "legendary_tzeentch": 0,
            "legendary_arcane": 0,
            "legendary_necromancer": 0,
        }

        self.habit_journaling_corruptions = {
            "tzeentchian": 0,
            "arcane": 0,
            "necromancer": 0,
        }

        self.habit_journaling_obtained_moleskin_reward = False

    def habit_journaling(self, rarity: Rarity) -> None:
        match rarity:
            case Rarity.Nothing:
                pass
            case Rarity.Common:
                self._habit_journaling_common()
            case Rarity.Uncommon:
                self._habit_journaling_uncommon()
            case Rarity.Rare:
                self._habit_journaling_flip_coins_for_item(Rarity.Rare, 2)
                self._habit_journaling_add_reward("undefined_themes")
                self._habit_journaling_rare_roll_reward()
            case Rarity.VeryRare:
                self._habit_journaling_unlock_moleskin()
                p_jester = parameters.P.JESTER_HAT
                if not self._obtained_jester_hat and self._rng.choice(
                    [True, False],
                    p=[p_jester, 1 - p_jester],
                ):
                    self._obtained_jester_hat = True
                else:
                    self._habit_journaling_veryrare_rewards()
            case _:
                raise RuntimeError

    def _habit_journaling_add_item(self, rarity: Rarity) -> None:
        self.habit_journaling_undefined_items[rarity.value] += 1
        print(f"Obtained a journaling item of rarity '{rarity.value}'!")

    def _habit_journaling_add_upgrade_token(self, rarity: Rarity) -> None:
        self.habit_journaling_undefined_items[rarity.value] += 1
        print(f"Obtained an upgrade token of rarity '{rarity.value}'!")

    def _habit_journaling_add_reward(self, reward: str, n=1) -> None:
        self.habit_journaling_rewards[reward] += 1
        print(
            f"Obtained {'a' if n == 1 else n} journaling reward{'s' if n > 1 else ''} '{reward}'!"
        )

    def _habit_journaling_add_corruption(self, corruption: str, n=1) -> None:
        self.habit_journaling_corruptions[corruption] += n
        print(
            f"Your corruption level for '{corruption}' increased by {n}, it's at {self.habit_journaling_corruptions[corruption]} now."
        )

    def _habit_journaling_unlock_moleskin(self) -> None:
        if not self.habit_journaling_obtained_moleskin_reward:
            print("Unlocked the Moleskin!")
            self.habit_journaling_obtained_moleskin_reward = True

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

    def _habit_journaling_veryrare_rewards(self):
        self._habit_journaling_flip_coins_for_item(Rarity.VeryRare, 2)
        self._habit_journaling_add_item(Rarity.Rare)
        self._habit_journaling_flip_coins_for_item(Rarity.Uncommon)
        for _ in range(3):
            self._habit_journaling_flip_coins_for_item(Rarity.Common, 2)
        match self._rng.choice([1, 2, 3]):
            case 1:
                self._habit_journaling_add_reward("legendary_tzeentch")
                self._habit_journaling_add_corruption("tzeentchian", 10)
            case 2:
                self._habit_journaling_add_reward("legendary_arcane")
                self._habit_journaling_add_corruption("arcane", 10)
            case 3:
                self._habit_journaling_add_reward("legendary_necromancer")
                self._habit_journaling_add_corruption("necromancer", 10)
            case _:
                raise RuntimeError

    def _habit_journaling_common(self):
        self._habit_journaling_flip_coins_for_item(Rarity.Common, 2)

        choice = int(self._rng.choice([1, 2, 3, 4], p=[1 / 3, 1 / 3, 1 / 6, 1 / 6]))
        match choice:
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

    def _habit_journaling_uncommon(self):
        self._habit_journaling_add_reward("undefined_lores")
        self._habit_journaling_flip_coins_for_item(Rarity.Uncommon, 2)
        choice = int(self._rng.choice([1, 2, 3]))
        match choice:
            case 1:
                self._habit_journaling_flip_coins_for_item(Rarity.Common)
                if not DEBUG.SKIP_INPUT:
                    input_ = input(
                        "\n".join(
                            [
                                "Choose what reward you want:",
                                "1.) 5 Scrolls -> 1 random elemental scroll",
                                "2.) 8 Scrolls -> 1 particular elemental scroll",
                                "3.) +4 Scrolls",
                                "",
                            ]
                        )
                    )
                else:
                    input_ = self._rng.choice([1, 2, 3])
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
                if not DEBUG.SKIP_INPUT:
                    elem_scroll = input(
                        f"Enter an elemental scroll {'\n'.join(elem_scrolls)}\n"
                    )
                else:
                    elem_scroll = self._rng.choice(elem_scrolls)
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

    def _habit_journaling_rare_roll_reward(self):
        choice = int(self._rng.choice([1, 2, 3, 4], p=[1 / 4, 1 / 2, 1 / 8, 1 / 8]))
        match choice:
            case 1:
                self._habit_journaling_add_reward("tzeentchian_scroll")
                self._habit_journaling_add_corruption("tzeentchian", 3)
            case 2:
                self._habit_journaling_add_reward("undefined_physical_reward")
            case 3:
                self._habit_journaling_add_upgrade_token(Rarity.VeryRare)
            case 4:
                self._streak_recovery += 1
                self._habit_journaling_rare_roll_reward()
            case _:
                raise RuntimeError
