from .constants import Rarity


class HabitPhysicalMixin:
    def on_init(self) -> None:
        self._currency["adventure_token_bronze"] = 0
        self._currency["adventure_token_silver"] = 0
        self._currency["adventure_token_gold"] = 0
        self.habit_physical_undefined_items: dict[str, int] = {
            rar.value: 0 for rar in Rarity
        }
        self.habit_physical_undefined_lores = 0
        self.habit_physical_undefined_physical_reward = 0
        self.habit_physical_upgrade_tokens: dict[str, int] = {
            Rarity.Nothing.value: 0,
            Rarity.Common.value: 0,
            Rarity.Uncommon.value: 0,
            Rarity.Rare.value: 0,
        }

    def habit_physical(self, rarity: Rarity) -> None:
        match rarity:
            case Rarity.Nothing:
                pass
            case Rarity.Common:
                self._habit_physical_common()
            case Rarity.Uncommon:
                self._habit_physical_uncommon()
            case Rarity.Rare:
                self._habit_physical_flip_coins_for_item(Rarity.Rare, 2)
                self.habit_physical_undefined_themes += 1

                self._habit_physical_rare_roll_reward()
            case Rarity.VeryRare:
                self.habit_physical_obtained_moleskin_reward = True
                if not self._obtained_jester_hat and self._rng.choice(
                    [True, False], p=[0.05, 0.95]
                ):
                    self._obtained_jester_hat = True

                self._habit_physical_veryrare_rewards()
            case _:
                raise RuntimeError

    def _habit_physical_add_item(self, rarity: Rarity) -> None:
        self.habit_physical_undefined_items[rarity.value] += 1

    def _habit_physical_flip_coins_for_item(self, rarity: Rarity, n: int = 1) -> None:
        if self.flip_coins_for_heads(n):
            self._habit_physical_add_item(rarity)

    def _habit_physical_get_random_elemental_scroll(self) -> str:
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

    def _habit_physical_veryrare_rewards(self):
        self._habit_physical_flip_coins_for_item(Rarity.VeryRare, 2)
        self._habit_physical_add_item(Rarity.Rare)
        self._habit_physical_flip_coins_for_item(Rarity.Uncommon)
        for _ in range(3):
            self._habit_physical_flip_coins_for_item(Rarity.Common, 2)
        match self._rng.choice([1, 2, 3]):
            case 1:
                self._habit_physical_add_item("legendary_tzeentch")
                self.habit_physical_tzeentchian_corruption += 10
            case 2:
                self._habit_physical_add_item("legendary_arcane")
                self.habit_physical_arcane_corruption += 10
            case 3:
                self._habit_physical_add_item("legendary_necromancer")
                self.habit_physical_necromancer_corruption += 10
            case _:
                raise RuntimeError

    def _habit_physical_common(self):
        self._habit_physical_flip_coins_for_item(Rarity.Common, 2)

        match self._rng.choice([1, 2, 3, 4], p=[1 / 3, 1 / 3, 1 / 6, 1 / 6]):
            case 1:
                self.increase_currency("scroll", 4)
            case 2:
                elem_scroll = self._habit_physical_get_random_elemental_scroll()
                self.increase_currency(elem_scroll)
            case 3:
                self._habit_physical_flip_coins_for_item(Rarity.Uncommon, 2)
            case 4:
                self._habit_physical_flip_coins_for_item(Rarity.Common)
            case _:
                raise RuntimeError

    def _habit_physical_uncommon(self):
        self.habit_physical_undefined_lores += 1
        self._habit_physical_flip_coins_for_item(Rarity.Uncommon, 2)
        match self._rng.choice([1, 2, 3]):
            case 1:
                self._habit_physical_flip_coins_for_item(Rarity.Common)
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
                self._habit_physical_uncommon_match_input(input_)
            case 2:
                elem_scroll = self._habit_physical_get_random_elemental_scroll()
                self.increase_currency(elem_scroll)
                if self.flip_coins_for_heads(1):
                    self.habit_physical_upgrade_tokens[Rarity.Common.value]
            case 3:
                self._habit_physical_flip_coins_for_item(Rarity.Common)
                self._habit_physical_flip_coins_for_item(Rarity.Common)

    def _habit_physical_uncommon_match_input(self, input_):
        match input_:
            case 1:
                elem_scroll = self._habit_physical_get_random_elemental_scroll()
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

    def _habit_physical_rare_roll_reward(self):
        match self._rng.choice([1, 2, 3, 4], p=[1 / 4, 1 / 2, 1 / 8, 1 / 8]):
            case 1:
                self.habit_physical_tzeentchian_scroll += 1
                self.habit_physical_tzeentchian_corruption += 3
            case 2:
                self.habit_physical_undefined_physical_reward += 1
            case 3:
                self.habit_physical_upgrade_tokens[Rarity.VeryRare.value] += 1
            case 4:
                self._streak_recovery += 1
                self._habit_physical_rare_roll_reward()
