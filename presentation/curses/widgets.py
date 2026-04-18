from __future__ import annotations
import curses
from typing import Callable, Optional


class Widget:
    def __init__(self, x: int = 0, y: int = 0, w: int = 0, h: int = 0) -> None:
        self.x: int = x
        self.y: int = y
        self.w: int = w
        self.h: int = h


class Panel(Widget):
    def __init__(
        self,
        padding_y: int = 1,
        padding_x: int = 3,
        spacing: int = 1,
        border: bool = True,
        children: list[Widget] = [],
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.padding_y: int = padding_y
        self.padding_x: int = padding_x
        self.spacing: int = spacing
        self.border: bool = border
        self.children: list[Widget] = children

    def centerize(self, screen_w: int, screen_h: int) -> None:
        self.y = (screen_h - self.h) // 2 if screen_h >= self.h else 0
        self.x = (screen_w - self.w) // 2 if screen_w >= self.w else 0


class Label(Widget):
    def __init__(self, text: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.w = len(text)
        self.text: str = text

    def draw(self, win: curses.window, origin_x: int = 0, origin_y: int = 0) -> None:
        win.addstr(origin_y + self.y, origin_x + self.x, self.text)

    def select(self, win: curses.window, origin_x: int = 0, origin_y: int = 0) -> None:
        win.addstr(origin_y + self.y, origin_x + self.x, self.text, curses.A_REVERSE)


class Button(Label):
    def __init__(self, trigger: Callable = lambda: ..., **kwargs) -> None:
        super().__init__(**kwargs)
        self.trigger: Callable = trigger

    def toggle(self) -> None:
        self.trigger()


class Checkbox(Button):
    def __init__(self, toggled: bool = False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.toggled: bool = toggled
        self.text += "  ■" if toggled else "  ⌂"

    def toggled(self) -> None:
        self.toggled = not self.toggled
        self.text[-1] = "■" if self.toggled else "⌂"


class Slider(Button):
    def __init__(
        self,
        value: float = 1.0,
        min_value: float = 0.0,
        max_value: float = 1.0,
        step: float = 0.1,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.value: float = value
        self.min_value: float = min_value
        self.max_value: float = max_value
        self.step: float = step
        self.text += "  ══════════ "
        self.set_value(self.value)

    def set_value(self, value: float) -> None:
        self.value = min(self.max_value, max(self.min_value, value))
        idx: int = -12 + int(10 * self.value / (self.max_value - self.min_value))
        self.text = self.text[:-12] + " ══════════ "
        self.text = self.text[:idx] + "█" + self.text[idx + 1 :]

    def increase_value(self):
        self.set_value(self.value + self.step)

    def decrease_value(self):
        self.set_value(self.value - self.step)


class VerticalMenu(Panel):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.selected_widget: Optional[Widget] = (
            self.children[0] if len(self.children) else None
        )

    def compute_size(self) -> None:
        longest = max((len(widget.text) for widget in self.children), default=1)
        n = len(self.children)
        content_height = n + self.spacing * (n - 1) if n > 0 else 0
        self.w = longest + 2 * self.padding_x + (2 if self.border else 0)
        self.h = content_height + 2 * self.padding_y + (2 if self.border else 0)

    def centralize_widget(self, wdg: Widget) -> None:
        content_w = self.w - 2 * self.padding_x - (2 if self.border else 0)
        wdg.x = (content_w - wdg.w) // 2

    def set_widget_postions(self) -> None:
        row_y = 0
        for i, wdg in enumerate(self.children):
            wdg.w = len(wdg.text)
            wdg.h = 1
            self.centralize_widget(wdg)
            wdg.y = row_y
            if i < len(self.children) - 1:
                row_y += 1 + self.spacing

    def draw(self, parent_win: curses.window) -> curses.window:
        sh, sw = parent_win.getmaxyx()
        self.compute_size()
        self.centerize(sw, sh)
        win = curses.newwin(self.h, self.w, self.y, self.x)
        win.bkgd(" ")
        if self.border:
            win.box()
        content_origin_y = (1 if self.border else 0) + self.padding_y
        content_origin_x = (1 if self.border else 0) + self.padding_x
        self.set_widget_postions()
        for wdg in self.children:
            if wdg == self.selected_widget:
                wdg.select(win, content_origin_x, content_origin_y)
            else:
                wdg.draw(win, content_origin_x, content_origin_y)
        win.refresh()
        return win

    def select_widget(self, Widget) -> None:
        self.selected_widget = Widget
