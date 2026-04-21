import curses
from math import atan2, cos, fabs, sin, sqrt
from random import random

from application.dto.game_state import GameStateDTO
from config.settings import Visuals
from domain.rules.progression import Level
from domain.value_objects.enums import TileType
from infrastructure.math import Constant
from presentation.curses.render_map import CursesRenderData, CursesRenderMap
from presentation.curses.sprites import SpriteMap, SpriteService, SpriteType
from presentation.renderer import Renderer


class CursesRenderer(Renderer):
    def __init__(self):
        super().__init__()
        self.window: curses.window


class CursesRenderer2D(CursesRenderer):
    ColorPair = 1

    def add_data(self, x: int, y: int, data: CursesRenderData):
        curses.init_pair(self.ColorPair, data.color1, data.color2)
        self.window.addstr(y, x, data.character, curses.color_pair(self.ColorPair))
        self.ColorPair += 1

    def insert_data(self, x: int, y: int, data: CursesRenderData):
        self.window.insstr(y, x, data.character, data.color1 | data.color2)

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

        self.window.clear()
        self.ColorPair = 1
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


"""class CursesRenderer3D(CursesRenderer):
    depth = 16.0
    FOV = Constant.PI / 4

    def _get_pair(self, fg, bg):
        if not hasattr(self, "_pair_cache"):
            self._pair_cache = {}
            self._next_pair = 1
            self._max_pairs = curses.COLOR_PAIRS - 1
        k = (fg, bg)
        p = self._pair_cache.get(k)
        if p is not None:
            return p
        if self._next_pair > self._max_pairs:
            return 0
        curses.init_pair(self._next_pair, fg, bg)
        self._pair_cache[k] = self._next_pair
        self._next_pair += 1
        return self._pair_cache[k]

    def add_data(self, x: int, y: int, data: CursesRenderData):
        pid = self._get_pair(data.color1, data.color2)
        self.window.addstr(y, x, data.character, curses.color_pair(pid))

    def insert_data(self, x: int, y: int, data: CursesRenderData):
        pid = self._get_pair(data.color1, data.color2)
        self.window.insstr(y, x, data.character, curses.color_pair(pid))

    def draw_mini_map(self, game_state: GameStateDTO) -> None:
        for i in range(len(game_state.tile_map)):
            for j in range(len(game_state.tile_map[i])):
                tile = game_state.tile_map[i][j]
                data = CursesRenderMap.TILE_RENDER_MAP[tile.type]
                self.add_data(j, i, data)

        for enemy in game_state.enemies:
            data = CursesRenderMap.ENEMY_RENDER_MAP[enemy.type]
            self.add_data(enemy.x, enemy.y, data)

        data = CursesRenderMap.PLAYER_RENDER_DATA
        self.add_data(game_state.player.x, game_state.player.y, data)

    def compute_ray(self, player_angle, FOV, x, screen_width):
        ray_angle = (player_angle - FOV / 2.0) + (float(x) / float(screen_width)) * FOV
        eye_x = cos(ray_angle)
        eye_y = sin(ray_angle)
        return eye_x, eye_y

    def cast_wall(
        self, player_x, player_y, eye_x, eye_y, depth, game_state, map_width, map_height
    ):
        distance_to_wall = 0
        hit_wall = False
        sample_x = 0.0
        while (not hit_wall) and distance_to_wall < depth:
            distance_to_wall += 0.07
            test_x = int(player_x + eye_x * distance_to_wall)
            test_y = int(player_y + eye_y * distance_to_wall)
            if test_x < 0 or test_y >= map_width or test_y < 0 or test_y >= map_height:
                hit_wall = True
                distance_to_wall = depth
            else:
                tile = game_state.tile_map[test_y][test_x]
                data = CursesRenderMap.TILE_RENDER_MAP[tile.type]
                if (
                    data == CursesRenderMap.TILE_RENDER_MAP[TileType.WALL]
                    or data == CursesRenderMap.TILE_RENDER_MAP[TileType.VOID]
                ):
                    hit_wall = True
                    block_mid_x = test_x + 0.5
                    block_mid_y = test_y + 0.5
                    test_point_x = player_x + eye_x * distance_to_wall
                    test_point_y = player_y + eye_y * distance_to_wall
                    test_angle = atan2(
                        (test_point_y - block_mid_y), (test_point_x - block_mid_x)
                    )
                    if test_angle >= -3.14159 * 0.25 and test_angle < 3.14159 * 0.25:
                        sample_x = test_point_y - float(test_y)
                    if test_angle >= 3.14159 * 0.25 and test_angle < 3.14159 * 0.75:
                        sample_x = test_point_x - float(test_x)
                    if test_angle < -3.14159 * 0.25 and test_angle >= -3.14159 * 0.75:
                        sample_x = test_point_x - float(test_x)
                    if test_angle >= 3.14159 * 0.75 or test_angle < -3.14159 * 0.75:
                        sample_x = test_point_y - float(test_y)
        return distance_to_wall, sample_x

    def draw_column(
        self,
        x,
        screen_height,
        ceiling,
        floor,
        distance_to_wall,
        eye_x,
        eye_y,
        player_x,
        player_y,
        depth,
        sample_x,
    ):
        for y in range(screen_height):
            if y < ceiling:
                rowDistance = screen_height / (screen_height - 2.0 * y)
                fx = player_x + eye_x * rowDistance
                fy = player_y + eye_y * rowDistance
                u = fx % 1.0
                v = fy % 1.0
                color = SpriteService.sample_sprite_color(SpriteType.CEILING_3, u, v)
                data = CursesRenderData("█", color)
                self.add_data(x, y, data)
            elif y > ceiling and y <= floor:
                if distance_to_wall < depth:
                    sample_y = (float(y) - float(ceiling)) / (
                        float(floor) - float(ceiling)
                    )
                    color = SpriteService.sample_sprite_color(
                        SpriteType.WALL_3, sample_x, sample_y
                    )
                    data = CursesRenderData("█", color)
                    self.add_data(x, y, data)
                else:
                    data = CursesRenderMap.TILE_RENDER_MAP[TileType.VOID]
            else:
                rowDistance = screen_height / (2.0 * y - screen_height)
                fx = player_x + eye_x * rowDistance
                fy = player_y + eye_y * rowDistance
                u = fx % 1.0
                v = fy % 1.0
                color = SpriteService.sample_sprite_color(SpriteType.FLOOR_3, u, v)
                data = CursesRenderData("█", color)
                self.add_data(x, y, data)

    def render_enemies(
        self,
        game_state,
        player_x,
        player_y,
        player_angle,
        FOV,
        screen_width,
        screen_height,
        depth,
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
            if object_angle < -3.14159:
                object_angle += 2.0 * 3.14159
            if object_angle > 3.14159:
                object_angle -= 2.0 * 3.14159
            in_player_fov = fabs(object_angle) < FOV / 2.0
            if (
                in_player_fov
                and distance_from_player >= 0.5
                and distance_from_player < depth
            ):
                object_ceiling = float(screen_height / 2.0) - screen_height / float(
                    distance_from_player
                )
                object_floor = screen_height - object_ceiling
                object_height = object_floor - object_ceiling
                aspect = sprite.width / sprite.height
                object_width = int(object_height * aspect)
                middle_of_object = (0.5 * (object_angle / (FOV / 2.0)) + 0.5) * float(
                    screen_width
                )
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
                            and y_screen >= 0
                            and y_screen < screen_height
                            and color is not None
                            and depth_buffer[object_column] >= distance_from_player
                        ):
                            data = CursesRenderData("█", color)
                            self.add_data(object_column, y_screen, data)

    def render(self, game_state: GameStateDTO) -> None:
        self.window.clear()
        player_x = game_state.player.x + 0.5
        player_y = game_state.player.y + 0.5
        player_angle = game_state.player.rotation
        map_height = len(game_state.tile_map)
        map_width = len(game_state.tile_map[0])
        screen_width = map_width * 3 - 1
        screen_height = map_height * 3 - 1
        depth_buffer = [0.0 for _ in range(screen_width)]
        for x in range(screen_width):
            ray_angle = (player_angle - self.FOV / 2.0) + (
                float(x) / float(screen_width)
            ) * self.FOV
            eye_x = cos(ray_angle)
            eye_y = sin(ray_angle)
            distance_to_wall, sample_x = self.cast_wall(
                player_x,
                player_y,
                eye_x,
                eye_y,
                self.depth,
                game_state,
                map_width,
                map_height,
            )
            ceiling = float(screen_height / 2.0) - screen_height / float(
                distance_to_wall
            )
            floor = screen_height - ceiling
            depth_buffer[x] = distance_to_wall
            self.draw_column(
                x,
                screen_height,
                ceiling,
                floor,
                distance_to_wall,
                eye_x,
                eye_y,
                player_x,
                player_y,
                self.depth,
                sample_x,
            )
        self.render_enemies(
            game_state,
            player_x,
            player_y,
            player_angle,
            self.FOV,
            screen_width,
            screen_height,
            self.depth,
            depth_buffer,
        )

        self.draw_mini_map(game_state)
        curses.curs_set(0)
        self.window.refresh()
"""
