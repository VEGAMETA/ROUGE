import heapq
from typing import Optional

DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def chebyshev_distance(dx: int, dy: int) -> int:
    """Октайльное расстояние (max) - быстрее чем sqrt"""
    return max(abs(dx), abs(dy))


def octile_distance(dx: int, dy: int) -> int:
    """Более точное октаильное расстояние для 8 направлений"""
    return max(abs(dx), abs(dy)) * 10 + (min(abs(dx), abs(dy)) * 4)
    # 10 и 4 вместо 1 и 0.414 для целочисленной арифметики


def astar(
    start_x: int, start_y: int, end_x: int, end_y: int, obstacles: list[list[bool]]
) -> Optional[list[tuple[int, int]]]:
    # if obstacles[start_y][start_x] or obstacles[end_y][end_x]:
    #     return None

    height, width = len(obstacles), len(obstacles[0])
    total_cells = width * height
    g_score = [100_000_000] * total_cells
    parent = [-1] * total_cells

    def pack(x: int, y: int) -> int:
        return y * width + x

    def unpack(idx: int) -> tuple[int, int]:
        return (idx % width, idx // width)

    start_idx = pack(start_x, start_y)
    end_idx = pack(end_x, end_y)
    g_score[start_idx] = 0

    open_heap = [(chebyshev_distance(start_x - end_x, start_y - end_y), 0, start_idx)]

    closed = [False] * total_cells

    while open_heap:
        f_score, _, current_idx = heapq.heappop(open_heap)

        if closed[current_idx]:
            continue

        if current_idx == end_idx:
            path = []
            while current_idx != -1:
                x, y = unpack(current_idx)
                path.append((x, y))
                current_idx = parent[current_idx]
            return path[::-1]

        closed[current_idx] = True
        current_x, current_y = unpack(current_idx)
        current_g = g_score[current_idx]

        for dx, dy in DIRS:
            nx, ny = current_x + dx, current_y + dy

            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue

            if obstacles[ny][nx]:
                continue

            neighbor_idx = pack(nx, ny)

            if closed[neighbor_idx]:
                continue

            if dx != 0 and dy != 0:
                move_cost = 14  # sqrt(2) * 10 ≈ 14
            else:
                move_cost = 10

            new_g = current_g + move_cost

            if new_g < g_score[neighbor_idx]:
                g_score[neighbor_idx] = new_g
                parent[neighbor_idx] = current_idx
                # Октайльная эвристика (точная для 8 направлений)
                h = octile_distance(nx - end_x, ny - end_y)
                f = new_g + h
                heapq.heappush(open_heap, (f, new_g, neighbor_idx))
    return None
