from typing import Optional

from domain.entities.game_session import GameSession
from domain.entities.room import Room
from domain.entities.tile import OBSTACLES


class Visibility:
    SIGHT_RADIUS: int = 6

    @staticmethod
    def update(session: GameSession) -> None:
        for row in session.tile_map:
            for tile in row:
                tile.visible = False

        room = Visibility.find_room(session)
        if room is not None:
            Visibility.reveal_room(session, room)
            return
        Visibility.reveal_radius(session)

    @staticmethod
    def find_room(session: GameSession) -> Optional[Room]:
        for room in session.stage.rooms:
            if room.is_inbound(session.player.position):
                return room
        return None

    @staticmethod
    def reveal_room(session: GameSession, room: Room) -> None:
        x0 = room.position.x
        y0 = room.position.y
        x1 = x0 + room.size.width
        y1 = y0 + room.size.height
        height = len(session.tile_map)
        width = len(session.tile_map[0]) if height else 0
        for y in range(max(0, y0), min(height, y1 + 1)):
            for x in range(max(0, x0), min(width, x1 + 1)):
                tile = session.tile_map[y][x]
                tile.visible = True
                tile.explored = True

    @staticmethod
    def reveal_radius(session: GameSession) -> None:
        height = len(session.tile_map)
        width = len(session.tile_map[0]) if height else 0
        ox, oy = session.player.position.x, session.player.position.y
        radius = Visibility.SIGHT_RADIUS

        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy > radius * radius:
                    continue
                tx, ty = ox + dx, oy + dy
                if not (0 <= tx < width and 0 <= ty < height):
                    continue
                if not Visibility._line_clear(session, ox, oy, tx, ty, width, height):
                    continue
                tile = session.tile_map[ty][tx]
                tile.visible = True
                tile.explored = True

    @staticmethod
    def _line_clear(
        session: GameSession,
        ox: int,
        oy: int,
        tx: int,
        ty: int,
        width: int,
        height: int,
    ) -> bool:
        steps = max(abs(tx - ox), abs(ty - oy))
        if steps == 0:
            return True
        sx = (tx - ox) / steps
        sy = (ty - oy) / steps
        for i in range(1, steps):
            x = round(ox + sx * i)
            y = round(oy + sy * i)
            if not (0 <= x < width and 0 <= y < height):
                return False
            if session.tile_map[y][x].type in OBSTACLES:
                return False
        return True
