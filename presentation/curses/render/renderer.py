import curses
from typing import Optional

from presentation.curses.render.render_map import CursesRenderData
from presentation.renderer import Renderer


class RenderState:
    def __init__(self):
        self.window: Optional[curses.window] = None
        self.pair_cache: dict[tuple[int, int], int] = {}
        self.next_pair: int = 1
        self.max_pairs: int = 255


class CursesRenderer(Renderer):
    def __init__(self) -> None:
        super().__init__()
        self.render_state: RenderState = RenderState()
        self.pair_id: int = 0

    @property
    def window(self) -> curses.window:
        return self.render_state.window

    @window.setter
    def window(self, window: curses.window) -> None:
        self.render_state.window = window

    def _get_pair(self, fg: int, bg: int) -> int:
        pair = self.render_state.pair_cache.get((fg, bg))
        if pair is not None:
            return pair
        if self.render_state.next_pair <= self.render_state.max_pairs:
            curses.init_pair(self.render_state.next_pair, fg, bg)
            self.render_state.pair_cache[(fg, bg)] = self.render_state.next_pair
            self.render_state.next_pair += 1
            return self.render_state.next_pair - 1
        return 0

    def add_data(self, x: int, y: int, data: CursesRenderData):
        pair = self._get_pair(data.color1, data.color2)
        self.window.addstr(y, x, data.character, curses.color_pair(pair))

    def insert_data(self, x: int, y: int, data: CursesRenderData):
        pair = self._get_pair(data.color1, data.color2)
        self.window.insstr(y, x, data.character, curses.color_pair(pair))
