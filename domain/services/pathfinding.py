from __future__ import annotations

import heapq
import math
from typing import Optional


class Node:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.g: int = 0
        self.h: int = 0
        self.f: int = 0
        self.parent: Optional[Node] = None

    def __hash__(self) -> int:
        return hash(self.x) ^ hash(self.y)

    def __lt__(self, other: Node) -> bool:
        return self.f < other.f

    def __eq__(self, other: Node) -> bool:
        return self.x == other.x and self.y == other.y


def astar(
    start_x: int, start_y: int, end_x: int, end_y: int, obstacles: list[list[bool]]
) -> Optional[list[tuple[int, int]]]:
    start_node: Node = Node(start_x, start_y)
    end_node: Node = Node(end_x, end_y)

    open_list: list[Node] = []
    heapq.heappush(open_list, start_node)

    closed_set: set[Node] = set()

    while open_list:
        current_node: Node = heapq.heappop(open_list)

        if current_node == end_node:
            path: list[tuple[int, int]] = []
            while current_node:
                path.append((current_node.x, current_node.y))
                current_node: Node = current_node.parent
            return path[::-1]

        closed_set.add(current_node)

        neighbors: list[Node] = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                x: int = current_node.x + dx
                y: int = current_node.y + dy
                if x < 0 or x >= len(obstacles[0]) or y < 0 or y >= len(obstacles):
                    continue
                if obstacles[y][x]:
                    continue
                neighbor: Node = Node(x, y)
                neighbors.append(neighbor)

        for neighbor in neighbors:
            if neighbor in closed_set:
                continue

            new_g: int = current_node.g + 1

            if nfo := next((n for n in open_list if n == neighbor), None):
                if new_g < nfo.g:
                    nfo.g = new_g
                    nfo.h = int(
                        math.sqrt((end_node.x - nfo.x) ** 2 + (end_node.y - nfo.y) ** 2)
                    )
                    nfo.f = nfo.g + nfo.h
                    nfo.parent = current_node
                    heapq.heapify(open_list)
            else:
                neighbor.g = new_g
                neighbor.h = int(
                    math.sqrt(
                        (end_node.x - neighbor.x) ** 2 + (end_node.y - neighbor.y) ** 2
                    )
                )
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current_node
                heapq.heappush(open_list, neighbor)

    return None
