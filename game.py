#!/usr/bin/python3

import sys

from application.game_loop import GameLoop
from config.settings import DefaultInputHandler, DefaultRenderer


def main() -> None:
    loop = GameLoop(
        renderer=DefaultRenderer,
        input_handler=DefaultInputHandler,
    )
    loop.run()


if __name__ == "__main__":
    sys.exit(main())
