from random import randint, sample

from domian.entities.corridor import Corridor
from domian.entities.room import Room
from domian.entities.stage import Stage
from domian.value_objects.position import Position


class StageFactory:
    @staticmethod
    def create_level(stage: Stage) -> Stage:
        StageFactory.create_rooms(stage.rooms)
        graph = StageFactory.create_room_graph()
        StageFactory.create_doors(stage.rooms, graph)

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

            stage.rooms.append(Room(Position(x, y), width, height))

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

        graph = [set() for _ in range(stage.MAX_ROOMS)]

        for room in range(stage.MAX_ROOMS):
            random_neighbor_count = randint(1, len(neighbors[room]))
            chosen_neighbors = sample(neighbors[room], random_neighbor_count)
            for neighbor in chosen_neighbors:
                graph[room].add(neighbor)
                graph[neighbor].add(room)
                neighbors[neighbor].pop(room)

        return graph

    @staticmethod
    def create_corridors(rooms: list[Room], corridors: list[Corridor]): ...

    @staticmethod
    def create_doors(rooms: list[Room], graph): ...
