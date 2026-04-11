from domian.value_objects.enums import ItemRarityType, Level

ITEM_RARITY_WEIGHTS = {
    Level.LEVEL_1: {
        ItemRarityType.COMMON: 10,
        ItemRarityType.RARE: 2,
        ItemRarityType.EPIC: 1,
        ItemRarityType.LEGENDARY: 1,
    },
    Level.LEVEL_2: {
        ItemRarityType.COMMON: 8,
        ItemRarityType.RARE: 2,
        ItemRarityType.EPIC: 1,
        ItemRarityType.LEGENDARY: 1,
    },
    Level.LEVEL_3: {
        ItemRarityType.COMMON: 5,
        ItemRarityType.RARE: 2,
        ItemRarityType.EPIC: 2,
        ItemRarityType.LEGENDARY: 1,
    },
    Level.LEVEL_4: {
        ItemRarityType.COMMON: 4,
        ItemRarityType.RARE: 2,
        ItemRarityType.EPIC: 2,
        ItemRarityType.LEGENDARY: 1,
    },
    Level.LEVEL_5: {
        ItemRarityType.COMMON: 4,
        ItemRarityType.RARE: 3,
        ItemRarityType.EPIC: 3,
        ItemRarityType.LEGENDARY: 2,
    },
    Level.LEVEL_6: {
        ItemRarityType.COMMON: 3,
        ItemRarityType.RARE: 4,
        ItemRarityType.EPIC: 4,
        ItemRarityType.LEGENDARY: 2,
    },
    Level.LEVEL_7: {
        ItemRarityType.COMMON: 1,
        ItemRarityType.RARE: 2,
        ItemRarityType.EPIC: 5,
        ItemRarityType.LEGENDARY: 2,
    },
    Level.LEVEL_8: {
        ItemRarityType.COMMON: 1,
        ItemRarityType.RARE: 2,
        ItemRarityType.EPIC: 3,
        ItemRarityType.LEGENDARY: 3,
    },
    Level.LEVEL_9: {
        ItemRarityType.COMMON: 1,
        ItemRarityType.RARE: 2,
        ItemRarityType.EPIC: 3,
        ItemRarityType.LEGENDARY: 5,
    },
}
