import curses
from curses import window as CursesWindow

from domian.value_objects.enums import NotificationType
from infrastructure.timers import Timer


class Notification:
    @staticmethod
    def show(
        stdscr: CursesWindow,
        message: str,
        title: str = "Notification",
        duration: float = 0.0,
        style: NotificationType = NotificationType.INFO,
    ) -> None:
        """
        Show a floating notification window in the center of the screen.

        Args:
            stdscr: curses main screen
            message: text to display
            title: window title
            duration: how long to show (seconds), 0 = wait for keypress
            style: "info" | "success" | "warning" | "error"
        """
        if not stdscr:
            return

        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()

        curses.init_pair
        curses.init_pair
        curses.init_pair
        curses.init_pair
        curses.init_pair
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

        # Icons
        icon_map = {
            NotificationType.INFO: "ℹ",
            NotificationType.OK: "✔",
            NotificationType.WARN: "⚠",
            NotificationType.ERROR: "✖",
        }
        icon = icon_map.get(style, "•")

        # Wrap long messages
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

        # Window dimensions
        inner_w = max(len(title) + 4, max(len(_) for _ in lines) + 6, 30)
        inner_h = len(lines) + 4  # top border + title + sep + lines + bottom border
        win_h = inner_h + 2  # +2 for shadow
        win_w = inner_w + 2  # +2 for shadow

        screen_h, screen_w = stdscr.getmaxyx()

        # Center the notification
        start_y = max(0, (screen_h - win_h) // 2)
        start_x = max(0, (screen_w - win_w) // 2)

        # --- Draw shadow ---
        try:
            shadow = curses.newwin(inner_h, inner_w, start_y + 2, start_x + 2)
            shadow.bkgd(" ", curses.color_pair(5) | curses.A_DIM)
            shadow.refresh()
        except curses.error:
            pass

        # --- Draw main window ---
        try:
            win = curses.newwin(inner_h, inner_w, start_y, start_x)
            win.bkgd(" ", color_pair)
            win.attron(color_pair)

            # Border
            win.box()

            # Title bar
            title_text = f" {icon} {title} "
            title_x = max(1, (inner_w - len(title_text)) // 2)
            win.addstr(0, title_x, title_text, color_pair | curses.A_BOLD)

            # Separator
            win.addstr(2, 1, "─" * (inner_w - 2), color_pair)

            # Message lines
            for i, line in enumerate(lines):
                win.addstr(3 + i, 3, line, color_pair)

            # Footer hint
            if duration == 0:
                hint = "[ Press any key ]"
                hint_x = max(1, (inner_w - len(hint)) // 2)
                win.addstr(inner_h - 1, hint_x, hint, color_pair | curses.A_DIM)

            win.attroff(color_pair)
            win.refresh()
        except curses.error:
            return

        # --- Wait or timeout ---
        if duration > 0:
            Timer.sleep_timer(duration)
        else:
            win.nodelay(False)
            win.getch()

        # Clean up
        win.clear()
        win.refresh()
        try:
            shadow.clear()
            shadow.refresh()
        except Exception:
            pass
