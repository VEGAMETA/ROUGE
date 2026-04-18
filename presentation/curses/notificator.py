import curses

from infrastructure.timers import Timer
from presentation.views.notificator import NotificationType, Notificator


class CursesNotificator(Notificator):
    ICON_MAP = {
        NotificationType.UNDEFINED: "",
        NotificationType.INFO: "!",
        NotificationType.OK: "√",
        NotificationType.WARN: "☼",
        NotificationType.ERROR: "X",
    }

    @staticmethod
    def _init_colors() -> None:
        for v, c1, c2 in [
            (NotificationType.UNDEFINED.value, curses.COLOR_WHITE, curses.COLOR_BLACK),
            (NotificationType.INFO.value, curses.COLOR_WHITE, curses.COLOR_BLUE),
            (NotificationType.OK.value, curses.COLOR_WHITE, curses.COLOR_GREEN),
            (NotificationType.WARN.value, curses.COLOR_BLACK, curses.COLOR_YELLOW),
            (NotificationType.ERROR.value, curses.COLOR_WHITE, curses.COLOR_RED),
            (NotificationType.DEBUG.value, curses.COLOR_BLACK, curses.COLOR_WHITE),
        ]:
            curses.init_pair(v, c1, c2)

    @staticmethod
    def show(
        window: curses.window,
        message: str,
        title: str = "",
        duration: float = 0.0,
        style: NotificationType = NotificationType.UNDEFINED,
    ) -> None:

        if not isinstance(window, curses.window):
            return

        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()

        CursesNotificator._init_colors()

        color_pair = curses.color_pair(style.value)

        icon = CursesNotificator.ICON_MAP.get(style, "•")

        max_msg_width = 50
        words = message.split()
        lines = []
        current = ""
        for word in words:
            if len(current) + len(word) + 1 <= max_msg_width:
                current = (current + " " + word).strip()
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)

        inner_w = max(len(title) + 4, max(len(_) for _ in lines) + 6, 30)
        inner_h = len(lines)
        win_h = inner_h + 2
        win_w = inner_w + 2

        screen_h, screen_w = window.getmaxyx()

        start_y = max(0, (screen_h - win_h) // 2)
        start_x = max(0, (screen_w - win_w) // 2)

        try:
            win = curses.newwin(win_h, win_w, start_y, start_x)
            win.bkgd(" ", color_pair)
            win.attron(color_pair)

            win.box()

            title_text = " ".join([icon, title]).strip()
            title_x = max(1, (inner_w - len(title_text) + 1) // 2)
            if title_text:
                win.addstr(0, title_x, f" {title_text} ")

            for i, line in enumerate(lines):
                win.addstr(1 + i, 3, line, color_pair)

            if not duration:
                hint = "[ Press any key... ]"
                hint_x = max(inner_h, (inner_w - len(hint) + 2) // 2)
                win.addstr(inner_h + 1, hint_x, hint)

            win.attroff(color_pair)
            win.refresh()
        except curses.error:
            return

        if duration:
            Timer.sleep_for(duration)

        else:
            win.nodelay(False)
            win.getch()

        win.clear()
        win.bkgd(" ")
        win.refresh()
