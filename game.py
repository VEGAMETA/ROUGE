#!/usr/bin/python3

import sys

from application.game_loop import GameLoop
from config.settings import DefaultWindow
from tests.stage import test


def main() -> None:
    # loop = GameLoop(DefaultWindow)
    # loop.run()
    test()


if __name__ == "__main__":
    sys.exit(main())
