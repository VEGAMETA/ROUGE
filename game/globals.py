from curses import window as CursesWindow


class Globals:
    window: CursesWindow | None = None
    process: bool = True

    @classmethod
    def set_window(cls, value: CursesWindow) -> None:
        cls.window = value

    @classmethod
    def kill_process(cls) -> None:
        cls.process = False
