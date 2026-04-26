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
        fixed: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.padding_y: int = padding_y
        self.padding_x: int = padding_x
        self.spacing: int = spacing
        self.border: bool = border
        self.children: list[Widget] = children
        self.fixed: bool = fixed

    def centerize(self, screen_w: int, screen_h: int) -> None:
        self.y = (screen_h - self.h) // 2 if screen_h >= self.h else 0
        self.x = (screen_w - self.w) // 2 if screen_w >= self.w else 0

    def compute_size(self) -> None:
        longest = max((len(widget.text) for widget in self.children), default=1)
        n = len(self.children)
        content_height = n + self.spacing * (n - 1) if n > 0 else 0
        self.w = longest + 2 * self.padding_x + (2 if self.border else 0)
        self.h = content_height + 2 * self.padding_y + (2 if self.border else 0)

    def centralize_widget(self, widget: Widget) -> None:
        content_w = self.w - 2 * self.padding_x - (2 if self.border else 0)
        widget.x = (content_w - widget.w) // 2

    def set_widget_postions(self) -> None:
        row_y = 0
        for i, widget in enumerate(self.children):
            widget.w = len(widget.text)
            widget.h = 1
            self.centralize_widget(widget)
            widget.y = row_y
            if i < len(self.children) - 1:
                row_y += 1 + self.spacing

    def draw(self, parent_win: curses.window) -> curses.window:
        if not self.fixed:
            sh, sw = parent_win.getmaxyx()
            self.compute_size()
            self.centerize(sw, sh)
        win = curses.newwin(self.h, self.w, self.y, self.x)
        if self.border:
            win.box()
        self.set_widget_postions()
        win.refresh()
        return win


class Label(Widget):
    def __init__(self, text: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.w = len(text)
        self._text: str = text

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text
        self.w = len(text)

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
        self.text += "  "
        self.text += self.get_toggled_str()

    def get_toggled_str(self) -> str:
        return "■" if self.toggled else "≡"

    def toggled(self) -> None:
        self.toggled = not self.toggled
        self.trigger(self.toggled)
        self.text[-1] = self.get_toggled_str()


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
    def __init__(self, title: str = "", **kwargs) -> None:
        super().__init__(**kwargs)
        self.title: str = title
        self.selected_widget: Optional[Widget] = (
            self.children[0] if self.children else None
        )

    def draw(self, parent_win: curses.window):
        win = super().draw(parent_win)
        if self.title and self.border:
            title_x = max(1, (self.w - len(self.title)) // 2)
            try:
                win.addstr(0, title_x, self.title)
            except curses.error:
                pass
        content_origin_y = (1 if self.border else 0) + self.padding_y
        content_origin_x = (1 if self.border else 0) + self.padding_x
        for wdg in self.children:
            if wdg == self.selected_widget:
                wdg.select(win, content_origin_x, content_origin_y)
            else:
                wdg.draw(win, content_origin_x, content_origin_y)
        win.refresh()
        return win

    def next_widget(self) -> None:
        if not self.children:
            return
        idx = self.children.index(self.selected_widget)
        self.selected_widget = self.children[(idx + 1) % len(self.children)]

    def prev_widget(self) -> None:
        if not self.children:
            return
        idx = self.children.index(self.selected_widget)
        self.select_widget(self.children[idx - 1])

    def select_widget(self, widget: Widget) -> None:
        self.selected_widget = widget
