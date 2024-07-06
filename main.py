import random
import time

import numpy as np
from colorama import Fore, Style, init

from src.constants import Habit
from src.player import Player
from src.util import clear_screen, setup_exit_handling


def main() -> None:
    init()
    player = Player("Daniel")
    setup_exit_handling(player)
    clear_screen()

    n_rows, n_cols = 25, 8

    rng = np.random.default_rng()
    choices = rng.choice(
        ["", "common", "uncommon", "rare", "very rare"],
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
                if not choice:
                    if (i, j) == highlight_pos:
                        centered_choice = "." * 12
                    else:
                        centered_choice = " " * 12
                else:
                    centered_choice = f"{choice:^12}"

                if (i, j) == highlight_pos:
                    print(f"{Fore.YELLOW}{centered_choice}{Style.RESET_ALL}", end=" ")
                elif not choice:
                    print(f"\033[30m{centered_choice}\033[0m", end=" ")
                elif choice == "common":
                    print(f"{Fore.WHITE}{centered_choice}{Style.RESET_ALL}", end=" ")
                elif choice == "uncommon":
                    print(f"{Fore.GREEN}{centered_choice}{Style.RESET_ALL}", end=" ")
                elif choice == "rare":
                    print(f"{Fore.BLUE}{centered_choice}{Style.RESET_ALL}", end=" ")
                elif choice == "very rare":
                    print(f"{Fore.MAGENTA}{centered_choice}{Style.RESET_ALL}", end=" ")
            print(" #")
        print("#" * 108)
        print()

    all_positions = [(i, j) for i in range(20) for j in range(5)]

    final_choice = None
    for _ in range(40):
        highlight_pos = random.choice(all_positions)
        print_choices(highlight_pos)
        final_choice = choices[highlight_pos]
        time.sleep(0.2)

    print("\nReward:")
    if final_choice:
        print(f"{Fore.YELLOW}{final_choice:^12}{Style.RESET_ALL}")
    else:
        print("Nothing 😞")


if __name__ == "__main__":
    main()
