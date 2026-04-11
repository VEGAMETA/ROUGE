from presentation.curses.input_handler import CursesInputHandler
from presentation.curses.renderer import CursesRenderer2D
from presentation.input_handler import InputHandler
from presentation.renderer import Renderer

DefaultRenderer: Renderer = CursesRenderer2D()
DefaultInputHandler: InputHandler = CursesInputHandler()
