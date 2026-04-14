import curses
from random import random

from application.dto.game_state import GameStateDTO
from config.settings import Visuals
from domian.value_objects.enums import TileType
from presentation.curses.render_map import CursesRenderMap
from presentation.renderer import Renderer


class CursesRenderer(Renderer):
    def __init__(self):
        super().__init__()
        self.window: curses.window


class CursesRenderer2D(CursesRenderer):
    def render(self, game_state: GameStateDTO) -> None:
        visible: set[tuple[int, int]] = set()

        self.window.clear()

        for i in range(len(game_state.tile_map)):
            for j in range(len(game_state.tile_map[i])):
                tile = game_state.tile_map[i][j]
                if not tile.explored:
                    continue
                data = CursesRenderMap.TILE_RENDER_MAP[tile.type]
                if tile.type == TileType.VOID:
                    if random() < Visuals.GLIMP_DENSITY:
                        data = CursesRenderMap.TILE_RENDER_MAP[TileType.UNDEFINED]
                if tile.visible:
                    visible.add((tile.x, tile.y))
                    # elif tile.type == TileType.FLOOR or (
                    #     tile.type in (TileType.WALL, TileType.DOOR, TileType.CORRIDOR)
                    #     and tile.explored
                    # ):
                    # data = CursesRenderMap.TILE_RENDER_MAP[TileType.VOID]
                self.window.insstr(i, j, data.character, data.color1 | data.color2)

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

        self.window.addstr(
            game_state.player.y,
            game_state.player.x,
            "@",
        )
        curses.curs_set(0)
        self.window.refresh()


class CursesRenderer3D(CursesRenderer):
    def render(self, game_state: GameStateDTO) -> None: ...
