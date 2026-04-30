#!/usr/bin/python3

import locale
import sys

from application.game_loop import GameLoop
from config.options import DefaultWindow


def main() -> None:
    locale.setlocale(locale.LC_ALL, "")
    try:
        while not GameLoop(DefaultWindow, selected_3d=True).run():
            pass
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    sys.exit(main())
