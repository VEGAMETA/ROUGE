#!/usr/bin/python3

import locale
import sys
import traceback

from application.game_loop import GameLoop
from config.options import DefaultWindow
from infrastructure.random import set_seed


def main() -> None:
    locale.setlocale(locale.LC_ALL, "")
    set_seed(1)
    loop = GameLoop(DefaultWindow)
    try:
        loop.run()
    except Exception as e:
        print(e)
        traceback.print_exc()


if __name__ == "__main__":
    sys.exit(main())
