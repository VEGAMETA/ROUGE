from domian.entities.stage import Stage
from domian.entities.tile import Tile
from domian.value_objects.enums import TileType
from domian.value_objects.position import Position


class TileFactory:
    @staticmethod
    def get_tiles(stage: Stage) -> list[Tile]:
        tiles: list[Tile] = []
        for corridor in stage.corridors:
            for pos in corridor.path:
                tiles.append(Tile(TileType.CORRIDOR, pos))
        for room in stage.rooms:
            for x in range(room.position.x, room.position.x + room.width + 1):
                for y in range(room.position.y, room.position.y + room.height + 1):
                    tiles.append(
                        Tile(
                            TileType.WALL
                            if x in (room.position.x, room.position.x + room.width)
                            or y in (room.position.y, room.position.y + room.height)
                            else TileType.FLOOR,
                            Position(x, y),
                            # TODO: Make invisible, unexplored
                        )
                    )
            for door in room.doors:
                tiles.append(Tile(TileType.DOOR, door.position))
        return tiles
