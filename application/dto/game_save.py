import dataclasses
import time
from dataclasses import dataclass
from pathlib import Path

from application.dto.enemy import EnemyDTO, EnemyMaper
from application.dto.item import ItemDTO, ItemMapper
from application.dto.player import PlayerDTO, PlayerMapper
from domain.entities.enemy import Enemy
from domain.entities.game_session import GameSession
from domain.entities.item import Item
from domain.generators.item import ItemFactory
from domain.rules.progression import Level
from domain.templates.item import ITEM_TEMPLATES
from domain.value_objects.enums import EnemyType, ItemRarityType, ItemType
from domain.value_objects.position import Position
from infrastructure.persistence.save_load import SaverLoader

SAVE_FILE = "save/data.json"


def _find_template_key(item_type: ItemType, raw_subtype: int) -> tuple | None:
    for key in ITEM_TEMPLATES:
        if key[0] is item_type and int(key[1]) == raw_subtype:
            return key
    return None


def restore_item(item_dto: ItemDTO, session: GameSession, owned: bool) -> None:
    if ItemType(item_dto.type) == ItemType.UNDEFINED:
        return
    pos = Position(item_dto.x, item_dto.y)
    template_key = _find_template_key(ItemType(item_dto.type), item_dto.subtype)
    if template_key:
        item = ItemFactory.create(template_key, pos)
    else:
        item = Item(
            position=pos,
            type=ItemType(item_dto.type),
            name=item_dto.name,
            description=item_dto.description,
            value=item_dto.value,
        )
    item.rarity = ItemRarityType(item_dto.rarity)
    item.is_owned = owned
    session.items.append(item)
    if owned:
        session.player.inventory.add_item(item)


@dataclass
class GameSaveDTO:
    player: PlayerDTO
    items: list[ItemDTO]
    floor_items: list[ItemDTO]
    enemies: list[EnemyDTO]
    entered_rooms: list[int]
    statistics: dict
    points: int
    time: float
    player_x: int
    player_y: int


class GameSaveMapper:
    @staticmethod
    def to_dto(session: GameSession) -> GameSaveDTO:
        return GameSaveDTO(
            player=PlayerMapper.to_dto(session.player),
            items=[ItemMapper.to_dto(i) for i in session.player.inventory.items],
            floor_items=[ItemMapper.to_dto(i) for i in session.items if not i.is_owned],
            enemies=[EnemyMaper.to_dto(e) for e in session.enemies],
            entered_rooms=sorted(session.entered_rooms),
            statistics={
                f.name: getattr(session.statistics, f.name)
                for f in dataclasses.fields(session.statistics)
            },
            points=session.points,
            time=time.monotonic() - session.start_time,
            player_x=session.player.position.x,
            player_y=session.player.position.y,
        )

    @staticmethod
    def to_dict(dto: GameSaveDTO) -> dict:
        return {
            "health": dto.player.health,
            "max_health": dto.player.max_health,
            "dexterity": dto.player.dexterity,
            "strength": dto.player.strength,
            "level": dto.player.level,
            "player_x": dto.player_x,
            "player_y": dto.player_y,
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
            "floor_items": [
                {
                    "x": item.x,
                    "y": item.y,
                    "type": item.type,
                    "subtype": item.subtype,
                    "name": item.name,
                    "description": item.description,
                    "rarity": item.rarity,
                    "value": item.value,
                }
                for item in dto.floor_items
            ],
            "enemies": [
                {
                    "x": e.x,
                    "y": e.y,
                    "type": e.type,
                    "health": e.health,
                    "max_health": e.max_health,
                    "dexterity": e.dexterity,
                    "strength": e.strength,
                    "level": e.level,
                    "hostility": e.hostility,
                    "home_room_index": e.home_room_index,
                }
                for e in dto.enemies
            ],
            "entered_rooms": dto.entered_rooms,
            "statistics": dto.statistics,
        }

    @staticmethod
    def from_dict(data: dict) -> GameSaveDTO:
        player = PlayerDTO(
            x=data.get("player_x", 0),
            y=data.get("player_y", 0),
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
        floor_items = [
            ItemDTO(
                x=item_data.get("x", 0),
                y=item_data.get("y", 0),
                type=ItemType(item_data.get("type", ItemType.UNDEFINED)),
                subtype=item_data.get("subtype", 0),
                name=item_data.get("name", "?"),
                description=item_data.get("description", "?"),
                value=item_data.get("value", 0),
                rarity=ItemRarityType(item_data.get("rarity", ItemRarityType.COMMON)),
                is_owned=False,
            )
            for item_data in data.get("floor_items", [])
        ]
        enemies = [
            EnemyDTO(
                x=e.get("x", 0),
                y=e.get("y", 0),
                type=e.get("type", 1),
                health=e.get("health", 1),
                max_health=e.get("max_health", 1),
                dexterity=e.get("dexterity", 1),
                strength=e.get("strength", 1),
                level=e.get("level", 0),
                hostility=e.get("hostility", 1),
                home_room_index=e.get("home_room_index", -1),
            )
            for e in data.get("enemies", [])
        ]
        return GameSaveDTO(
            player=player,
            items=items,
            floor_items=floor_items,
            enemies=enemies,
            entered_rooms=data.get("entered_rooms", []),
            statistics=data.get("statistics", {}),
            points=data.get("points", 0),
            time=data.get("time", 0.0),
            player_x=data.get("player_x", 0),
            player_y=data.get("player_y", 0),
        )

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
        session.player.position = Position(dto.player_x, dto.player_y)
        session.points = dto.points
        session.start_time = time.monotonic() - dto.time

        session.enemies = set()
        for ed in dto.enemies:
            session.enemies.add(
                Enemy(
                    position=Position(ed.x, ed.y),
                    type=EnemyType(ed.type),
                    health=ed.health,
                    max_health=ed.max_health,
                    dexterity=ed.dexterity,
                    strength=ed.strength,
                    level=Level(ed.level),
                    path=[],
                    hostility=ed.hostility,
                    home_room_index=ed.home_room_index,
                )
            )

        session.items = [i for i in session.items if i.is_owned]
        session.player.inventory.items.clear()
        session.player.weapon = None
        for item_dto in dto.items:
            restore_item(item_dto, session, owned=True)
        for item_dto in dto.floor_items:
            restore_item(item_dto, session, owned=False)

        session.entered_rooms = set(dto.entered_rooms)
        session.update_visibility()

        for key, val in dto.statistics.items():
            if hasattr(session.statistics, key):
                setattr(session.statistics, key, val)
