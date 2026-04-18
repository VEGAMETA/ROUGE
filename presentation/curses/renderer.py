import curses
from random import random

from application.dto.game_state import GameStateDTO
from config.settings import Visuals
from domain.rules.progression import Level
from domain.value_objects.enums import TileType
from presentation.curses.render_map import CursesRenderData, CursesRenderMap
from presentation.renderer import Renderer


class CursesRenderer(Renderer):
    def __init__(self):
        super().__init__()
        self.window: curses.window


class CursesRenderer2D(CursesRenderer):
    def add_data(self, x: int, y: int, data: CursesRenderData):
        self.window.addstr(y, x, data.character, data.color1 | data.color2)

    def insert_data(self, x: int, y: int, data: CursesRenderData):
        self.window.insstr(y, x, data.character, data.color1 | data.color2)

    def hud(self, game_state: GameStateDTO) -> None:
        level = game_state.player.level.value
        health = round(game_state.player.health)
        max_health = round(game_state.player.max_health)
        strength = game_state.player.strength
        dexterity = game_state.player.dexterity
        self.window.addstr(
            0,
            0,
            f"↓{level:2d}/{len(Level)}    ♥{health:4d}/{max_health}    S {strength}  D {dexterity}",
        )

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
                self.insert_data(j, i, data)

        for enemy in game_state.enemies:
            # if (enemy.x, enemy.y) not in visible:
            #     continue
            data = CursesRenderMap.ENEMY_RENDER_MAP[enemy.type]
            self.add_data(enemy.x, enemy.y, data)

        for item in game_state.items:
            if (item.x, item.y) not in visible:
                continue
            if not item.is_owned:
                continue
            data = CursesRenderMap.ITEM_RENDER_MAP[item.type]
            data.color1 |= CursesRenderMap.RARITY_MAP[item.rarity]
            self.add_data(item.x, item.y, data)

        data = CursesRenderMap.PLAYER_RENDER_DATA
        self.add_data(game_state.player.x, game_state.player.y, data)

        self.hud(game_state)

        curses.curs_set(0)
        self.window.refresh()


class CursesRenderer3D(CursesRenderer):
    def render(self, game_state: GameStateDTO) -> None: ...
