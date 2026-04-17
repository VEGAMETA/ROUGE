import curses


class Widget:
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.widgets: list[Widget] = []


# Alinging + CENTER


class Panel(Widget): ...


class VerticalMenu(Panel): ...


class Label(Panel): ...


class Button(Panel):
    def toggle(self, /): ...


class Checkbox(Button): ...


class Slider(Button): ...


# class ProgressBar(Panel):
#     def toggle(self, /): ...
