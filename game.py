#!/usr/bin/python3

import sys

from application.globals import Globals
from presentation.curses.app import Window
from presentation.curses.notification import Notification, NotificationType


def main_loop() -> None:
    screen = Globals.window.window
    screen.clear()

    Notification.show(screen, "abiba", style=NotificationType.WARN)

    while Globals.process:
        screen.addstr(0, 0, f"abobus {Globals.process}")

        screen.refresh()
        screen.getkey()
    Notification.show(screen, "abiaba", style=NotificationType.WARN)


def main() -> None:
    try:
        Window()
        main_loop()
    except KeyboardInterrupt:
        Globals.window.close()


if __name__ == "__main__":
    sys.exit(main())
