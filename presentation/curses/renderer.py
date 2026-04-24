import curses
from math import atan2, cos, fabs, sin, sqrt
from random import random
from typing import Optional

from application.dto.game_state import GameStateDTO
from config.settings import Visuals
from domain.rules.progression import Level
from domain.value_objects.enums import TileType
from infrastructure.math import Constant
from infrastructure.vector import Size, Vector2, Vector2i
from presentation.curses.render_map import CursesRenderData, CursesRenderMap
from presentation.curses.sprites import SpriteMap, SpriteService, SpriteType
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

    @property
    def window(self) -> curses.window:
        return self.render_state.window

    @window.setter
    def window(self, window: curses.window) -> None:
        self.render_state.window = window

    def _get_pair(self, fg: int, bg: int) -> int:
        k: tuple[int, int] = (fg, bg)
        p: int = self.render_state.pair_cache.get(k)
        if p:
            return p
        if self.render_state.next_pair > self.render_state.max_pairs:
            return 0
        curses.init_pair(self.render_state.next_pair, fg, bg)
        self.render_state.pair_cache[k] = self.render_state.next_pair
        self.render_state.next_pair += 1
        return self.render_state.pair_cache[k]

    def add_data(self, x: int, y: int, data: CursesRenderData):
        pair = self._get_pair(data.color1, data.color2)
        self.window.addstr(y, x, data.character, curses.color_pair(pair))

    def insert_data(self, x: int, y: int, data: CursesRenderData):
        pair = self._get_pair(data.color1, data.color2)
        self.window.insstr(y, x, data.character, curses.color_pair(pair))


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
        visible: set[tuple[int, int]] = set()
        for row in game_state.tile_map[:-1]:
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
                if tile.changed or tile.x + tile.y in self.old_pos:
                    self.window.addch(
                        tile.y,
                        tile.x,
                        CursesRenderMap.TILE_RENDER_MAP[tile.show_type].character,
                    )
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
        for enemy in game_state.enemies:
            # if (enemy.x, enemy.y) not in visible:
            #     continue
            self.add_data(
                enemy.x, enemy.y, CursesRenderMap.ENEMY_RENDER_MAP[enemy.type]
            )
            self.old_pos.append(enemy.x + enemy.y)

        # for item in game_state.items:
        #     if (item.x, item.y) not in visible:
        #         continue
        #     if not item.is_owned:
        #         continue
        #     data = CursesRenderMap.ITEM_RENDER_MAP[item.type]
        #     data.color1 = CursesRenderMap.RARITY_MAP[item.rarity]
        #     # self.add_data(item.x, item.y, data)

        self.add_data(
            game_state.player.x, game_state.player.y, CursesRenderMap.PLAYER_RENDER_DATA
        )
        self.old_pos.append(game_state.player.x + game_state.player.y)

        self.hud(game_state)

        # self.window.refresh()


class CursesRenderer3D(CursesRenderer):
    def __init__(self) -> None:
        super().__init__()
        self.map_renderer: CursesRenderer2D = CursesRenderer2D()
        self.map_renderer.render_state = self.render_state
        self.depth: float = 16.0
        self.FOV: float = Constant.PI_BY_3  # 60 degrees

    def cast_wall(
        self, pos: Vector2, eye: Vector2, depth: float, game_state: GameStateDTO
    ) -> tuple[float, float]:
        wall_distance: float = 0
        sample_x: float = 0.0
        while wall_distance < depth:
            wall_distance += 0.1
            test_point: Vector2 = pos + eye * wall_distance
            test: Vector2i = Vector2i(*test_point)
            tile_type: TileType = game_state.tile_map[test.y][test.x].type
            if test.x < 0 or test.y < 0:
                wall_distance = depth
            elif tile_type not in (TileType.WALL, TileType.VOID):
                continue
            d = test_point - test
            test_angle = atan2(*([*(d - 0.5)][::-1]))
            sample_x = d.y if abs(test_angle) < Constant.PI_BY_4 else d.x
            break
        return wall_distance, sample_x

    def draw_column(
        self,
        pos: Vector2,
        eye: Vector2,
        map_size: Size,
        scr_size: Size,
        x: int,
        floor: float,
        ceiling: float,
        sample_x: float,
        wall_distance: float,
    ) -> None:
        for y in range(scr_size.height):
            if y < map_size.height and x < map_size.width:
                continue
            col: SpriteType = SpriteType.WALL_3
            color: int = SpriteService.sample_sprite_color(col, 0, 0)
            if y > ceiling and y <= floor:
                if wall_distance > self.depth:
                    continue
                sample_y: float = (y - ceiling) / (floor - ceiling)
                color = SpriteService.sample_sprite_color(col, sample_x, sample_y)
            else:
                rowDistance = 1 / (1 - 2 * y / scr_size.height)
                rowDistance *= 1 if y < ceiling else -1
                f: Vector2 = pos + eye * rowDistance
                col = SpriteType.CEILING_3 if y < ceiling else SpriteType.FLOOR_3
                color = SpriteService.sample_sprite_color(col, f.x % 1, f.y % 1)
            self.add_data(x, y, CursesRenderData("\u2588", color))  # █

    def render_enemies(
        self,
        game_state,
        player_x,
        player_y,
        player_angle,
        map_height,
        map_width,
        screen_width,
        screen_height,
        depth_buffer,
    ):
        for enemy in game_state.enemies:
            sprite = SpriteService.sprites[SpriteMap.ENEMY_MAP[enemy.type]]
            vec_x = enemy.x - player_x + 0.5
            vec_y = enemy.y - player_y + 0.5
            distance_from_player = sqrt(vec_x * vec_x + vec_y * vec_y)
            eye_x = cos(player_angle)
            eye_y = sin(player_angle)
            object_angle = atan2(eye_x, eye_y) - atan2(vec_x, vec_y)
            if object_angle < Constant.MINUS_PI:
                object_angle += Constant.PI_TIMES_2
            if object_angle > Constant.PI:
                object_angle -= Constant.PI_TIMES_2
            in_player_fov = fabs(object_angle) < self.FOV / 2.0
            if (
                in_player_fov
                and distance_from_player >= 0.5
                and distance_from_player < self.depth
            ):
                object_ceiling = float(screen_height / 2.0) - screen_height / float(
                    distance_from_player
                )
                object_floor = screen_height - object_ceiling
                object_height = object_floor - object_ceiling
                aspect = sprite.width / sprite.height
                object_width = int(object_height * aspect)
                middle_of_object = (
                    0.5 * (object_angle / (self.FOV / 2.0)) + 0.5
                ) * float(screen_width)
                for lx in range(int(object_width)):
                    for ly in range(int(object_height)):
                        sample_x = lx / object_width
                        sample_y = ly / object_height
                        color = SpriteService.sample_sprite_color(
                            sprite.type, sample_x, sample_y
                        )
                        object_column = int(
                            middle_of_object + lx - (object_width / 2.0)
                        )
                        y_screen = int(object_ceiling + ly)
                        if (
                            object_column >= 0
                            and object_column < screen_width
                            # and object_column > map_width#
                            and (
                                (y_screen >= 0 and object_column >= map_width)
                                or (y_screen >= map_height and object_column >= 0)
                            )
                            and y_screen < screen_height
                            and color is not None
                            and depth_buffer[object_column] >= distance_from_player
                        ):
                            data = CursesRenderData("█", color)
                            self.add_data(object_column, y_screen, data)

    def render(self, game_state: GameStateDTO) -> None:
        self.map_renderer.render(game_state)
        pos = Vector2(game_state.player.x, game_state.player.y) + 0.5
        player_angle = game_state.player.rotation
        map_size: Size = Size(len(game_state.tile_map[0]), len(game_state.tile_map))
        scr_size: Size = map_size * 3 - 1
        depth_buffer = [0.0] * scr_size.width
        for x in range(scr_size.width):
            ray_angle = player_angle + (x / scr_size.width - 0.5) * self.FOV
            eye: Vector2 = Vector2(cos(ray_angle), sin(ray_angle))
            wall_distance, sample_x = self.cast_wall(pos, eye, self.depth, game_state)
            ceiling = 0.5 * scr_size.height * (wall_distance - 2) / wall_distance
            floor = scr_size.height - ceiling
            depth_buffer[x] = wall_distance
            self.draw_column(
                pos,
                eye,
                map_size,
                scr_size,
                x,
                floor,
                ceiling,
                sample_x,
                wall_distance,
            )
        self.render_enemies(
            game_state,
            pos.x,
            pos.y,
            player_angle,
            map_size.height,
            map_size.width,
            scr_size.width,
            scr_size.height,
            depth_buffer,
        )
