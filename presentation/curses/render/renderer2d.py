import curses
from random import random

from application.dto.game_state import GameStateDTO
from config.settings import Visuals
from domain.rules.progression import Level
from domain.value_objects.enums import TileType
from presentation.curses.render.render_map import CursesRenderData, CursesRenderMap
from presentation.curses.render.renderer import CursesRenderer


class CursesRenderer2D(CursesRenderer):
    old_pos: list[int] = []

    def hud(self, game_state: GameStateDTO) -> None:
        level = game_state.player.level.value
        health = round(game_state.player.health)
        max_health = round(game_state.player.max_health)
        strength = game_state.player.strength
        dexterity = game_state.player.dexterity
        curses.init_pair(255, curses.COLOR_BLACK, curses.COLOR_BLACK)
        self.window.addstr(
            0,
            0,
            f"↓{level:2d}/{len(Level)}    ♥{health:4d}/{max_health}    S {strength}  D {dexterity}",
            curses.color_pair(255) | curses.A_REVERSE | curses.A_BLINK | curses.A_DIM,
        )

    def render(self, game_state: GameStateDTO) -> None:
        # visible: set[tuple[int, int]] = set()
        toprint: dict[tuple[int, int], str] = {}
        for row in game_state.tile_map:
            for tile in row:
                # tile.show_type = tile.type if tile.explored else TileType.VOID

                # if tile.visible:
                # elif tile.type == TileType.FLOOR or (
                #     tile.type in (TileType.WALL, TileType.DOOR, TileType.CORRIDOR)
                #     and tile.explored
                # ):
                # data = CursesRenderMap.TILE_RENDER_MAP[TileType.VOID]
                # tile.show_type = TileType.VOID
                # else:
                # tile.show_type = tile.type
                t = (tile.x, tile.y)
                if tile.changed or hash(t) in self.old_pos:
                    toprint[t] = CursesRenderMap.TILE_RENDER_MAP[tile.show_type]
                    tile.changed = False
                if tile.show_type == TileType.VOID:
                    if random() < Visuals.GLIMP_DENSITY_M:
                        tile.show_type = TileType.UNDEFINED
                        tile.changed = True
                elif tile.show_type == TileType.UNDEFINED:
                    if random() < Visuals.GLIMP_DENSITY:
                        tile.show_type = TileType.VOID
                        tile.changed = True

        self.old_pos.clear()

        for item in game_state.items:
            if item.is_owned:
                continue
            t = (item.x, item.y)
            toprint[t] = CursesRenderData(
                CursesRenderMap.ITEM_RENDER_MAP[item.type].character,
                CursesRenderMap.RARITY_MAP[item.rarity],
            )
            self.old_pos.append(hash(t))

        for enemy in game_state.enemies:
            # if (enemy.x, enemy.y) not in visible:
            #     continue
            t = (enemy.x, enemy.y)
            toprint[t] = CursesRenderMap.ENEMY_RENDER_MAP[enemy.type]
            self.old_pos.append(hash(t))

        t = (game_state.player.x, game_state.player.y)
        toprint[t] = CursesRenderMap.PLAYER_RENDER_DATA
        self.old_pos.append(hash(t))

        max_height = len(game_state.tile_map) - 1
        max_width = len(game_state.tile_map[0]) - 1

        toprint.pop((max_width, max_height), None)
        for t, data in toprint.items():
            self.add_data(t[0], t[1], data)
        self.hud(game_state)
