#!/usr/bin/python3

import locale
import sys
import traceback

from application.game_loop import GameLoop
from config.options import DefaultWindow


def main() -> None:
    locale.setlocale(locale.LC_ALL, "")
    loop = GameLoop(DefaultWindow)
    try:
        loop.run()
    except Exception as e:
        print(e)
        traceback.print_exc()


if __name__ == "__main__":
    sys.exit(main())
