from dataclasses import dataclass

from application.dto.item import ItemDTO, ItemMapper
from application.dto.player import PlayerDTO, PlayerMapper
from domain.entities.game_session import GameSession
from domain.entities.item import Item
from domain.value_objects.enums import ItemType
from domain.value_objects.position import Position
from infrastructure.persistence.save_load import SaverLoader

SAVE_FILE = "save/data.json"


@dataclass
class GameSaveDTO:
    player: PlayerDTO
    items: list[ItemDTO]


class GameSaveMapper:
    @staticmethod
    def to_dto(session: GameSession) -> GameSaveDTO:
        return GameSaveDTO(
            player=PlayerMapper.to_dto(session.player),
            items=[ItemMapper.to_dto(item) for item in session.items if item.is_owned],
        )

    @staticmethod
    def to_dict(dto: GameSaveDTO) -> dict:
        return {
            "player": {
                "x": dto.player.x,
                "y": dto.player.y,
                "health": dto.player.health,
                "max_health": dto.player.max_health,
                "dexterity": dto.player.dexterity,
                "strength": dto.player.strength,
                "level": int(dto.player.level),
                "rotation": dto.player.rotation,
            },
            "items": [
                {
                    "x": item.x,
                    "y": item.y,
                    "type": item.type.value,
                    "is_owned": item.is_owned,
                    "name": item.name,
                    "description": item.description,
                    "value": item.value,
                }
                for item in dto.items
            ],
        }

    @staticmethod
    def from_dict(data: dict) -> GameSaveDTO:
        player_data = data["player"]
        player = PlayerDTO(
            x=player_data["x"],
            y=player_data["y"],
            health=player_data["health"],
            max_health=player_data["max_health"],
            dexterity=player_data["dexterity"],
            strength=player_data["strength"],
            level=player_data["level"],
            rotation=player_data["rotation"],
        )
        items = [
            ItemDTO(
                x=item_data["x"],
                y=item_data["y"],
                type=ItemType(item_data["type"]),
                is_owned=item_data["is_owned"],
                name=item_data["name"],
                description=item_data["description"],
                value=item_data["value"],
            )
            for item_data in data["items"]
        ]
        return GameSaveDTO(player=player, items=items)

    @staticmethod
    def save(session: GameSession) -> None:
        dto = GameSaveMapper.to_dto(session)
        SaverLoader.save(SAVE_FILE, GameSaveMapper.to_dict(dto))

    @staticmethod
    def load(session: GameSession) -> None:
        data = SaverLoader.load(SAVE_FILE)
        dto = GameSaveMapper.from_dict(data)
        player = dto.player
        session.player.position.x = player.x
        session.player.position.y = player.y
        session.player.health = player.health
        session.player.max_health = player.max_health
        session.player.dexterity = player.dexterity
        session.player.strength = player.strength
        session.player.level = player.level
        session.player.rotation = player.rotation
        owned = [
            Item(
                position=Position(item_dto.x, item_dto.y),
                type=item_dto.type,
                is_owned=item_dto.is_owned,
                name=item_dto.name,
                description=item_dto.description,
                value=item_dto.value,
            )
            for item_dto in dto.items
        ]
        session.items = [item for item in session.items if not item.is_owned] + owned
