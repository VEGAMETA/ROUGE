from domian.entities.stage import Stage
from domian.generators.stage import StageFactory


def render_stage(stage):
    try:
        from colorama import Fore, Style, init

        init()
    except Exception:

        class _NoColor:
            def getattr(self, _):
                return ""

    w, h = stage.width, stage.height
    grid_ch = [[" " for _ in range(w)] for _ in range(h)]
    grid_kind = [["empty" for _ in range(w)] for _ in range(h)]

    def put(x, y, ch, kind):
        if 0 <= x < w and 0 <= y < h:
            grid_ch[y][x] = ch
            grid_kind[y][x] = kind

    for room in stage.rooms:
        rx, ry = room.position.x, room.position.y
        rw, rh = room.width, room.height

        for x in range(rx, rx + rw + 1):
            put(x, ry, "#", "wall")
            put(x, ry + rh, "#", "wall")
        for y in range(ry, ry + rh + 1):
            put(rx, y, "#", "wall")
            put(rx + rw, y, "#", "wall")

        for y in range(ry + 1, ry + rh):
            for x in range(rx + 1, rx + rw):
                put(x, y, ".", "room")

    for corridor in stage.corridors:
        for p in corridor.path:
            put(p.x, p.y, ".", "corridor")

    for room in stage.rooms:
        for d in room.doors:
            put(d.position.x, d.position.y, "+", "door")

    for y in range(h):
        row_out = []
        for x in range(w):
            # kind = grid_kind[y][x]
            ch = grid_ch[y][x]
            color = ""  # colors.get(kind, "")
            row_out.append(f"{color}{ch}" if color else ch)
        print("".join(row_out))


def test():
    stage = Stage([], [], 90, 20, [])
    StageFactory.create_level(stage)

    render_stage(stage)
