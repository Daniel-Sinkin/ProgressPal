import random
import time
from typing import TypeAlias

import colorama
import numpy as np
from colorama import Fore, Style

from src.constants import Rarity
from src.player import Player
from src.util import clear_screen, pulling_sound, setup_exit_handling

GRIDPOS: TypeAlias = tuple[int, int]


def count_rarities(choices) -> dict[str, int]:
    flat_choices = choices.flatten()
    return {
        "Common": int(np.sum(flat_choices == "common")),
        "Uncommon": int(np.sum(flat_choices == "uncommon")),
        "Rare": int(np.sum(flat_choices == "rare")),
        "VeryRare": int(np.sum(flat_choices == "veryrare")),
    }


def main() -> None:
    colorama.init()
    player = Player("Daniel")
    # TODO: Shouldn't this be inside of the player `__init­­__` method?
    setup_exit_handling(player)
    clear_screen()

    n_rows, n_cols = 25, 8
    rng = np.random.default_rng()
    choices = rng.choice(
        ["nothing", "common", "uncommon", "rare", "veryrare"],
        p=[0.5, 0.35, 0.11, 0.03, 0.01],
        size=(n_rows, n_cols),
    )

    def print_choices(highlight_pos=None):
        clear_screen()
        print("#" * 108)
        print("#", " " * 106, "#", sep="")
        for i in range(n_rows):
            print("# ", end="")
            for j in range(n_cols):
                choice = choices[i, j]
                if choice == "nothing":
                    if (i, j) == highlight_pos:
                        centered_choice = ". " * 6
                    else:
                        centered_choice = " " * 12
                else:
                    if choice == "veryrare":
                        centered_choice = "  Very Rare "
                    else:
                        centered_choice = f"{choice:^12}".title()
                if (i, j) == highlight_pos:
                    print(f"{Fore.YELLOW}{centered_choice}{Style.RESET_ALL}", end=" ")
                elif choice == "nothing":
                    print(f"\033[30m{centered_choice}\033[0m", end=" ")
                elif choice == "common":
                    print(f"{Fore.WHITE}{centered_choice}{Style.RESET_ALL}", end=" ")
                elif choice == "uncommon":
                    print(f"{Fore.GREEN}{centered_choice}{Style.RESET_ALL}", end=" ")
                elif choice == "rare":
                    print(f"{Fore.BLUE}{centered_choice}{Style.RESET_ALL}", end=" ")
                elif choice == "veryrare":
                    print(f"{Fore.MAGENTA}{centered_choice}{Style.RESET_ALL}", end=" ")
            print(" #")
        print("#", " " * 106, "#", sep="")
        print("#" * 108)
        print()

        # Print rarity counts
        rarity_counts = count_rarities(choices)
        print(
            f"{Fore.WHITE}Common: {rarity_counts['Common']}{Style.RESET_ALL} | ", end=""
        )
        print(
            f"{Fore.GREEN}Uncommon: {rarity_counts['Uncommon']}{Style.RESET_ALL} | ",
            end="",
        )
        print(f"{Fore.BLUE}Rare: {rarity_counts['Rare']}{Style.RESET_ALL} | ", end="")
        print(f"{Fore.MAGENTA}Very Rare: {rarity_counts['VeryRare']}{Style.RESET_ALL}")
        print()

    all_positions: list[GRIDPOS] = [(i, j) for i in range(20) for j in range(5)]
    final_choice = None
    for i in range(40):
        highlight_pos = random.choice(all_positions)
        print_choices(highlight_pos)
        final_choice = choices[highlight_pos]
        time.sleep(0.2)
    pulling_sound.play()

    print("\nReward: ", end="")
    if final_choice != "nothing":
        print(f"{Fore.YELLOW}{final_choice:^12}{Style.RESET_ALL}")
    else:
        print("Nothing 😞")
    rarity = Rarity(final_choice)

    time.sleep(2.0)

    input("Press Enter to continue...")
    clear_screen()

    player.habit_physical(rarity=rarity)


if __name__ == "__main__":
    main()
    # init()
    # player = Player("Daniel")
    # setup_exit_handling(player)
    # clear_screen()
    # player.habit_physical(rarity=Rarity.Uncommon)
