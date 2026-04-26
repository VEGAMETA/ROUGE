import curses
import time
from typing import Optional

from domain.entities.game_session import GameSession
from domain.entities.item import Item
from domain.services.item import ItemService
from domain.value_objects.enums import ConsumableType, ItemType, KeyType
from presentation.curses.widgets import Label, VerticalMenu
from presentation.views.inventory import InventoryView
from domain.rules.progression import MAX_LEVEL


class CursesInventoryView(InventoryView):
    _STATS_W = 20
    _PADDING_X = 1
    _PADDING_Y = 1
    _NUM_ITEM_COLS = 4
    _ITEM_COL_W = 20
    _MAX_ITEMS = 9
    _TITLES = ["weapon", "food", "elixir", "scroll"]
    _HEART_PAIR = 243
    _KEY_BLUE_PAIR = 240
    _KEY_GREEN_PAIR = 241
    _KEY_RED_PAIR = 242

    @staticmethod
    def _get_column_items(context: GameSession) -> list[list[Optional[Item]]]:
        owned = context.player.inventory.items
        weapons = [i for i in owned if i.type == ItemType.WEAPON]
        return [
            [None] + weapons,
            [
                i
                for i in owned
                if i.type == ItemType.CONSUMABLE and i.subtype == ConsumableType.FOOD
            ],
            [
                i
                for i in owned
                if i.type == ItemType.CONSUMABLE and i.subtype != ConsumableType.FOOD
            ],
            [i for i in owned if i.type == ItemType.SCROLL],
        ]

    @staticmethod
    def _make_columns(
        context: GameSession,
        col_x_start: int,
        col_y: int,
        col_w: int,
        col_h: int,
        selected_idx: list[int],
    ) -> tuple[list[VerticalMenu], list[list[Optional[Item]]]]:
        all_items = CursesInventoryView._get_column_items(context)
        content_w = col_w - 2 * CursesInventoryView._PADDING_X - 2
        columns: list[VerticalMenu] = []
        for i, (title, items) in enumerate(zip(CursesInventoryView._TITLES, all_items)):
            children: list[Label] = []
            for item in items:
                if item is None:
                    marker = " [E]" if context.player.weapon is None else ""
                    children.append(Label(text=("Empty hands" + marker)[:content_w]))
                else:
                    marker = " [E]" if item is context.player.weapon else ""
                    stack = f" x{item.count}" if item.count > 1 else ""
                    children.append(
                        Label(text=(item.name + stack + marker)[:content_w])
                    )
            col = VerticalMenu(
                title=title,
                padding_x=CursesInventoryView._PADDING_X,
                padding_y=CursesInventoryView._PADDING_Y,
                spacing=0,
                border=True,
                children=children,
                fixed=True,
            )
            col.x = col_x_start + i * col_w
            col.y = col_y
            col.w = col_w
            col.h = col_h
            if children:
                idx = min(selected_idx[i], len(children) - 1)
                selected_idx[i] = idx
                col.selected_widget = children[idx]
            columns.append(col)
        return columns, all_items

    @staticmethod
    def _item_info(item: Optional[Item], context: GameSession) -> tuple[str, str]:
        if item is None:
            equipped = context.player.weapon
            label = equipped.name if equipped else "nothing"
            return f"Unequip current weapon ({label})", ""
        desc = item.description
        parts = []
        if hasattr(item, "damage"):
            parts.append(f"Damage: {item.damage}")
        if hasattr(item, "health") and item.health:
            parts.append(f"HP +{item.health}")
        if hasattr(item, "max_health") and item.max_health:
            parts.append(f"MaxHP +{item.max_health}")
        if hasattr(item, "strength") and item.strength:
            parts.append(f"STR +{item.strength}")
        if hasattr(item, "dexterity") and item.dexterity:
            parts.append(f"DEX +{item.dexterity}")
        if item.count > 1 and item.type == ItemType.CONSUMABLE:
            parts.append(f"Count: {item.count}")
        if not parts:
            parts.append(f"Value: {item.value}")
        return desc, "  ".join(parts)

    @staticmethod
    def _draw_stats(x: int, y: int, w: int, h: int, context: GameSession) -> None:
        win = curses.newwin(h, w, y, x)
        win.keypad(True)
        win.clear()
        elapsed = time.monotonic() - context.start_time
        hh = int(elapsed) // 3600
        mm = int(elapsed) % 3600 // 60
        ss = int(elapsed) % 60
        lv = int(context.player.level)
        row = 1
        win.addstr(row, 2, f"LEVEL     {lv}/{MAX_LEVEL}")
        row += 2
        hp_str = (
            f"HEALTH  {int(context.player.health)}/{int(context.player.max_health)}"
        )
        win.addstr(row, 2, hp_str)
        win.addstr(
            row,
            2 + len(hp_str),
            "♡",
            curses.color_pair(CursesInventoryView._HEART_PAIR),
        )
        row += 2
        win.addstr(row, 2, f"STRENGTH  {context.player.strength}")
        row += 1
        win.addstr(row, 2, f"DEXTERITY {context.player.dexterity}")
        row += 2
        win.addstr(row, 2, f"POINTS {context.points}")
        row += 2
        win.addstr(row, 2, f"TIME   {hh:02d}:{mm:02d}:{ss:02d}")
        row += 2
        owned_types = {k.type for k in context.keys if k.is_owned}
        win.addstr(row, 2, f"KEYS   {len(owned_types)}/3")
        row += 2
        slots = [
            (KeyType.BLUE,  CursesInventoryView._KEY_BLUE_PAIR),
            (KeyType.GREEN, CursesInventoryView._KEY_GREEN_PAIR),
            (KeyType.RED,   CursesInventoryView._KEY_RED_PAIR),
        ]
        col = 2
        for kt, pair in slots:
            if kt in owned_types:
                win.addstr(row, col, "⚿", curses.color_pair(pair))
            else:
                win.addstr(row, col, " ")
            col += 6
        win.refresh()

    @staticmethod
    def show(window: curses.window, context: GameSession) -> None:
        sh, sw = window.getmaxyx()

        padding = 1
        col_h = CursesInventoryView._MAX_ITEMS + 2 + 2 * CursesInventoryView._PADDING_Y
        stats_h = col_h + 4
        outer_h = max(col_h + 2 + 2 * padding, stats_h + 2 * padding) + 1

        n = CursesInventoryView._NUM_ITEM_COLS
        item_col_w = CursesInventoryView._ITEM_COL_W
        stats_w = CursesInventoryView._STATS_W
        inner_w = n * item_col_w + stats_w
        outer_w = inner_w + 2 + 2 * padding

        if outer_w > sw - 2:
            max_w = sw - 2
            item_col_w = max(10, (max_w - stats_w - 4) // n)
            stats_w = max(10, max_w - n * item_col_w - 4)
            inner_w = n * item_col_w + stats_w
            outer_w = inner_w + 2 + 2 * padding
        outer_h = min(outer_h, sh)
        outer_x = max(0, (sw - outer_w) // 2)
        outer_y = max(0, (sh - outer_h) // 2)
        start_x = outer_x + 1 + padding
        start_y = outer_y + 1 + padding
        stats_x = start_x + n * item_col_w

        curses.init_pair(CursesInventoryView._HEART_PAIR,    curses.COLOR_RED,   curses.COLOR_BLACK)
        curses.init_pair(CursesInventoryView._KEY_BLUE_PAIR,  curses.COLOR_BLUE,  curses.COLOR_BLACK)
        curses.init_pair(CursesInventoryView._KEY_GREEN_PAIR, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(CursesInventoryView._KEY_RED_PAIR,   curses.COLOR_RED,   curses.COLOR_BLACK)

        active_col = 0
        selected_idx = [0, 0, 0, 0]
        outer_win = curses.newwin(outer_h, outer_w, outer_y, outer_x)

        columns, all_items = CursesInventoryView._make_columns(
            context, start_x, start_y, item_col_w, col_h, selected_idx
        )

        window.timeout(1000)
        try:
            while True:
                outer_win.clear()
                outer_win.box()
                outer_win.refresh()

                for i, col in enumerate(columns):
                    win = col.draw(window)
                    if i == active_col:
                        try:
                            title_x = max(1, (col.w - len(col.title)) // 2)
                            win.addstr(
                                0, title_x, col.title, curses.A_BOLD | curses.A_REVERSE
                            )
                            win.refresh()
                        except curses.error:
                            pass

                CursesInventoryView._draw_stats(
                    stats_x, start_y, stats_w, stats_h, context
                )

                items_in_col = all_items[active_col]
                idx = selected_idx[active_col]
                sel = (
                    items_in_col[idx]
                    if items_in_col and 0 <= idx < len(items_in_col)
                    else None
                )
                desc_line, stats_line = CursesInventoryView._item_info(sel, context)
                desc_w = CursesInventoryView._NUM_ITEM_COLS * item_col_w
                desc_win = curses.newwin(3, desc_w, start_y + col_h, start_x)
                desc_win.clear()
                try:
                    desc_win.addstr(0, 1, desc_line[: desc_w - 2])
                    if stats_line:
                        desc_win.addstr(1, 1, stats_line[: desc_w - 2])
                except curses.error:
                    pass
                desc_win.refresh()

                key = window.getch()

                if key in (27, 9):
                    break

                elif key in (curses.KEY_UP, ord("w")):
                    col = columns[active_col]
                    if col.children:
                        col.prev_widget()
                        selected_idx[active_col] = col.children.index(
                            col.selected_widget
                        )

                elif key in (curses.KEY_DOWN, ord("s")):
                    col = columns[active_col]
                    if col.children:
                        col.next_widget()
                        selected_idx[active_col] = col.children.index(
                            col.selected_widget
                        )

                elif key in (curses.KEY_LEFT, ord("a"), ord("A")):
                    active_col = (active_col - 1) % CursesInventoryView._NUM_ITEM_COLS

                elif key in (curses.KEY_RIGHT, ord("d"), ord("D")):
                    active_col = (active_col + 1) % CursesInventoryView._NUM_ITEM_COLS

                elif key == ord("e"):
                    items = all_items[active_col]
                    idx = selected_idx[active_col]
                    if items and 0 <= idx < len(items):
                        item = items[idx]
                        if item is None:
                            context.player.weapon = None
                        else:
                            ItemService.use(item, context)
                        columns, all_items = CursesInventoryView._make_columns(
                            context, start_x, start_y, item_col_w, col_h, selected_idx
                        )

                elif key == ord("x"):
                    items = all_items[active_col]
                    idx = selected_idx[active_col]
                    if items and 0 <= idx < len(items):
                        item = items[idx]
                        if item is not None:
                            if item is context.player.weapon:
                                context.player.weapon = None
                            context.player.inventory.remove_item(item)
                            columns, all_items = CursesInventoryView._make_columns(
                                context,
                                start_x,
                                start_y,
                                item_col_w,
                                col_h,
                                selected_idx,
                            )
        finally:
            window.timeout(0)
            window.touchwin()
            window.refresh()
