from domain.entities.stage import Stage
from domain.entities.tile import Tile
from domain.value_objects.enums import TileType
from domain.value_objects.position import Position


class TileFactory:
    @staticmethod
    def get_tiles(stage: Stage) -> list[Tile]:
        tiles: list[Tile] = []
        for corridor in stage.corridors:
            for pos in corridor.path:
                tiles.append(Tile(position=pos, type=TileType.CORRIDOR))
        for room in stage.rooms:
            for x in range(room.position.x, room.position.x + room.size.width + 1):
                for y in range(room.position.y, room.position.y + room.size.height + 1):
                    tiles.append(
                        Tile(
                            position=Position(x, y),
                            type=TileType.WALL
                            if x in (room.position.x, room.position.x + room.size.width)
                            or y
                            in (room.position.y, room.position.y + room.size.height)
                            else TileType.FLOOR,
                            # TODO: Make invisible, unexplored
                        )
                    )
            for door in room.doors:
                tiles.append(Tile(position=door.position, type=TileType.DOOR))
        return tiles

    @staticmethod
    def get_tile_map(stage: Stage, tiles: list[Tile]) -> list[list[Tile]]:
        tile_map: list[list[Tile]] = []
        for i in range(stage.size.height):
            tile_map.append([])
            for j in range(stage.size.width):
                tile_map[i].append(Tile(position=Position(j, i), type=TileType.VOID))
        for tile in tiles:
            tile_map[tile.position.y][tile.position.x] = tile
        return tile_map
