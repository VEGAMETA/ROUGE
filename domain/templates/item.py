from functools import partial

from domain.entities.consumables import Consumable
from domain.entities.item import Item
from domain.entities.scroll import Scroll
from domain.entities.weapon import Weapon
from domain.value_objects.enums import (
    ConsumableType,
    ItemType,
    TreasureType,
    WeaponType,
)

CONSUMABLE_TEMPLATES = {
    (ItemType.CONSUMABLE, ConsumableType.FOOD): partial(
        Consumable,
        subtype=ConsumableType.FOOD,
        name="Food Ration",
        description="Restores 50 HP",
        health=50,
        max_health=0,
        dexterity=0,
        strength=0,
        value=500,
    ),
    (ItemType.CONSUMABLE, ConsumableType.HEALTH): partial(
        Consumable,
        subtype=ConsumableType.HEALTH,
        name="Healing Potion",
        description="Restores 100 HP",
        health=100,
        max_health=0,
        dexterity=0,
        strength=0,
        value=1000,
    ),
    (ItemType.CONSUMABLE, ConsumableType.STRENGTH): partial(
        Consumable,
        subtype=ConsumableType.STRENGTH,
        name="Elixir of Strength",
        description="Temporarily increases strength by 5",
        health=0,
        max_health=0,
        dexterity=0,
        strength=5,
        value=1000,
    ),
    (ItemType.CONSUMABLE, ConsumableType.DEXTERITY): partial(
        Consumable,
        subtype=ConsumableType.DEXTERITY,
        name="Elixir of Agility",
        description="Temporarily increases dexterity by 5",
        health=0,
        max_health=0,
        dexterity=5,
        strength=0,
        value=1000,
    ),
}

WEAPON_TEMPLATES = {
    (ItemType.WEAPON, WeaponType.DAGGER): partial(
        Weapon,
        subtype=WeaponType.DAGGER,
        name="Dagger",
        description="A short, quick blade",
        damage=5,
        value=100,
    ),
    (ItemType.WEAPON, WeaponType.MACE): partial(
        Weapon,
        subtype=WeaponType.MACE,
        name="Mace",
        description="A heavy blunt weapon",
        damage=10,
        value=300,
    ),
    (ItemType.WEAPON, WeaponType.SWORD): partial(
        Weapon,
        subtype=WeaponType.SWORD,
        name="Iron Sword",
        description="A sturdy iron sword",
        damage=10,
        value=500,
    ),
    (ItemType.WEAPON, WeaponType.SPEAR): partial(
        Weapon,
        subtype=WeaponType.SPEAR,
        name="Spear",
        description="A long thrusting weapon",
        damage=15,
        value=1000,
    ),
    (ItemType.WEAPON, WeaponType.AXE): partial(
        Weapon,
        subtype=WeaponType.AXE,
        name="War Axe",
        description="A brutal axe",
        damage=15,
        value=1000,
    ),
    (ItemType.WEAPON, WeaponType.STAFF): partial(
        Weapon,
        subtype=WeaponType.STAFF,
        name="Magic Staff",
        description="Channels arcane power",
        damage=15,
        value=1000,
    ),
    (ItemType.WEAPON, WeaponType.TWO_HANDED_SWORD): partial(
        Weapon,
        subtype=WeaponType.TWO_HANDED_SWORD,
        name="Greatsword",
        description="A massive sword for powerful strikes",
        damage=20,
        value=2000,
    ),
}

TREASURE_TEMPLATES = {
    (ItemType.TREASURE, TreasureType.SILVER): partial(
        Item,
        type=ItemType.TREASURE,
        subtype=TreasureType.SILVER,
        name="Silver Coins",
        description="Shiny silver coins",
        value=100,
    ),
    (ItemType.TREASURE, TreasureType.GOLD): partial(
        Item,
        type=ItemType.TREASURE,
        subtype=TreasureType.GOLD,
        name="Gold Coins",
        description="Shiny gold coins",
        value=500,
    ),
    (ItemType.TREASURE, TreasureType.GEM): partial(
        Item,
        type=ItemType.TREASURE,
        subtype=TreasureType.GEM,
        name="Gemstone",
        description="A sparkling gemstone",
        value=1000,
    ),
    (ItemType.TREASURE, TreasureType.RUBY): partial(
        Item,
        type=ItemType.TREASURE,
        subtype=TreasureType.RUBY,
        name="Ruby",
        description="A precious ruby",
        value=2500,
    ),
    (ItemType.TREASURE, TreasureType.SAPPHIRE): partial(
        Item,
        type=ItemType.TREASURE,
        subtype=TreasureType.SAPPHIRE,
        name="Sapphire",
        description="A brilliant sapphire",
        value=5000,
    ),
}

SCROLL_TEMPLATES = {
    (ItemType.SCROLL, ConsumableType.STRENGTH): partial(
        Scroll,
        subtype=ConsumableType.STRENGTH,
        name="Scroll of Strength",
        description="Permanently increases strength by 5",
        health=0,
        max_health=0,
        dexterity=0,
        strength=5,
        value=4000,
    ),
    (ItemType.SCROLL, ConsumableType.DEXTERITY): partial(
        Scroll,
        subtype=ConsumableType.DEXTERITY,
        name="Scroll of Agility",
        description="Permanently increases dexterity by 5",
        health=0,
        max_health=0,
        dexterity=5,
        strength=0,
        value=3000,
    ),
    (ItemType.SCROLL, ConsumableType.HEALTH): partial(
        Scroll,
        subtype=ConsumableType.HEALTH,
        name="Scroll of Healing",
        description="Restores HP",
        health=9999,
        max_health=0,
        dexterity=0,
        strength=0,
        value=1000,
    ),
    (ItemType.SCROLL, ConsumableType.MAX_HEALTH): partial(
        Scroll,
        subtype=ConsumableType.MAX_HEALTH,
        name="Scroll of Vitality",
        description="Permanently increases max HP by 50",
        health=0,
        max_health=50,
        dexterity=0,
        strength=0,
        value=5000,
    ),
}

ITEM_TEMPLATES = {}
ITEM_TEMPLATES.update(CONSUMABLE_TEMPLATES)
ITEM_TEMPLATES.update(WEAPON_TEMPLATES)
ITEM_TEMPLATES.update(SCROLL_TEMPLATES)

ENEMY_DROP = {}
ITEM_TEMPLATES.update(CONSUMABLE_TEMPLATES)
ITEM_TEMPLATES.update(WEAPON_TEMPLATES)
ITEM_TEMPLATES.update(SCROLL_TEMPLATES)
ENEMY_DROP.update(TREASURE_TEMPLATES)
