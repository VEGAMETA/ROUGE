from functools import lru_cache
from math import atan2, cos, fabs, sin

import numpy as np

from application.dto.game_state import GameStateDTO
from domain.value_objects.enums import TileType
from infrastructure.math import Constant
from infrastructure.vector import Size, Vector2, Vector2i
from presentation.curses.render.render_map import CursesRenderData
from presentation.curses.render.renderer import CursesRenderer
from presentation.curses.render.renderer2d import CursesRenderer2D
from presentation.curses.sprites import SpriteMap, SpriteService, SpriteType


class CursesRenderer3D(CursesRenderer):
    def __init__(self) -> None:
        super().__init__()
        self.map_renderer: CursesRenderer2D = CursesRenderer2D()
        self.map_renderer.render_state = self.render_state
        self.depth: float = 16.0
        self.FOV: float = Constant.PI_BY_3  # 60 degrees
        self.ONE_BY_FOV: float = 1 / self.FOV
        self.HALF_FOV: float = 0.5 * self.FOV

        self.rows_init: bool = False
        self.rowDistances_ceiling: dict[int, float] = {}
        self.rowDistances_floor: dict[int, float] = {}

    def init_rows(self, game_state: GameStateDTO) -> None:
        if self.rows_init:
            return
        self.map_size: Size = Size(
            len(game_state.tile_map[0]), len(game_state.tile_map)
        )
        self.scr_size: Size = self.map_size * 3 - 1
        self.depth_buffer = [0.0] * self.scr_size.width
        self.rowDistances_ceiling = {
            y: 1 / (1 - 2 * y / self.scr_size.height)
            for y in range(self.scr_size.height)
        }
        self.rowDistances_floor = {
            y: 1 / (2 * y / self.scr_size.height - 1)
            for y in range(self.scr_size.height)
        }
        self.arr = np.zeros((self.scr_size.height, self.scr_size.width), dtype=np.int8)
        for y in range(self.map_size.height):
            for x in range(self.map_size.width):
                self.arr[y, x] = game_state.tile_map[y][x].type.value
        self.rows_init = True

    def get_shadow(self, surface_distance: float) -> str:
        ratio = self.depth - surface_distance
        if ratio <= 4:
            return " "
        elif ratio < 8:
            return "░"
        elif ratio < 10:
            return "▒"
        return "\u2588"  # █

    def print_sprite_(
        self,
        x: int,
        y: int,
        distance: float,
        sprite_type: SpriteType = SpriteType.UNDEFINED,
        sample_x: float = 0,
        sample_y: float = 0,
    ):
        color = SpriteService.sample_sprite_color(sprite_type, sample_x, sample_y)
        self.add_data(x, y, CursesRenderData(self.get_shadow(distance), color))

    @lru_cache(maxsize=10000)
    def cast_wall(
        self, pos: Vector2, eye: Vector2, depth: float
    ) -> tuple[float, float]:
        delta_dist_x = abs(1 / eye.x) if eye.x != 0 else 1e6
        delta_dist_y = abs(1 / eye.y) if eye.y != 0 else 1e6
        map_x = int(pos.x)
        map_y = int(pos.y)
        step_x = 1 if eye.x > 0 else -1
        step_y = 1 if eye.y > 0 else -1
        side_dist_x = (map_x + 1 - pos.x if eye.x > 0 else pos.x - map_x) * delta_dist_x
        side_dist_y = (map_y + 1 - pos.y if eye.y > 0 else pos.y - map_y) * delta_dist_y
        while True:
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                hit_vertical = True
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                hit_vertical = False
            if min(side_dist_x, side_dist_y) >= 10:
                return depth, 0.0
            if map_x < 0 or map_y < 0:
                return depth, 0.0
            tile_type = self.arr[map_y][map_x]
            if tile_type not in (TileType.WALL, TileType.VOID):
                continue
            if hit_vertical:
                wall_distance = (map_x - pos.x + (0 if step_x > 0 else 1)) / eye.x
                sample_x = (pos.y + wall_distance * eye.y) % 1
            else:
                wall_distance = (map_y - pos.y + (0 if step_y > 0 else 1)) / eye.y
                sample_x = (pos.x + wall_distance * eye.x) % 1
            return wall_distance, sample_x

    def draw_column(
        self, pos: Vector2, eye: Vector2, x: int, sample_x: float, wall_distance: float
    ) -> None:
        start = self.map_size.height + 1 if x < self.map_size.width else 0
        ceiling = max(start, int(self.ceiling))
        floor = min(self.scr_size.height, int(self.floor))
        smf = self.floor - self.ceiling
        smfb = self.ceiling / smf
        for y in range(ceiling, floor):
            a = y / smf - smfb
            self.print_sprite_(x, y, wall_distance, SpriteType.WALL_3, sample_x, a)
        for y in range(start, ceiling):
            rowDistance = self.rowDistances_ceiling[y]
            f = pos + eye * rowDistance
            f -= Vector2i(*f)
            self.print_sprite_(x, y, rowDistance, SpriteType.CEILING_3, f.x, f.y)
        for y in range(floor, self.scr_size.height):
            rowDistance = self.rowDistances_floor[y]
            f = pos + eye * rowDistance
            f -= Vector2i(*f)
            self.print_sprite_(x, y, rowDistance, SpriteType.FLOOR_3, f.x, f.y)

    def render_enemies(
        self, game_state: GameStateDTO, pos: Vector2, player_angle: float
    ) -> None:
        eye: Vector2 = Vector2(cos(player_angle), sin(player_angle))
        obj_eye: float = atan2(eye.x, eye.y)
        game_state.enemies.sort(
            key=lambda e: (Vector2(e.x, e.y) - pos + 0.5).length(), reverse=True
        )
        for enemy in game_state.enemies:
            sprite: SpriteType = SpriteService.sprites[SpriteMap.ENEMY_MAP[enemy.type]]
            vec: Vector2 = Vector2(enemy.x, enemy.y) - pos + 0.5
            distance = vec.length()
            object_angle = obj_eye - atan2(vec.x, vec.y)
            if object_angle < Constant.MINUS_PI:
                object_angle += Constant.PI_TIMES_2
            if object_angle > Constant.PI:
                object_angle -= Constant.PI_TIMES_2
            in_player_fov = fabs(object_angle) < self.HALF_FOV
            if not (in_player_fov and distance >= 0.5 and distance < self.depth):
                continue
            object_ceiling = self.scr_size.height * (0.5 - 1 / distance)
            object_floor = self.scr_size.height - object_ceiling
            object_height = object_floor - object_ceiling
            aspect = sprite.width / sprite.height
            object_width = int(object_height * aspect)
            middle_of_object = (
                object_angle * self.ONE_BY_FOV + 0.5
            ) * self.scr_size.width

            lx = np.arange(object_width)
            ly = np.arange(int(object_height))
            sample_x = lx / object_width
            sample_y = ly / int(object_height)
            object_columns = (middle_of_object + lx - object_width / 2.0).astype(int)
            y_screens = (object_ceiling + ly).astype(int)
            col_mask = (object_columns >= 0) & (object_columns < self.scr_size.width)
            row_mask = (y_screens >= 0) & (y_screens < self.scr_size.height)
            valid_cols = object_columns[col_mask]
            depth_mask = [self.depth_buffer[c] >= distance for c in valid_cols]
            col_indices = np.where(col_mask)[0]
            col_indices = col_indices[depth_mask]
            if col_indices.size == 0:
                continue
            row_indices = np.where(row_mask)[0]
            for ci in col_indices:
                col = object_columns[ci]
                for ri in row_indices:
                    y = y_screens[ri]
                    if not (
                        (y >= 0 and col >= self.map_size.width)
                        or (y >= self.map_size.height and col >= 0)
                    ):
                        continue
                    color = SpriteService.sample_sprite_color(
                        sprite.type, sample_x[ci], sample_y[ri]
                    )
                    if color is None:
                        continue
                    self.add_data(
                        col, y, CursesRenderData(self.get_shadow(distance), color)
                    )

    def render(self, game_state: GameStateDTO) -> None:
        self.init_rows(game_state)
        self.map_renderer.render(game_state)
        pos = Vector2(game_state.player.x, game_state.player.y) + 0.5
        angle = game_state.player.rotation

        for x in range(self.scr_size.width):
            ray_angle = angle + (x / self.scr_size.width - 0.5) * self.FOV
            eye: Vector2 = Vector2(cos(ray_angle), sin(ray_angle))
            wall_distance, sample_x = self.cast_wall(pos, eye, self.depth)
            self.ceiling = self.scr_size.height * (0.5 - 1 / wall_distance)
            self.floor = self.scr_size.height - self.ceiling
            self.depth_buffer[x] = wall_distance
            self.draw_column(pos, eye, x, sample_x, wall_distance)
        self.render_enemies(game_state, pos, angle)
