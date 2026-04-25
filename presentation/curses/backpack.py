import curses
from typing import Optional

from domain.entities.item import Item
from domain.value_objects.enums import ItemType
from presentation.curses.widgets import Label, VerticalMenu
from presentation.views.backpack import BackpackView


class CursesBackpackView(BackpackView):
    DROP_OFFSET = 100

    @staticmethod
    def show(
        window: curses.window,
        items: list[Item],
        item_type: ItemType,
        equipped: Optional[Item] = None,
    ) -> Optional[int]:
        can_unequip = item_type == ItemType.WEAPON

        if not items and not can_unequip:
            return None

        children: list[Label] = []
        if can_unequip:
            children.append(Label(text="0. empty hands"))
        for idx, item in enumerate(items):
            marker = " [E]" if item is equipped else ""
            children.append(Label(text=f"{idx + 1}. {item.name}{marker}"))

        menu = VerticalMenu(children=children)
        win = menu.draw(window)

        result: Optional[int] = None
        while True:
            key = win.getch()
            if key == 27:
                break
            elif key == curses.KEY_UP:
                menu.prev_widget()
                win = menu.draw(window)
            elif key == curses.KEY_DOWN:
                menu.next_widget()
                win = menu.draw(window)
            elif key in (curses.KEY_ENTER, 10, 13):
                selected_idx = menu.children.index(menu.selected_widget)
                result = selected_idx - 1 if can_unequip else selected_idx
                break
            elif ord("1") <= key <= ord("9"):
                slot = key - ord("1")
                if slot < len(items):
                    result = slot
                    break
            elif key == ord("0") and can_unequip:
                result = -1
                break
            elif key == ord("d"):
                selected_idx = menu.children.index(menu.selected_widget)
                item_idx = selected_idx - 1 if can_unequip else selected_idx
                if item_idx >= 0:
                    result = CursesBackpackView.DROP_OFFSET + item_idx
                    break

        window.touchwin()
        window.refresh()
        return result
