import atexit
import os
import signal
import sys
from contextlib import contextmanager
from io import StringIO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .player import Player

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame


def clear_screen():
    # For Windows
    if os.name == "nt":
        _ = os.system("cls")
    # For Mac and Linux
    else:
        _ = os.system("clear")


def exit_handler(player: "Player") -> None:
    player.save()


def setup_exit_handling(player: "Player") -> None:
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
