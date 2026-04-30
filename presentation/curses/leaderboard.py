import curses

from infrastructure.persistence.leaderboard import LeaderboardRecord
from presentation.views.leaderboard import LeaderboardView

HEADER = " # | {:<14} | {:>8} | Lvl | Kills | Food | Elix | Scrl |  Atk |  Hits | Tiles | Date".format(
    "Name", "Treasure"
)
COL_WIDTHS = len(HEADER)


class CursesLeaderboardView(LeaderboardView):
    _TITLE = "Leaderboard"
    _EMPTY_LINE = "(no records yet)"
    _HINT = "[ Press any key... ]"
    _SIDE_PADDING = 2

    @staticmethod
    def show(window: curses.window, records: list[LeaderboardRecord]) -> None:
        if not isinstance(window, curses.window):
            return

        if records:
            lines = [HEADER, "-" * COL_WIDTHS] + [
                CursesLeaderboardView._format_row(i + 1, r)
                for i, r in enumerate(records)
            ]
        else:
            lines = [CursesLeaderboardView._EMPTY_LINE]

        inner_w = max(
            len(CursesLeaderboardView._TITLE) + 4,
            max(len(line) for line in lines) + CursesLeaderboardView._SIDE_PADDING * 2,
            len(CursesLeaderboardView._HINT) + CursesLeaderboardView._SIDE_PADDING * 2,
        )
        inner_h = len(lines)
        win_h = inner_h + 4
        win_w = inner_w + 2

        screen_h, screen_w = window.getmaxyx()
        start_y = max(0, (screen_h - win_h) // 2)
        start_x = max(0, (screen_w - win_w) // 2)

        try:
            win = curses.newwin(win_h, win_w, start_y, start_x)
            win.box()

            title_x = max(1, (win_w - len(CursesLeaderboardView._TITLE) - 2) // 2)
            win.addstr(0, title_x, f" {CursesLeaderboardView._TITLE} ")

            for i, line in enumerate(lines):
                win.addstr(2 + i, 1 + CursesLeaderboardView._SIDE_PADDING, line)

            hint_x = max(1, (win_w - len(CursesLeaderboardView._HINT)) // 2)
            win.addstr(inner_h + 2, hint_x, CursesLeaderboardView._HINT)

            win.refresh()
        except curses.error:
            return

        win.nodelay(False)
        win.getch()

        win.clear()
        window.touchwin()
        win.refresh()

    @staticmethod
    def _format_row(rank: int, r: LeaderboardRecord) -> str:
        return (
            f"{rank:>2} | {r.name:<14} | {r.treasure:>8} | {r.level:>3} | {r.enemies:>5} |"
            f" {r.food:>4} | {r.elixirs:>4} | {r.scrolls:>4} | {r.attacks:>4} | {r.hits:>5} |"
            f" {r.tiles:>5} | {r.timestamp}"
        )
