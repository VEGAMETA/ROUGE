from collections import deque
from random import choice, randint, shuffle
from typing import Optional

from domain.entities.corridor import Corridor
from domain.entities.door import Door
from domain.entities.key import Key
from domain.entities.room import Room
from domain.entities.stage import Stage
from domain.value_objects.enums import DoorSide, DoorType, KeyType
from domain.value_objects.position import Position
from infrastructure.math import build_grid_graph
from infrastructure.vector import Size


class StageFactory:
    @staticmethod
    def create_stage(size: Size) -> Stage:
        stage: Stage = Stage(
            position=Position(), size=size, corridors=[], rooms=[], graph=[], keys=[]
        )
        StageFactory._create_rooms(stage)
        StageFactory._create_room_graph(stage)
        StageFactory._create_doors(stage)
        StageFactory._create_corridors(stage)
        stage.start_room = choice(stage.rooms)
        stage.end_room = choice(
            [room for room in stage.rooms if room != stage.start_room]
        )
        StageFactory._create_keys(stage)

        return stage

    @staticmethod
    def _create_rooms(stage: Stage) -> None:
        room_size: Size = stage.size / 3
        if room_size.width < 6 or room_size.height < 6:
            return

        for i in range(stage.MAX_ROOMS):
            width = randint(3, room_size.width - 3)
            height = randint(3, room_size.height - 3)
            min_x = (i % 3) * room_size.width + 1
            max_x = (i % 3 + 1) * room_size.width - width - 1
            min_y = (i // 3) * room_size.height + 1
            max_y = (i // 3 + 1) * room_size.height - height - 1

            pos = Position(randint(min_x, max_x), randint(min_y, max_y))
            stage.rooms.append(Room(position=pos, size=Size(width, height), doors=[]))

    @staticmethod
    def _create_room_graph(stage: Stage) -> None:
        n = int(stage.MAX_ROOMS**0.5)
        all_neighbors = build_grid_graph(n)
        graph: list[set[int]] = [set(neighbors) for neighbors in all_neighbors]
        edges: list[tuple[int, int]] = []
        for room in range(stage.MAX_ROOMS):
            for neighbor in all_neighbors[room]:
                if neighbor > room:
                    edges.append((room, neighbor))
        shuffle(edges)
        for a, b in edges:
            graph[a].discard(b)
            graph[b].discard(a)
            if StageFactory._is_connected(graph, stage.MAX_ROOMS):
                continue
            graph[a].add(b)
            graph[b].add(a)
        stage.graph = graph

    @staticmethod
    def _is_connected(graph: list[set[int]], n: int) -> bool:
        visited: set[int] = {0}
        queue: deque[int] = deque([0])
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return len(visited) == n

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
        ax, ay, bx, by = (*door.position, *matching_door.position)
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

        stage.corridors.append(Corridor(path=path))

    @staticmethod
    def _create_doors(stage: Stage) -> None:
        for idx, room in enumerate(stage.rooms):
            x, y, w, h = (*room.position, *room.size)
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
                room.doors.append(Door(position=position, side=side))

    @staticmethod
    def _create_keys(stage: Stage) -> None:
        if not stage.rooms or stage.start_room is None:
            return

        rooms = stage.rooms
        start_idx = rooms.index(stage.start_room)

        accessible: set[int] = {start_idx}
        visited: set[int] = {start_idx}
        queue: deque[int] = deque([start_idx])

        key_types = list(KeyType)

        while queue:
            current = queue.popleft()
            for neighbor in stage.graph[current]:
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                door_out = StageFactory._find_connecting_door(
                    rooms[current], current, neighbor
                )
                door_in = StageFactory._find_connecting_door(
                    rooms[neighbor], neighbor, current
                )
                should_lock = (
                    door_out is not None
                    and door_in is not None
                    and choice([True, False])
                )
                if should_lock:
                    if not key_types:
                        break
                    key_type = key_types.pop()
                    door_out.is_locked = True
                    door_in.is_locked = True
                    host_room = rooms[choice(list(accessible))]
                    key_pos = host_room.get_random_inbound()
                    stage.keys.append(Key(position=key_pos, type=key_type))
                    door_out.type = DoorType(key_type.value)
                    door_in.type = DoorType(key_type.value)
                accessible.add(neighbor)
                queue.append(neighbor)

    def _find_connecting_door(
        room_src: Room, src_idx: int, dst_idx: int
    ) -> Optional[Door]:
        if dst_idx == src_idx + 1:
            side = DoorSide.RIGHT
        elif dst_idx == src_idx - 1:
            side = DoorSide.LEFT
        elif dst_idx == src_idx + 3:
            side = DoorSide.BOTTOM
        elif dst_idx == src_idx - 3:
            side = DoorSide.TOP
        else:
            return None
        return next((d for d in room_src.doors if d.side == side), None)
