import curses

from presentation.views.leaderboard import LeaderboardView


class CursesLeaderboardView(LeaderboardView):
    _TITLE = "Leaderboard"
    _EMPTY_LINE = "(no records yet)"
    _HINT = "[ Press any key... ]"
    _MIN_INNER_W = 30
    _SIDE_PADDING = 6
    _TITLE_PADDING = 4

    @staticmethod
    def show(window: curses.window, entries: list[str]) -> None:
        if not isinstance(window, curses.window):
            return

        lines = entries if entries else [CursesLeaderboardView._EMPTY_LINE]

        inner_w = max(
            len(CursesLeaderboardView._TITLE) + CursesLeaderboardView._TITLE_PADDING,
            max(len(line) for line in lines) + CursesLeaderboardView._SIDE_PADDING,
            len(CursesLeaderboardView._HINT) + CursesLeaderboardView._SIDE_PADDING,
            CursesLeaderboardView._MIN_INNER_W,
        )
        inner_h = len(lines)
        win_h = inner_h + 3
        win_w = inner_w + 2

        screen_h, screen_w = window.getmaxyx()
        start_y = max(0, (screen_h - win_h) // 2)
        start_x = max(0, (screen_w - win_w) // 2)

        try:
            win = curses.newwin(win_h, win_w, start_y, start_x)
            win.box()

            title_x = max(1, (inner_w - len(CursesLeaderboardView._TITLE) + 1) // 2)
            win.addstr(0, title_x, f" {CursesLeaderboardView._TITLE} ")

            for i, line in enumerate(lines):
                win.addstr(1 + i, 3, line)

            hint_x = max(1, (inner_w - len(CursesLeaderboardView._HINT) + 2) // 2)
            win.addstr(inner_h + 1, hint_x, CursesLeaderboardView._HINT)

            win.refresh()
        except curses.error:
            return

        win.nodelay(False)
        win.getch()

        win.clear()
        win.refresh()
