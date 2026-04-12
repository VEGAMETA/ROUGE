from random import randint, sample, choice

from domian.entities.corridor import Corridor
from domian.entities.door import Door
from domian.entities.room import Room
from domian.entities.stage import Stage
from domian.value_objects.position import Position


class StageFactory:
    @staticmethod
    def create_level(stage: Stage) -> Stage:
        StageFactory.create_rooms(stage)
        graph = StageFactory.create_room_graph(stage)
        StageFactory.create_doors(stage, graph)
        StageFactory.create_corridors(stage, graph)
        return stage

    @staticmethod
    def create_rooms(stage: Stage) -> None:
        room_width = stage.width // 3
        room_height = stage.height // 3
        if room_width < 6 or room_height < 6:
            return

        for i in range(stage.MAX_ROOMS):
            width = randint(3, room_width - 3)
            height = randint(3, room_height - 3)

            min_x = (i % 3) * room_width + 1
            max_x = (i % 3 + 1) * room_width - width - 1
            x = randint(min_x, max_x)

            min_y = (i // 3) * room_height + 1
            max_y = (i // 3 + 1) * room_height - height - 1
            y = randint(min_y, max_y)

            stage.rooms.append(Room(Position(x, y), width, height, i, []))

    @staticmethod
    def create_room_graph(stage: Stage) -> list[set[int]]:
        neighbors = [
            [1, 3],
            [0, 2, 4],
            [1, 5],
            [0, 4, 6],
            [1, 3, 5, 7],
            [2, 4, 8],
            [3, 7],
            [4, 6, 8],
            [5, 7],
        ]

        graph: list[set[int]] = [set() for _ in range(stage.MAX_ROOMS)]

        for room in range(stage.MAX_ROOMS):
            if len(neighbors[room]) == 0:
                continue
            random_neighbor_count: int = randint(1, len(neighbors[room]))
            chosen_neighbors: list[int] = sample(neighbors[room], random_neighbor_count)
            for neighbor in chosen_neighbors:
                graph[room].add(neighbor)
                graph[neighbor].add(room)
                neighbors[neighbor].pop(neighbors[neighbor].index(room))

        return graph

    @staticmethod
    def create_corridors(stage: Stage, graph) -> None:
        rooms = stage.rooms
        for room in rooms:
            for neighbor in graph[room.idx]:
                if neighbor == room.idx + 1 and room.idx % 3 != 2:
                    src = [d for d in room.doors if d.side == 'right']
                    dst = [d for d in rooms[neighbor].doors if d.side == 'left']
                    StageFactory.create_horizontal_corridor(stage, *src, *dst)
                elif neighbor == room.idx + 3:
                    src = [d for d in room.doors if d.side == 'bot']
                    dst = [d for d in rooms[neighbor].doors if d.side == 'top']
                    StageFactory.create_vertical_corridor(stage, *src, *dst)

    @staticmethod
    def create_horizontal_corridor(stage: Stage, door: Door, matching_door: Door) -> None:
        ax, ay = door.position.x, door.position.y
        bx, by = matching_door.position.x, matching_door.position.y

        if ay == by:
            path = [(ax + i, ay) for i in range(bx - ax)]
            corridor = Corridor([Position(x, y) for x, y in path])
            stage.corridors.append(corridor)
            return

        turn = randint(ax + 1, bx - 1)
        path = []
        x_on_turn = 0

        for i in range(bx - ax):
            if ax + i != turn:
                path.append((ax + i, ay))
            else:
                path.append((ax + i, ay))
                x_on_turn = i
                break

        if by < ay:
            for i in range(ay - by + 1):
                path.append((ax + x_on_turn, ay - i))
        else:
            for i in range(by - ay + 1):
                path.append((ax + x_on_turn, ay + i))

        path.extend([(ax + x_on_turn + 1 + i, by) for i in range(bx - turn - 1)])

        corridor = Corridor([Position(x, y) for x, y in path])
        stage.corridors.append(corridor)

    @staticmethod
    def create_vertical_corridor(stage: Stage, door: Door, matching_door: Door) -> None:
        ax, ay = door.position.x, door.position.y
        bx, by = matching_door.position.x, matching_door.position.y

        if ax == bx:
            path = [(ax, ay + i) for i in range(by - ay)]
            corridor = Corridor([Position(x, y) for x, y in path])
            stage.corridors.append(corridor)
            return

        turn = randint(ay + 1, by - 1)
        path = []
        y_on_turn = 0

        for i in range(by - ay):
            if ay + i != turn:
                path.append((ax, ay + i))
            else:
                path.append((ax, ay + i))
                y_on_turn = i
                break

        if bx < ax:
            for i in range(ax - bx + 1):
                path.append((ax - i, ay + y_on_turn))
        else:
            for i in range(bx - ax + 1):
                path.append((ax + i, ay + y_on_turn))

        path.extend([(bx, ay + y_on_turn + 1 + i) for i in range(by - turn - 1)])

        corridor = Corridor([Position(x, y) for x, y in path])
        stage.corridors.append(corridor)

    @staticmethod
    def create_doors(stage: Stage, graph) -> None:
        for room in stage.rooms:
            x, y = room.position.x, room.position.y
            width, height = room.width, room.height

            top = [(x + i, y) for i in range(1, width - 1)]
            left = [(x, y + i) for i in range(1, height - 1)]
            bottom = [(x + i, y + height) for i in range(1, width - 1)]
            right = [(x + width, y + i) for i in range(1, height - 1)]

            for neighbor in graph[room.idx]:
                if neighbor == room.idx + 1 and room.idx % 3 != 2:
                    room.doors.append(Door(Position(*choice(right)), 'right'))
                elif neighbor == room.idx - 1 and room.idx % 3 != 0:
                    room.doors.append(Door(Position(*choice(left)), 'left'))
                elif neighbor == room.idx + 3:
                    room.doors.append(Door(Position(*choice(bottom)), 'bot'))
                elif neighbor == room.idx - 3:
                    room.doors.append(Door(Position(*choice(top)), 'top'))
