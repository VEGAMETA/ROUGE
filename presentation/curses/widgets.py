import curses


class Widget:
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.title: str = ''


class Panel(Widget):
    def __init__(self, x: int = 0, y: int = 0, w: int = 0, h: int = 0) -> None:
        super().__init__(x, y, w, h)
        self.padding_y = 1
        self.padding_x = 3
        self.spacing = 1
        self.border = True

    def centerize(self, screen_w: int, screen_h: int) -> None:
        self.y = (screen_h - self.h) // 2 if screen_h >= self.h else 0
        self.x = (screen_w - self.w) // 2 if screen_w >= self.w else 0


class Label(Widget):
    def __init__(self, title: str) -> None:
        super().__init__(0, 0, 0, 1)
        self.title = title
        self.w = len(title)
        self.h = 1

    def draw(self, win: curses.window, origin_x: int = 0, origin_y: int = 0) -> None:
        win.addstr(origin_y + self.y, origin_x + self.x, self.title)
    
    def select(self, win: curses.window, origin_x: int = 0, origin_y: int = 0) -> None:
        win.addstr(origin_y + self.y, origin_x + self.x, f'> {self.title} <')


class Button(Panel):
    def toggle(self) -> None:
        ...


class Checkbox(Button):
    def align(self) -> None:
        ...


class Slider(Button):
    ...


class Widjet_list:
    WIDGETS: list[Widget] = [
        Label("Continue"),
        Label("New game"),
        Label("Exit"),
    ]


class VerticalMenu(Panel, Widjet_list):
    def __init__(self) -> None:
        Panel.__init__(self, 0, 0, 0, 0)
        self.selected_widget: Widget = self.WIDGETS[0]

    def compute_size(self) -> None:
        longest = max((len(widget.title) for widget in self.WIDGETS), default=1)
        n = len(self.WIDGETS)
        content_height = n + self.spacing * (n - 1) if n > 0 else 0
        self.w = longest + 2 * self.padding_x + (2 if self.border else 0)
        self.h = content_height + 2 * self.padding_y + (2 if self.border else 0)

    def centralize_widget(self, wdg: Widget) -> None:
        content_w = self.w - 2 * self.padding_x - (2 if self.border else 0)
        wdg.x = (content_w - wdg.w) // 2

    def set_widget_postions(self) -> None:
        row_y = 0
        for i, wdg in enumerate(self.WIDGETS):
            wdg.w = len(wdg.title)
            wdg.h = 1
            self.centralize_widget(wdg)
            wdg.y = row_y
            if i < len(self.WIDGETS) - 1:
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
        for wdg in self.WIDGETS:
            if wdg == self.selected_widget:
                wdg.select(win, content_origin_x, content_origin_y)
            wdg.draw(win, content_origin_x, content_origin_y)
        win.refresh()
        return win

    def select_widget(self, Widget) -> None:
        self.selected_widget = Widget
