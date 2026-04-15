from application.dto.game_state import GameStateDTO
from application.dto.tile import TileMapper
from domain.generators.stage import StageFactory
from domain.generators.tiles import TileFactory
from presentation.window import Window


def stage_test(window: Window):
    stage = StageFactory.create_stage(90, 20)
    tiles = map(TileMapper.to_dto, TileFactory.get_tiles(stage))
    window.renderer.render(GameStateDTO(None, [], tiles, []))
    window.renderer.window.getch()
