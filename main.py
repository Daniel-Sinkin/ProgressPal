from src.constants import Rarity
from src.player import Player


def main():
    player = Player("Daniel")
    player.habit_journaling(Rarity.Nothing)
    player.habit_journaling(Rarity.Common)
    player.habit_journaling(Rarity.Uncommon)
    player.habit_journaling(Rarity.Rare)
    player.habit_journaling(Rarity.VeryRare)


if __name__ == "__main__":
    main()
