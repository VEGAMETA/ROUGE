import curses

from application.dto.game_state import GameStateDTO
from presentation.curses.render_map import CursesRenderMap
from presentation.renderer import Renderer


class CursesRenderer2D(Renderer):
    def __init__(self):
        super().__init__()
        self.window: curses.window

    def render(self, game_state: GameStateDTO) -> None:
        visible: set[tuple[int, int]] = set()

        self.window.clear()

        for tile in game_state.tiles:
            if not tile.explored:
                continue
            data = CursesRenderMap.TILE_RENDER_MAP[tile.type]
            if tile.visible:
                visible.add((tile.x, tile.y))
            # else:
            #     data = CursesRenderMap.TILE_RENDER_MAP[TileType.VOID]
            self.window.addstr(
                tile.y, tile.x, data.character, data.color1 | data.color2
            )

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
        curses.curs_set(0)
        self.window.refresh()


class CursesRenderer3D(Renderer):
    def render(self, game_state: GameStateDTO) -> None:
        pass
