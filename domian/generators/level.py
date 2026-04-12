from random import randint, sample

from domian.entities.corridor import Corridor
from domian.entities.level import Level
from domian.entities.room import Room
from domian.rules.progression import Level as Level_depth
from domian.value_objects.position import Position


class LevelFactory:
    @staticmethod
    def create_level(level: Level, level_depth: Level_depth = Level_depth.LEVEL_1) -> Level:
        LevelFactory.create_rooms(level.rooms)
        graph = LevelFactory.create_room_graph()
        LevelFactory.create_doors(level.rooms, graph)

    @staticmethod
    def create_rooms(rooms: list[Room]):
        for i in range(9):
            width = randint(6, 25)
            height = randint(5, 25)

            left_range_coord = (i % 3) * 27 + 1
            right_range_coord = (i % 3 + 1) * 27 - width - 1
            x_coord = randint(left_range_coord, right_range_coord)

            up_range_coord = round((i / 3) * 10 + 1)
            bottom_range_coord = round((i / 3 + 1) * 10 - height - 1)
            y_coord = randint(up_range_coord, bottom_range_coord)

            rooms.append(Room(Position(x=x_coord, y=y_coord), width=width, height=height))

    @staticmethod
    def create_room_graph():
        neighbors = [(1, 3), (0, 2, 4), (1, 5), (0, 4, 6), (1, 3, 5, 7), (2, 4, 8), (3, 7), (4, 6, 8), (5, 7)]

        graph = [set() for _ in range(9)]

        for room in range(9):
            random_neighbor_count = randint(1, len(neighbors[room]))
            chosen_neighbors = sample(neighbors[room], random_neighbor_count)
            for i in range(len(chosen_neighbors)):
                graph[room].add(chosen_neighbors[i])
                graph[chosen_neighbors[i]].add(room)

        return graph

    @staticmethod
    def create_corridors(rooms: list[Room], corridors: list[Corridor]):
        ...

    @staticmethod
    def create_doors(rooms: list[Room], graph):
        ...