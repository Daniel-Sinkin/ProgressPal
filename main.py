import atexit
import os
import signal
import sys
import time
from contextlib import contextmanager
from io import StringIO

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

from src.player import Player


def clear_screen():
    # For Windows
    if os.name == "nt":
        _ = os.system("cls")
    # For Mac and Linux
    else:
        _ = os.system("clear")


def exit_handler(player: Player) -> None:
    player.save()


def setup_exit_handling(player: Player) -> None:
    atexit.register(exit_handler, player)
    signal.signal(signal.SIGINT, lambda s, f: exit(0))
    signal.signal(signal.SIGTERM, lambda s, f: exit(0))


@contextmanager
def indented_print(indent="\t"):
    original_stdout = sys.stdout
    string_io = StringIO()
    sys.stdout = string_io
    yield
    printed_text = string_io.getvalue()
    sys.stdout = original_stdout
    for line in printed_text.splitlines():
        print(indent + line, end="")
        input()


pygame.mixer.init()
pulling_sound = pygame.mixer.Sound("data/pulled_rarity.wav")
pulling_sound.set_volume(0.3)


def main():
    clear_screen()
    player = Player("Daniel")
    setup_exit_handling(player)

    n_pulls = 1
    for i, rarity in enumerate(player.pull_rarities(n_pulls)):
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
        print(f"Pulled '{rarity.prettify()}' ({i + 1} / {n_pulls})", end="")

        input()
        if rarity != "nothing":
            with indented_print():
                player.habit_journaling(rarity)
            input("\nFinished iteration. Press enter to continue...")
        clear_screen()

    serialized_data = player.serialize()
    json_data = player.to_json()
    new_player = Player.deserialize(serialized_data)


if __name__ == "__main__":
    main()
