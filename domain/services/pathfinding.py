import heapq
import math


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def astar(start, end, obstacles):
    start_node = Node(start[0], start[1])
    end_node = Node(end[0], end[1])

    open_list = []
    heapq.heappush(open_list, start_node)

    closed_set = set()

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node == end_node:
            path = []
            while current_node is not None:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(current_node)

        neighbors = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                x = current_node.x + dx
                y = current_node.y + dy
                if x < 0 or x >= len(obstacles) or y < 0 or y >= len(obstacles[0]):
                    continue
                if obstacles[x][y]:
                    continue
                neighbor = Node(x, y)
                neighbors.append(neighbor)

        for neighbor in neighbors:
            if neighbor in closed_set:
                continue

            new_g = current_node.g + 1

            if nfo := next((n for n in open_list if n == neighbor), None):
                if new_g < nfo.g:
                    nfo.g = new_g
                    nfo.h = math.sqrt(
                        (end_node.x - nfo.x) ** 2 + (end_node.y - nfo.y) ** 2
                    )
                    nfo.f = nfo.g + nfo.h
                    nfo.parent = current_node
                    heapq.heapify(open_list)
            else:
                neighbor.g = new_g
                neighbor.h = math.sqrt(
                    (end_node.x - neighbor.x) ** 2 + (end_node.y - neighbor.y) ** 2
                )
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current_node
                heapq.heappush(open_list, neighbor)

    return None
