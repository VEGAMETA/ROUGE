from collections import deque
from random import randint, sample

from domain.entities.corridor import Corridor
from domain.entities.door import Door
from domain.entities.room import Room
from domain.entities.stage import Stage
from domain.value_objects.enums import DoorSide
from domain.value_objects.position import Position
from infrastructure.math import build_grid_graph
from infrastructure.vector import Size


class StageFactory:
    @staticmethod
    def create_stage(size: Size) -> Stage:
        stage: Stage = Stage(
            position=Position(),
            size=size,
            corridors=[],
            rooms=[],
            graph=[],
        )
        StageFactory._create_rooms(stage)
        StageFactory._create_room_graph(stage)
        StageFactory._create_doors(stage)
        StageFactory._create_corridors(stage)
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

    # def _create_stairs(stage: Stage) -> None:

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
        keys_count = randint(0, 3)
        if keys_count == 0:
            return
        start_room = 0
        # двери/замки:
        # будем считать что lock_id == key_id
        # например:
        # door.lock_id = 1
        # room.keys.append(1)

        for key_id in range(1, keys_count + 1):
            reachable = StageFactory._get_reachable_rooms(
                stage=stage,
                start=start_room,
                obtained_keys=set(range(1, key_id)),
            )

            candidates = []

            for room_id in reachable:
                for neighbor in stage.graph[room_id]:
                    if neighbor not in reachable:
                        candidates.append((room_id, neighbor))

            if not candidates:
                break
            from_room, locked_room = sample(candidates, 1)[0]
            StageFactory._lock_connection(
                stage=stage,
                room_a=from_room,
                room_b=locked_room,
                key_id=key_id,
            )
            key_room = sample(list(reachable), 1)[0]
            stage.rooms[key_room].keys.append(key_id)
        if not StageFactory._all_rooms_accessible(stage, start_room):
            raise RuntimeError("Invalid key generation: soft-lock detected")

    @staticmethod
    def _get_reachable_rooms(
        stage: Stage,
        start: int,
        obtained_keys: set[int],
    ) -> set[int]:
        """
        BFS с учетом закрытых дверей
        """

        visited = set()
        queue = deque([start])

        while queue:
            room_id = queue.popleft()

            if room_id in visited:
                continue

            visited.add(room_id)

            for neighbor in stage.graph[room_id]:
                if StageFactory._can_pass(
                    stage,
                    room_id,
                    neighbor,
                    obtained_keys,
                ):
                    queue.append(neighbor)

        return visited

    @staticmethod
    def _can_pass(
        stage: Stage,
        room_a: int,
        room_b: int,
        obtained_keys: set[int],
    ) -> bool:
        """
        Проверка можно ли пройти между комнатами
        """

        room = stage.rooms[room_a]

        for door in room.doors:
            if getattr(door, "to_room", None) != room_b:
                continue

            lock_id = getattr(door, "lock_id", None)

            if lock_id is None:
                return True

            return lock_id in obtained_keys

        return True

    @staticmethod
    def _lock_connection(
        stage: Stage,
        room_a: int,
        room_b: int,
        key_id: int,
    ) -> None:
        """
        Двусторонне закрываем проход
        """

        for room_id, target in [(room_a, room_b), (room_b, room_a)]:
            room = stage.rooms[room_id]

            for door in room.doors:
                if getattr(door, "to_room", None) == target:
                    door.lock_id = key_id

    @staticmethod
    def _all_rooms_accessible(
        stage: Stage,
        start: int,
    ) -> bool:
        """
        Итеративный BFS + сбор ключей
        """

        obtained_keys = set()
        changed = True
        reachable = set()

        while changed:
            changed = False

            current = StageFactory._get_reachable_rooms(
                stage=stage,
                start=start,
                obtained_keys=obtained_keys,
            )

            if current != reachable:
                reachable = current
                changed = True

            for room_id in reachable:
                for key in getattr(stage.rooms[room_id], "keys", []):
                    if key not in obtained_keys:
                        obtained_keys.add(key)
                        changed = True

        return len(reachable) == len(stage.rooms)
