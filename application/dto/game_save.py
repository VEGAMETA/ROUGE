from dataclasses import dataclass

from application.dto.item import ItemDTO, ItemMapper
from application.dto.player import PlayerDTO, PlayerMapper
from domain.entities.game_session import GameSession
from domain.entities.item import Item
from domain.value_objects.enums import ItemRarityType, ItemType
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
            items=[ItemMapper.to_dto(i) for i in session.items if i.is_owned],
        )

    @staticmethod
    def to_dict(dto: GameSaveDTO) -> dict:
        return {
            "health": dto.player.health,
            "max_health": dto.player.max_health,
            "dexterity": dto.player.dexterity,
            "strength": dto.player.strength,
            "level": dto.player.level,
            "items": [
                {
                    "type": item.type,
                    "name": item.name,
                    "description": item.description,
                    "rarity": item.rarity,
                    "value": item.value,
                }
                for item in dto.items
            ],
        }

    @staticmethod
    def from_dict(data: dict) -> GameSaveDTO:
        player = PlayerDTO(
            x=0,
            y=0,
            health=data.get("health", 1),
            max_health=data.get("max_health", 1),
            dexterity=data.get("dexterity", 1),
            strength=data.get("strength", 1),
            level=data.get("level", 0),
        )
        items = [
            ItemDTO(
                x=0,
                y=0,
                type=ItemType.get("type", ItemType.UNDEFINED),
                name=item_data.get("name", "?"),
                description=item_data.get("description", "?"),
                value=item_data.get("value", 0),
                rarity=item_data.get("rarity", ItemRarityType.COMMON),
                is_owned=True,
            )
            for item_data in data.get("items")
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
        session.player.health = player.health
        session.player.max_health = player.max_health
        session.player.dexterity = player.dexterity
        session.player.strength = player.strength
        session.player.level = player.level
        session.new_stage(player.level - 1)
        session.items.extend(
            [
                Item(
                    position=Position(),
                    type=item_dto.type,
                    name=item_dto.name,
                    description=item_dto.description,
                    value=item_dto.value,
                    rarity=item_dto.rarity,
                    is_owned=True,
                )
                for item_dto in dto.items
                if item_dto.type != ItemType.UNDEFINED
            ]
        )
