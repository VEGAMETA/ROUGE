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
            for x in range(room.position.x, room.position.x + room.size.width + 1):
                for y in range(room.position.y, room.position.y + room.size.height + 1):
                    tiles.append(
                        Tile(
                            TileType.WALL
                            if x in (room.position.x, room.position.x + room.size.width)
                            or y
                            in (room.position.y, room.position.y + room.size.height)
                            else TileType.FLOOR,
                            Position(x, y),
                            # TODO: Make invisible, unexplored
                        )
                    )
            for door in room.doors:
                tiles.append(Tile(TileType.DOOR, door.position))
        return tiles

    @staticmethod
    def get_tile_map(stage: Stage, tiles: list[Tile]) -> list[list[Tile]]:
        tile_map: list[list[Tile]] = []
        for i in range(stage.size.height):
            tile_map.append([])
            for j in range(stage.size.width):
                tile_map[i].append(Tile(TileType.VOID, Position(j, i)))
        for tile in tiles:
            tile_map[tile.position.y][tile.position.x] = tile
        return tile_map
