#!/usr/bin/python3

import sys

from presentation.curses.input_handler import CursesInputHandler
from presentation.curses.notification import CursesNotification
from presentation.curses.renderer import CursesRenderer2D
from presentation.views.notification import NotificationType


def main_loop() -> None:
    renderer = CursesRenderer2D()
    notificator = CursesNotification(renderer)
    input_handler = CursesInputHandler(renderer)

    while True:
        # screen.addstr(0, 0, "abobus")

        notificator.show("abiba", style=NotificationType.WARN)
        key = renderer.window.getkey()
        if key == "q":
            break

    notificator.show("abiaba", style=NotificationType.WARN)
    renderer.window.refresh()


def main() -> None:
    main_loop()


if __name__ == "__main__":
    sys.exit(main())
