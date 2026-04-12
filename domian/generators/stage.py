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
                if (neighbor == room.idx + 1) and (room.idx % 3 != 2):
                    door = [door for door in room.doors if door.side == 'right']
                    matching_door = [door for door in rooms[neighbor].doors if door.side == 'left']
                    StageFactory.create_horizontal_corridor(stage, door, *matching_door)
                elif neighbor == (room.idx + 3):
                    door = [door for door in room.doors if door.side == 'bot']
                    matching_door = [door for door in rooms[neighbor].doors if door.side == 'top']
                    StageFactory.create_vertical_corridor(stage, door, *matching_door)

    @staticmethod
    def create_horizontal_corridor(stage: Stage, door: Door, matching_door: Door):
        if door.position.y == matching_door.position.y:
            path = [(door.position.x + i, door.position.y) for i in range(matching_door.position.x - door.position.x)]
            corridor = Corridor([Position(x_y[0], x_y[1]) for x_y in path])
            stage.corridors.append(corridor)
        else:
            turn = randint(door.position.x+1, matching_door.position.x-1)
            path = []
            x_on_turn = 0
            for i in range(matching_door.position.x - door.position.x):
                if door.position.x + i != turn:
                    path.append((door.position.x + i, door.position.y))
                else:
                    x_on_turn = i
                    break
            if matching_door.position.y < door.position.y:
                for i in range(door.position.y, matching_door.position.y):
                    path.append((door.position.x+x_on_turn, door.position.y + i))
            else:
                for i in range(matching_door.position.y, door.position.y):
                    path.append((door.position.x+x_on_turn, door.position.y - i))
            path.extend([(door.position.x + x_on_turn + 1 + i, door.position.y) for i in range(matching_door.position.x - turn)])
            corridor = Corridor([Position(x_y[0], x_y[1]) for x_y in path])
            stage.corridors.append(corridor)

    @staticmethod
    def create_vertical_corridor(stage: Stage, door: Door, matching_door: Door):
        if door.position.x == matching_door.position.x:
            path = [(door.position.x, door.position.y + i) for i in range(matching_door.position.y - door.position.y)]
            corridor = Corridor([Position(x_y[0], x_y[1]) for x_y in path])
            stage.corridors.append(corridor)
        else:
            turn = randint(door.position.y + 1, matching_door.position.y - 1)
            path = []
            y_on_turn = 0
            for i in range(matching_door.position.y - door.position.y):
                if door.position.y + i != turn:
                    path.append((door.position.x, door.position.y + i))
                else:
                    y_on_turn = i
                    break
            if matching_door.position.x < door.position.x:
                for i in range(matching_door.position.x, door.position.x):
                    path.append((door.position.x - i, door.position.y + y_on_turn))
            else:
                for i in range(matching_door.position.y, door.position.y):
                    path.append((door.position.x + i, door.position.y + y_on_turn))
            path.extend([(door.position.x, door.position.y + y_on_turn + 1 + i) for i in
                         range(matching_door.position.y - turn)])
            corridor = Corridor([Position(x_y[0], x_y[1]) for x_y in path])
            stage.corridors.append(corridor)

    @staticmethod
    def create_doors(stage: Stage, graph) -> None:
        rooms = stage.rooms
        for room in rooms:
            x, y = room.position.x, room.position.y
            top_side = [(x+i, y) for i in range(room.width)]
            left_side = [(x, y+i) for i in range(room.height)]
            bot_side = [(x+i, y+room.height) for i in range(room.width)]
            right_side = [(x + room.width, y + i) for i in range(room.height)]
            for neighbor in graph[room.idx]:
                if (neighbor == room.idx + 1) and (room.idx % 3 != 2):
                    door = Door(Position(*choice(right_side)), 'right')
                    room.doors.append(door)
                elif (neighbor == room.idx - 1) and (room.idx % 3 != 0):
                    door = Door(Position(*choice(left_side)), 'left')
                    room.doors.append(door)
                elif neighbor == (room.idx + 3):
                    door = Door(Position(*choice(bot_side)), 'bot')
                    room.doors.append(door)
                elif neighbor == (room.idx - 3):
                    door = Door(Position(*choice(top_side)), 'top')
                    room.doors.append(door)
