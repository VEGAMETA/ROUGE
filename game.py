#!/usr/bin/python3

import sys

from application.game_loop import GameLoop
from config.options import DefaultWindow


def main() -> None:
    loop = GameLoop(DefaultWindow)
    loop.run()


if __name__ == "__main__":
    sys.exit(main())
