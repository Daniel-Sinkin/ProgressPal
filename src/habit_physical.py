from . import parameters
from .constants import Rarity


class HabitPhysicalMixin:
    def on_init(self) -> None:
        self._currency["adventure_token_bronze"] = 0
        self._currency["adventure_token_silver"] = 0
        self._currency["adventure_token_golden"] = 0
        self.habit_physical_undefined_items = {rar.value: 0 for rar in Rarity}
        self.habit_physical_upgrade_tokens = {
            rar.value: 0 for rar in Rarity if rar != Rarity.VeryRare
        }
        self.habit_physical_rewards: dict[str, int] = {
            "undefined_lores": 0,
            "undefined_physical_reward": 0,
            "tzeentchian_scroll": 0,
            "tzeentchian_corruption": 0,
            "arcane_corruption": 0,
            "necromancer_corruption": 0,
            "legendary_khrone": 0,
            "legendary_champion": 0,
            "legendary_warrior": 0,
        }

        self.habit_physical_corruptions = {
            "khorne": 0,
            "fame": 0,
            "rage": 0,
        }

        self.habit_physical_obtained_epic_reward = False

    def habit_physical(self, rarity: Rarity) -> None:
        match rarity:
            case Rarity.Nothing:
                pass
            case Rarity.Common:
                self._habit_physical_common()
            case Rarity.Uncommon:
                self._habit_physical_uncommon()
            case Rarity.Rare:
                self._habit_physical_rare()
            case Rarity.VeryRare:
                self._habit_physical_obtained_epic_reward()

                p_jester = parameters.P.JESTER_HAT
                if not self._obtained_jester_hat and self._rng.choice(
                    [True, False],
                    p=[p_jester, 1 - p_jester],
                ):
                    self._obtained_jester_hat = True
                else:
                    self._habit_physical_veryrare_rewards()

            case _:
                raise RuntimeError

    def _habit_physical_uncommon(self):
        self._habit_physical_add_reward("undefined_lores")
        self._habit_physical_quest_event()
        self._habit_physical_flip_coins_for_item(Rarity.Uncommon, 2)
        self._habit_physical_challenge()

        choice = int(self._rng.choice([1, 2, 3]))
        match choice:
            case 1:
                self._habit_physical_flip_coins_for_item(Rarity.Common, 2)
                self.increase_currency("adventure_token_bronze", 4)
            case 2:
                self._habit_physical_shop()
            case 3:
                self._habit_physical_flip_coins_for_item(Rarity.Common, 2)
                self._habit_physical_flip_coins_for_item(Rarity.Common, 2)
            case _:
                raise RuntimeError

    def _habit_physical_common(self):
        self._habit_journaling_flip_coins_for_item(Rarity.Common, 2)

        choice = int(self._rng.choice([1, 2, 3, 4], p=[1 / 3, 1 / 3, 1 / 6, 1 / 6]))
        match choice:
            case 1:
                self.increase_currency("adventure_token_bronze", 4)
            case 2:
                token_type = str(
                    self._rng.choice(
                        ["adventure_token_silver", "adventure_token_golden"],
                        p=[0.96, 0.04],
                    )
                )
                self.increase_currency(token_type)
            case 3:
                self._habit_physical_flip_coins_for_item(Rarity.Uncommon, 2)
            case 4:
                self._habit_physical_flip_coins_for_item(Rarity.Common)
            case _:
                raise RuntimeError

    def _habit_physical_rare(self):
        choice = int(self._rng.choice([1, 2, 3, 4], p=[1 / 4, 1 / 2, 1 / 8, 1 / 8]))
        match choice:
            case 1:
                self._habit_physical_khorne_challenge()
                self._habit_journaling_add_corruption("khorne", 3)
            case 2:
                self._habit_physical_add_reward("undefined_physical_reward")
            case 3:
                self.habit_physical_upgrade_tokens(Rarity.Rare)
            case 4:
                self._streak_recovery += 1
                self._habit_physical_rare()
            case _:
                raise RuntimeError

    def _habit_physical_veryrare_rewards(self) -> None:
        self._habit_physical_add_item(Rarity.Rare)
        self._habit_physical_flip_coins_for_item(Rarity.Rare, 2)
        self._habit_physical_flip_coins_for_item(Rarity.Uncommon, 2)
        for _ in range(3):
            self._habit_physical_flip_coins_for_item(Rarity.Common, 3)

        choice = int(self._rng.choice([1, 2, 3]))
        match choice:
            case 1:
                self._habit_journaling_add_reward("legendary_khorne")
                self._habit_journaling_add_corruption("khrone", 10)
            case 2:
                self._habit_journaling_add_reward("legendary_champion")
                self._habit_journaling_add_corruption("champion", 10)
            case 3:
                self._habit_journaling_add_reward("legendary_warrior")
                self._habit_journaling_add_corruption("warrior", 10)
            case _:
                raise RuntimeError

    def _habit_physical_flip_coins_for_item(self, rarity: Rarity, n: int = 1) -> None:
        if self.flip_coins_for_heads(n):
            self._habit_physical_add_item(rarity)

    def _habit_physical_add_item(self, rarity: Rarity) -> None:
        self.habit_physical_undefined_items[rarity.value] += 1
        print(f"Obtained a physical item of rarity '{rarity.value}'!")

    def _habit_physical_add_upgrade_token(self, rarity: Rarity) -> None:
        self.habit_physical_undefined_items[rarity.value] += 1
        print(f"Obtained an upgrade token of rarity '{rarity.value}'!")

    def _habit_physical_add_reward(self, reward: str, n=1) -> None:
        self.habit_physical_rewards[reward] += 1
        print(
            f"Obtained {'a' if n == 1 else n} physical reward{'s' if n > 1 else ''} '{reward}'!"
        )

    def _habit_physical_quest_event(self) -> None:
        print("_habit_physical_quest_event is not implemented yet.")

    def _habit_physical_challenge(self) -> None:
        print("_habit_physical_challenge is not implemented yet.")

    def _habit_physical_shop(self) -> None:
        print("_habit_physical_shop is not implemented yet.")

    def _habit_physical_khorne_challenge(self) -> None:
        print("_habit_physical_khorne_challenge is not implemented yet.")

    def _habit_physical_obtained_epic_reward(self) -> None:
        if not self.habit_physical_obtained_epic_reward:
            self.habit_physical_obtained_epic_reward = True
            print("Obtained an epic physical reward!")
