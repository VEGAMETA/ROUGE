#!/usr/bin/python3

import sys

# from application.game_loop import GameLoop
from config.settings import DefaultWindow
from tests.stage import stage_test


def main() -> None:
    # loop = GameLoop(DefaultWindow)
    # loop.run()
    stage_test(DefaultWindow)


if __name__ == "__main__":
    sys.exit(main())
