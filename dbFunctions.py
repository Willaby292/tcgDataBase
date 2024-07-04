insertCard = """
    INSERT INTO cards_HS (
        card_id
    ,   "name"
    ,   mana_cost
    ,   attack
    ,   health
    ,   "durability"
    ,   "text"
    ,   armor
    ,   collectible
    ,   flavor_text
    ,   "image"
    ,   image_gold
    ,   crop_image
    ,   artist_name
    ,   slug
    ,   class_id
    ,   card_type_id
    ,   card_set_id
    ,   rarity_id
    ,   minion_type_id
    ,   spell_school_id
    ,   copy_of_card_id
    ,   parent_id
    ,   is_zilliax_functional_module
    ,   is_zilliax_cosmetic_module
    ,   banned_from_sideboard
    ,   max_sideboard_cards
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    );
"""

def executeInsertCard(cursor, card):
    cursor.execute(insertCard, (
        card.get('id')
    ,   card.get('name')
    ,   card.get('manaCost')
    ,   card.get('attack')
    ,   card.get('health')
    ,   card.get('durability')
    ,   card.get('text')
    ,   card.get('armor')
    ,   card.get('collectible')
    ,   card.get('flavorText')
    ,   card.get('image')
    ,   card.get('imageGold')
    ,   card.get('cropImage')
    ,   card.get('artistName')
    ,   card.get('slug')
    ,   card.get('classId')
    ,   card.get('cardTypeId')
    ,   card.get('cardSetId')
    ,   card.get('rarityId')
    ,   card.get('minionTypeId')
    ,   card.get('spellSchoolId')
    ,   card.get('copyOfCardId')
    ,   card.get('parentId')
    ,   card.get('isZilliaxFunctionalModule')
    ,   card.get('isZilliaxCosmeticModule')
    ,   card.get('bannedFromSideboard')
    ,   card.get('maxSideboardCards')
    ))
    cursor.connection.commit()

insertClasses = """
    INSERT INTO classes_HS(
        class_id
    ,   hero_card_id
    ,   class_name
    ,   hero_power_card_id
    ,   slug
    ) VALUES(
        %s, %s, %s, %s, %s
    )
"""
def executeInsertClass(cursor, classes):
    cursor.execute(insertClasses,(
        classes.get('id')
    ,   classes.get('cardId')
    ,   classes.get('name')
    ,   classes.get('heroPowerCardId')
    ,   classes.get('slug')
    ))
    cursor.connection.commit()

insertClassesLink = """
    INSERT INTO classes_link_HS(
        card_id
    ,   class_id
    ) VALUES(
        %s, %s
    )
"""

def executeInsertClassLink(cursor , cardId, classId):
    cursor.execute(insertClassesLink, (
        cardId
    ,   classId
    ))
    cursor.connection.commit()

insertAlternateHeros = """
    INSERT INTO alternate_heros_HS(
        class_id
    ,   alt_hero_card_id
    ) VALUES(
        %s, %s
    )
"""

def executeInsertAlternateHeros(cursor , classes, altHeroId):
    cursor.execute(insertAlternateHeros,( #just change insertAlternateHeros to insertClassesLink
        altHeroId
    ,   classes.get('id')
    ))
    cursor.connection.commit()


insertRarities = """
    INSERT INTO rarities_HS(
        rarity_id
    ,   crafting_cost_normal
    ,   crafting_cost_golden
    ,   dust_value_normal
    ,   dust_value_golden
    ,   rarity_name
    ,   slug
    ) VALUES(
        %s, %s, %s, %s, %s, %s, %s
    )
"""

def executeInsertRarities(cursor, rarity):
    try:
        craftingCostNormal = min(rarity.get('craftingCost'))
        craftingCostGold = max(rarity.get('craftingCost'))
    except TypeError:
        craftingCostNormal = None
        craftingCostGold = None
    try:
        dustValueNormal = min(rarity.get('dustValue'))
        dustValueGold = max(rarity.get('dustValue'))
    except TypeError:
        dustValueNormal = None
        dustValueGold = None
    cursor.execute(insertRarities,(
            rarity.get('id')
        ,   craftingCostNormal
        ,   craftingCostGold
        ,   dustValueNormal
        ,   dustValueGold
        ,   rarity.get('name')
        ,   rarity.get('slug')
    ))
    cursor.connection.commit()

insertBGCards = """
    INSERT INTO bg_cards_HS(
        card_id
    ,   tier
    ,   is_hero
    ,   is_quest
    ,   is_reward
    ,   is_duos_only
    ,   is_solos_only
    ,   upgrade_id
    ,   "image"
    ,   image_gold
    ) VALUES(
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
"""

def executeInsertBGCards(cursor , card):
    cursor.execute(insertBGCards, (
        card.get('id')
    ,   card.get('battlegrounds').get('tier')
    ,   card.get('battlegrounds').get('hero')
    ,   card.get('battlegrounds').get('quest')
    ,   card.get('battlegrounds').get('reward')
    ,   card.get('battlegrounds').get('duosOnly')
    ,   card.get('battlegrounds').get('solosOnly')
    ,   card.get('battlegrounds').get('upgradeId')
    ,   card.get('battlegrounds').get('image')
    ,   card.get('battlegrounds').get('imageGold')
    ))
    cursor.connection.commit()

insertSetGroups = """
    INSERT INTO set_groups_HS(
        set_group_name
    ,   is_standard
    ,   svg
    ,   icon
    ,   year
    ,   year_range
    ,   slug
    ) VALUES(
        %s, %s, %s, %s, %s, %s, %s
    )
"""

def executeInsertSetGroups(cursor, setGroup):
    cursor.execute(insertSetGroups,(
            setGroup.get('name')
        ,   setGroup.get('standard')
        ,   setGroup.get('svg')
        ,   setGroup.get('icon')
        ,   setGroup.get('year')
        ,   setGroup.get('yearRange')
        ,   setGroup.get('slug')
        ))
    cursor.connection.commit()

insertSets = """
    INSERT INTO sets_HS(
        set_id
    ,   set_name
    ,   is_hyped
    ,   set_type
    ,   collectible_count
    ,   collectible_revealed_count
    ,   non_collectible_count
    ,   non_collectible_reavealed_count
    ,   slug
    ) VALUES(
        %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
"""

def executeInsertSet(cursor, set):
    cursor.execute(insertSets,(
        set.get('id')
    ,   set.get('name')
    ,   set.get('hyped')
    ,   set.get('type')
    ,   set.get('collectibleCount')
    ,   set.get('collectibleRevealedCount')
    ,   set.get('nonCollectibleCount')
    ,   set.get('nonCollectibleReavealedCount')
    ,   set.get('slug')
    ))
    cursor.connection.commit()


insertSetsLinkSetGroups = """
    INSERT INTO sets_link_set_groups_HS(
        set_id
    ,   set_group_id
    ) VALUES(
        %s, %s
    )
"""

def executeInsertSetsLinkSetGroups(cursor, set, setGroupId):
    cursor.execute(insertSetsLinkSetGroups,(
        set.get('id')
    ,   setGroupId
    ))
    cursor.connection.commit()


insertSetsAlias = """
    INSERT INTO set_alias_HS(
        set_id
    ,   alias_id
    ) VALUES(
        %s, %s
    )
"""

def executeInsertSetsAlias(cursor, set, alias):
    cursor.execute(insertSetsAlias, (
        set.get('id')
    ,   alias
    ))
    cursor.connection.commit()

insertRuneCosts = """
    INSERT INTO rune_costs_HS(
        card_id
    ,   blood_rune_count
    ,   frost_rune_count
    ,   unholy_rune_count
    ) VALUES(
        %s, %s, %s, %s
    )
"""

def executeInsertRuneCosts(cursor , cardId, runeCostBlood, runeCostFrost, runeCostUnholy):
    cursor.execute(insertRuneCosts,(
        cardId
    ,   runeCostBlood
    ,   runeCostFrost
    ,   runeCostUnholy
    ))
    cursor.connection.commit()

insertMinionType = """
    INSERT INTO minion_types_HS(
        minion_type_id
    ,   minion_type_name
    ,   slug
    ) VALUES(
        %s, %s, %s
    )
"""

def executeInsertMinionType(cursor, minionType):
    cursor.execute(insertMinionType,(
        minionType.get('id')
    ,   minionType.get('name')
    ,   minionType.get('slug')
    ))
    cursor.connection.commit()

insertMinionTypesLink = """
    INSERT INTO minion_types_link_HS(
        card_id
    ,   minion_type_id
    ) VALUES(
        %s, %s
    )
"""

def executeInsertMinionTypesLink(cursor , cardId, typeId):
    cursor.execute(insertMinionTypesLink, (
        cardId
    ,   typeId
    ))
    cursor.connection.commit()

insertGameModes = """
    INSERT INTO game_modes_HS(
        game_mode_id
    ,   game_mode_name
    ,   slug
    ) VALUES(
        %s, %s, %s
    )
"""


def executeInsertGameMode(cursor, gameMode):
    cursor.execute(insertGameModes,(
        gameMode.get('id')
    ,   gameMode.get('name')
    ,   gameMode.get('slug')
    ))
    cursor.connection.commit()


insertMinionTypesLinkGameMode = """
    INSERT INTO minion_types_link_game_modes_HS(
        minion_type_id
    ,   game_mode_id
    ) VALUES(
        %s, %s
    )
"""

def executeInsertMinionTypeLinkGameMode(cursor, minionType, gameMode):
    cursor.execute(insertMinionTypesLinkGameMode, (
        minionType.get('id')
    ,   gameMode
    ))
    cursor.connection.commit()



insertKeyword = """
    INSERT INTO keywords_HS(
        keyword_id
    ,   keyword_name
    ,   keyword_text
    ,   ref_text
    ,   slug
    ) VALUES(
        %s, %s, %s, %s, %s
    )
"""

def executeInsertKeyword(cursor, keyword):
    cursor.execute(insertKeyword,(
        keyword.get('id')
    ,   keyword.get('name')
    ,   keyword.get('text')
    ,   keyword.get('refText')
    ,   keyword.get('slug')
    ))
    cursor.connection.commit()

insertKeywordsLink = """
    INSERT INTO keywords_link_HS(
        card_id
    ,   keyword_id
    ) VALUES(
        %s, %s
    )
"""

def executeInsertKeywordsLink(cursor , cardId, keywordId):
    cursor.execute(insertKeywordsLink, (
        cardId
    ,   keywordId
    ))
    cursor.connection.commit()

insertKeywordsLinkGameModes = """
    INSERT INTO keywords_link_game_modes_HS(
        keyword_id
    ,   game_mode_id
    ) VALUES(
        %s, %s
    )
"""

def executeInsertKeywordLinkGameModes(cursor, keyword, gameMode):
    cursor.execute(insertKeywordsLinkGameModes, (
        keyword.get('id')
    ,   gameMode
    ))
    cursor.connection.commit()

insertTypes = """
    INSERT INTO types_HS(
        type_id
    ,   type_name
    ,   slug
    ) VALUES(
        %s, %s, %s
    )
"""

def executeInsertType(cursor, type):
    cursor.execute(insertTypes,(
        type.get('id')
    ,   type.get('name')
    ,   type.get('slug')
    ))
    cursor.connection.commit()

insertTypesLinkGameModes = """
    INSERT INTO types_link_game_modes_HS(
        type_id
    ,   game_mode_id
    ) VALUES(
        %s, %s
    )
"""

def executeInsertTypesLinkGameModes(cursor, type, mode):
    cursor.execute(insertTypesLinkGameModes,(
        type.get('id')
    ,   mode
    ))

insertSpellSchool = """
    INSERT INTO spell_schools_HS(
        spell_school_id
    ,   spell_school_name
    ,   slug
    ) VALUES(
        %s, %s, %s
    )
"""
def executeInsertSpellSchool(cursor, spellSchool):
    cursor.execute(insertSpellSchool,(
        spellSchool.get('id')
    ,   spellSchool.get('name')
    ,   spellSchool.get('slug')
    ))
    cursor.connection.commit()

insertCardRemap = """
    INSERT INTO card_remap_HS(
        parent_id
    ,   child_id
    ) VALUES(
        %s, %s
    )
"""

def executeInsertCardRemap(cursor , cardId, childId):
    cursor.execute(insertCardRemap, (
        cardId
    ,   childId
    ))
    cursor.connection.commit()

insertBGGameModes = """
    INSERT INTO bg_game_modes_HS(
        bg_game_mode_id
    ,   bg_game_mode_name
    ,   slug
    ) VALUES(
        %s, %s, %s
    )
"""


def executeInsertBGGameMode(cursor, bgGameMode):
    cursor.execute(insertBGGameModes,(
        bgGameMode.get('id')
    ,   bgGameMode.get('name')
    ,   bgGameMode.get('slug')
    ))
    cursor.connection.commit()


selectSetGroupId = """
    SELECT set_group_id
    FROM set_groups_HS
    WHERE set_group_name = (%s)
    """