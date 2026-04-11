import curses

from infrastructure.timers import Timer
from presentation.curses.renderer import CursesRenderer2D
from presentation.views.notification import Notification, NotificationType


class CursesNotification(Notification):
    def __init__(self, renderer: CursesRenderer2D) -> None:
        super().__init__()
        self.window = renderer.window

    def show(
        self,
        message: str,
        title: str = "Notification",
        duration: float = 0.0,
        style: NotificationType = NotificationType.INFO,
    ) -> None:
        if not self.window:
            return

        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()

        map(
            curses.init_pair,
            [
                (NotificationType.INFO.value, curses.COLOR_WHITE, curses.COLOR_BLUE),
                (NotificationType.OK.value, curses.COLOR_WHITE, curses.COLOR_GREEN),
                (NotificationType.WARN.value, curses.COLOR_BLACK, curses.COLOR_YELLOW),
                (NotificationType.ERROR.value, curses.COLOR_WHITE, curses.COLOR_RED),
                (NotificationType.DEBUG.value, curses.COLOR_BLACK, curses.COLOR_WHITE),
            ],
        )
        color_pair = curses.color_pair(style.value)

        icon_map = {
            NotificationType.INFO: "ℹ",
            NotificationType.OK: "✔",
            NotificationType.WARN: "⚠",
            NotificationType.ERROR: "✖",
        }
        icon = icon_map.get(style, "•")

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

        screen_h, screen_w = self.window.getmaxyx()

        start_y = max(0, (screen_h - win_h) // 2)
        start_x = max(0, (screen_w - win_w) // 2)

        try:
            shadow = curses.newwin(inner_h, inner_w, start_y + 2, start_x + 2)
            shadow.bkgd(" ", curses.color_pair(5) | curses.A_DIM)
            shadow.refresh()
        except curses.error:
            pass

        try:
            win = curses.newwin(inner_h, inner_w, start_y, start_x)
            win.bkgd(" ", color_pair)
            win.attron(color_pair)

            win.box()

            title_text = f" {icon} {title} "
            title_x = max(1, (inner_w - len(title_text)) // 2)
            win.addstr(0, title_x, title_text, color_pair | curses.A_BOLD)

            win.addstr(2, 1, "─" * (inner_w - 2), color_pair)

            for i, line in enumerate(lines):
                win.addstr(3 + i, 3, line, color_pair)

            if duration == 0:
                hint = "[ Press any key ]"
                hint_x = max(1, (inner_w - len(hint)) // 2)
                win.addstr(inner_h - 1, hint_x, hint, color_pair | curses.A_DIM)

            win.attroff(color_pair)
            win.refresh()
        except curses.error:
            return

        if duration > 0:
            Timer.sleep_timer(duration)
        else:
            win.nodelay(False)
            win.getch()

        win.clear()
        win.refresh()
        try:
            shadow.clear()
            shadow.refresh()
        except Exception:
            pass
