from random import randint, sample

from domian.entities.corridor import Corridor
from domian.entities.door import Door
from domian.entities.room import Room
from domian.entities.stage import Stage
from domian.value_objects.enums import DoorSide
from domian.value_objects.position import Position
from infrastructure.math import build_grid_graph


class StageFactory:
    @staticmethod
    def create_stage(width: int, height: int) -> Stage:
        stage: Stage = Stage(width, height, [], [], [])
        StageFactory._create_rooms(stage)
        StageFactory._create_room_graph(stage)
        StageFactory._create_doors(stage)
        StageFactory._create_corridors(stage)
        return stage

    @staticmethod
    def _create_rooms(stage: Stage) -> None:
        room_width = stage.width // 3
        room_height = stage.height // 3
        if room_width < 6 or room_height < 6:
            return

        for i in range(stage.MAX_ROOMS):
            width = randint(3, room_width - 3)
            height = randint(3, room_height - 3)
            min_x = (i % 3) * room_width + 1
            max_x = (i % 3 + 1) * room_width - width - 1
            min_y = (i // 3) * room_height + 1
            max_y = (i // 3 + 1) * room_height - height - 1

            pos = Position(randint(min_x, max_x), randint(min_y, max_y))
            stage.rooms.append(Room(pos, width, height, []))

    @staticmethod
    def _create_room_graph(stage: Stage) -> None:
        neighbors = build_grid_graph(int(stage.MAX_ROOMS**0.5))

        graph: list[set[int]] = [set() for _ in range(stage.MAX_ROOMS)]

        for room in range(stage.MAX_ROOMS):
            if len(neighbors[room]) == 0:
                continue
            random_neighbor_count: int = 1  # randint(1, len(neighbors[room]))
            chosen_neighbors: list[int] = sample(neighbors[room], random_neighbor_count)
            for neighbor in chosen_neighbors:
                graph[room].add(neighbor)
                graph[neighbor].add(room)
                neighbors[neighbor].pop(neighbors[neighbor].index(room))

        stage.graph = graph

    @staticmethod
    def _create_corridors(stage: Stage) -> None:
        rooms = stage.rooms
        for idx, room1 in enumerate(rooms):
            for room2 in stage.graph[idx]:
                if room2 == idx + 1 and idx % 3 != stage.MAX_ROOMS - 1:
                    src = next(d for d in room1.doors if d.side == DoorSide.RIGHT)
                    dst = next(d for d in rooms[room2].doors if d.side == DoorSide.LEFT)
                elif room2 == idx + 3:
                    src = next(d for d in room1.doors if d.side == DoorSide.BOTTOM)
                    dst = next(d for d in rooms[room2].doors if d.side == DoorSide.TOP)
                else:
                    continue
                StageFactory._create_corridor(stage, src, dst)

    @staticmethod
    def _create_corridor(stage: Stage, door: Door, matching_door: Door) -> None:
        ax, ay, bx, by = (
            door.position.x,
            door.position.y,
            matching_door.position.x,
            matching_door.position.y,
        )
        path: list[Position] = []
        horizontal: bool = door.side in (DoorSide.LEFT, DoorSide.RIGHT)

        if not horizontal:
            ax, ay, bx, by = ay, ax, by, bx

        def pos(along: int, cross: int) -> Position:
            return Position(along, cross) if horizontal else Position(cross, along)

        if ay == by:
            path = [pos(p, ay) for p in range(ax, bx + 1)]
        else:
            turn = randint(ax + 1, bx - 1)
            step = 1 if by >= ay else -1
            for p in range(ax, turn):
                path.append(pos(p, ay))
            for c in range(ay, by + step, step):
                path.append(pos(turn, c))
            for p in range(turn, bx + 1):
                path.append(pos(p, by))

        stage.corridors.append(Corridor(path))

    @staticmethod
    def _create_doors(stage: Stage) -> None:
        for idx, room in enumerate(stage.rooms):
            x, y, w, h = room.position.x, room.position.y, room.width, room.height
            for neighbor in stage.graph[idx]:
                if neighbor == idx + 1 and idx % 3 != stage.MAX_ROOMS - 1:
                    position = Position(x + w, randint(y + 1, y + h - 1))
                    side = DoorSide.RIGHT
                elif neighbor == idx - 1 and idx % 3 != 0:
                    position = Position(x, randint(y + 1, y + h - 1))
                    side = DoorSide.LEFT
                elif neighbor == idx + 3:
                    position = Position(randint(x + 1, x + w - 1), y + h)
                    side = DoorSide.BOTTOM
                elif neighbor == idx - 3:
                    position = Position(randint(x + 1, x + w - 1), y)
                    side = DoorSide.TOP
                else:
                    continue
                room.doors.append(Door(position, side))
