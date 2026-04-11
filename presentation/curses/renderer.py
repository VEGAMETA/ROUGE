import curses

from application.dto.game_state import GameStateDTO
from domian.value_objects.enums import TileType
from presentation.curses.render_map import CursesRenderMap
from presentation.renderer import Renderer


class CursesRenderer2D(Renderer):
    def __init__(self):
        super().__init__()
        self.window = curses.initscr()
        self.window.clear()
        self.window.refresh()
        curses.noecho()
        curses.cbreak()
        self.window.keypad(True)

    def render(self, game_state: GameStateDTO) -> None:
        visible: set[tuple[int, int]] = set()

        self.window.clear()

        for tile in game_state.tiles:
            if not tile.explored:
                continue
            render_data = CursesRenderMap.TILE_RENDER_MAP[tile.type]
            char = render_data.character
            color = render_data.color1

            if tile.visible:
                visible.add((tile.x, tile.y))
            elif tile.type == TileType.FLOOR:
                char = CursesRenderMap.TILE_RENDER_MAP[TileType.VOID].character

            self.window.addstr(tile.x, tile.y, char, color)

        for enemy in game_state.enemies:
            if (enemy.position.x, enemy.position.y) not in visible:
                continue
            self.window.addstr(
                enemy.position.y,
                enemy.position.x,
                CursesRenderMap.ENEMY_RENDER_MAP[enemy.type].character,
                CursesRenderMap.ENEMY_RENDER_MAP[enemy.type].color,
            )

        for item in game_state.items:
            if (item.position.x, item.position.y) not in visible:
                continue
            if not item.is_owned:
                continue
            self.window.addstr(
                item.position.y,
                item.position.x,
                item.character,
                CursesRenderMap.RARITY_MAP[item.rarity],
            )

        self.window.refresh()

    def close(self) -> None:
        self.window.clear()
        self.window.refresh()
        curses.nocbreak()
        self.window.keypad(False)
        curses.endwin()


class CursesRenderer3D(Renderer): ...
