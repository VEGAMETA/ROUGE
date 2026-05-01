#!/usr/bin/python3

import locale
import sys

from application.game_loop import GameLoop
from config.options import DefaultWindow


def main() -> None:
    locale.setlocale(locale.LC_ALL, "")
    while True:
        try:
            is_3d = "3d" in sys.argv or "--3d" in sys.argv
            loop = GameLoop(DefaultWindow, selected_3d=is_3d)
            if loop.run():
                break
            del loop
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    sys.exit(main())
