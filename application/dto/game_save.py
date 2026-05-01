import time
from dataclasses import dataclass
from pathlib import Path

from application.dto.item import ItemDTO, ItemMapper
from application.dto.player import PlayerDTO, PlayerMapper
from domain.entities.game_session import GameSession
from domain.entities.item import Item
from domain.generators.item import ItemFactory
from domain.templates.item import ITEM_TEMPLATES
from domain.value_objects.enums import ItemRarityType, ItemType
from domain.value_objects.position import Position
from infrastructure.persistence.save_load import SaverLoader

SAVE_FILE = "save/data.json"


def _find_template_key(item_type: ItemType, raw_subtype: int) -> tuple | None:
    for key in ITEM_TEMPLATES:
        if key[0] is item_type and int(key[1]) == raw_subtype:
            return key
    return None


@dataclass
class GameSaveDTO:
    player: PlayerDTO
    items: list[ItemDTO]
    points: int
    time: float


class GameSaveMapper:
    @staticmethod
    def to_dto(session: GameSession) -> GameSaveDTO:
        return GameSaveDTO(
            player=PlayerMapper.to_dto(session.player),
            items=[ItemMapper.to_dto(i) for i in session.player.inventory.items],
            points=session.points,
            time=time.monotonic() - session.start_time,
        )

    @staticmethod
    def to_dict(dto: GameSaveDTO) -> dict:
        return {
            "health": dto.player.health,
            "max_health": dto.player.max_health,
            "dexterity": dto.player.dexterity,
            "strength": dto.player.strength,
            "level": dto.player.level,
            "points": dto.points,
            "time": dto.time,
            "items": [
                {
                    "type": item.type,
                    "subtype": item.subtype,
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
            rotation=0.0,
        )
        items = [
            ItemDTO(
                x=0,
                y=0,
                type=ItemType(item_data.get("type", ItemType.UNDEFINED)),
                subtype=item_data.get("subtype", 0),
                name=item_data.get("name", "?"),
                description=item_data.get("description", "?"),
                value=item_data.get("value", 0),
                rarity=ItemRarityType(item_data.get("rarity", ItemRarityType.COMMON)),
                is_owned=True,
            )
            for item_data in data.get("items", [])
        ]
        return GameSaveDTO(
            player=player,
            items=items,
            points=data.get("points", 0),
            time=data.get("time", 0.0),
        )

    @staticmethod
    def delete() -> bool:
        return Path(SAVE_FILE).unlink(True)

    @staticmethod
    def file_exists() -> bool:
        return Path(SAVE_FILE).exists()

    @staticmethod
    def save(session: GameSession) -> None:
        SaverLoader.save(
            SAVE_FILE, GameSaveMapper.to_dict(GameSaveMapper.to_dto(session))
        )

    @staticmethod
    def load(session: GameSession) -> None:
        dto = GameSaveMapper.from_dict(SaverLoader.load(SAVE_FILE))
        player = dto.player
        session.player.level = max(0, player.level - 1)
        session.new_stage()
        session.player.health = player.health
        session.player.max_health = player.max_health
        session.player.dexterity = player.dexterity
        session.player.strength = player.strength
        session.player.level = player.level
        session.points = dto.points
        session.start_time = time.monotonic() - dto.time
        session.player.inventory.items.clear()
        session.player.weapon = None
        session.items = [item for item in session.items if not item.is_owned]
        for item_dto in dto.items:
            if item_dto.type == ItemType.UNDEFINED:
                continue
            template_key = _find_template_key(item_dto.type, item_dto.subtype)
            if template_key:
                item = ItemFactory.create(template_key, Position())
            else:
                item = Item(
                    position=Position(),
                    type=item_dto.type,
                    name=item_dto.name,
                    description=item_dto.description,
                    value=item_dto.value,
                    rarity=item_dto.rarity,
                )
            item.is_owned = True
            item.rarity = item_dto.rarity
            session.items.append(item)
            session.player.inventory.add_item(item)
