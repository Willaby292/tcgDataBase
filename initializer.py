import psycopg2
import json
import requests # for handling api calls
import subprocess
import time
import os
from collections import defaultdict
from dotenv import load_dotenv

# TODO create versioning of the data so that each time its updated I can check to see changes

load_dotenv()
PSQL_PASSWORD = os.getenv('PSQL_PASSWORD')
API_TOKEN = os.getenv('API_TOKEN')

pageSize = 500
cardSearchUrl = 'https://us.api.blizzard.com/hearthstone/cards?locale=en_US&access_token='+API_TOKEN
metaDataSearchUrl = 'https://us.api.blizzard.com/hearthstone/metadata?locale=en_US&access_token='+API_TOKEN
collectible = '0,1'

# TODO change camel case to snake case in SQL
# TODO type cast variables when instanced
# TODO find hidden data like hero card data
# TODO insert or update

# TODO can i add catch blocks to catch foriegn key missing and then add it to the main value
# The plan for this is to catch execptions on the inserts and put them in a data structure to be handled at the end of the init

# Programatic authentication has not been set up. To get API token go to 'https://develop.battle.net/documentation/hearthstone/game-data-apis'.
# Use the TRY IT button on one of the example api requests and then copy and paste in the token at the end of the given url.
# If the TRY IT button take you to a page that says state parameter not provided simply add &state='' at the end of the url.


###############################################################
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
    cursor.execute(insertClassesLink, (## have to have classes and cards initialized first. the entire card import should probably just be run second
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
        classes.get('id')
    ,   altHeroId
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

# def executeInsertRarities(cursor , x):
# cursor.connection.commit()


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

# def executeInsertSetGroups(cursor , x):
# cursor.connection.commit()

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

# def executeInsertSets(cursor , x):
# cursor.connection.commit()

insertSetsLinkSetGroups = """
    INSERT INTO sets_link_set_groups_HS(
        set_id
    ,   set_group_id
    ) VALUES(
        %s, %s
    )
"""

# def executeInsertSetsLinkSetGroups(cursor , x):
# cursor.connection.commit()

insertSetsAlias = """
    INSERT INTO set_alias_HS(
        set_id
    ,   alias_id
    ) VALUES(
        %s, %s
    )
"""

# def executeInsertSetsAlias(cursor , x):
# cursor.connection.commit()

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

# def executeInsertMinionTypes(cursor , x):
# cursor.connection.commit()

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

# def executeInsertGameModes(cursor , x):
# cursor.connection.commit()

insertMinionTypesLinkGameMode = """
    INSERT INTO minion_types_link_game_modes_HS(
        minion_type_id
    ,   game_mode_id
    ) VALUES(
        %s, %s
    )
"""

# def executeInsertMinionTypesLinkGameModes(cursor , x):
# cursor.connection.commit()

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

# def executeInsertKeywords(cursor , x):
# cursor.connection.commit()

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

# def executeInsertKeywordsLinkGameModes(cursor , x):
# cursor.connection.commit()

insertTypes = """
    INSERT INTO types_HS(
        type_id
    ,   type_name
    ,   slug
    ) VALUES(
        %s, %s, %s
    )
"""

# def executeInsertTypes(cursor , x):
# cursor.connection.commit()

insertTypesLinkGameModes = """
    INSERT INTO types_link_game_modes_HS(
        type_id
    ,   game_mode_id
    ) VALUES(
        %s, %s
    )
"""

# def executeInsertTypesLinkGameModes(cursor , x):
# cursor.connection.commit()

insertSpellSchool = """
    INSERT INTO spell_schools_HS(
        spell_school_id
    ,   spell_school_name
    ,   slug
    ) VALUES(
        %s, %s, %s
    )
"""

# def executeInsertSpellSchools(cursor , x):
# cursor.connection.commit()

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

# def executeInsertBGGameModes(cursor , x):
# cursor.connection.commit()

selectSetGroupId = """
    SELECT set_group_id
    FROM set_groups_HS
    WHERE set_group_name = (%s)
    """

###############################################################

def to_lower_kebab_case(str):
    str = str.replace(" ", "-").lower()
    return str


def get_data_from_bnet_api(url, **searchArguments):
    for key, value in searchArguments.items():
        url = url + "&%s=%s" % (key, value)
    print(url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

def getPageCount(cardSearchUrl, **searchArguments) -> int:
    try:
        pageCount = get_data_from_bnet_api(cardSearchUrl, **searchArguments).get('pageCount')
        return pageCount
    except AttributeError as e:
        print('Error:', e)
    return None

def cardHasValue(value) -> bool:
    return bool(value)

def addCardData(cursor, card):
    id = card.get('id')
    classId = card.get('classId')
    multiClassIds = card.get('multiClassIds')
    runeCost = card.get('runeCost')
    childIds = card.get('childIds')
    multiTypeIds = card.get('multiTypeIds')
    keywordIds = card.get('keywordIds')
    mercenaryHero = card.get('mercenaryHero')

    if not mercenaryHero:
        executeInsertCard(cursor, card)
        if cardHasValue(classId):
            executeInsertClassLink(cursor, id, classId)
        if cardHasValue(multiClassIds):
            for multiClassId in multiClassIds:
                    if multiClassId != classId:
                        executeInsertClassLink(cursor, id, multiClassId)
        if cardHasValue(runeCost):
            executeInsertRuneCosts(cursor, id, runeCost.get('blood'), runeCost.get('frost'), runeCost.get('unholy'))
        if cardHasValue(childIds):
            for childId in childIds:
                executeInsertCardRemap(cursor, id, childId)
        if cardHasValue(multiTypeIds):
            for typeId in multiTypeIds:
                executeInsertMinionTypesLink(cursor, id, typeId)
        if cardHasValue(keywordIds):
            for keywordId in keywordIds:
                try:
                    executeInsertKeywordsLink(cursor, id, keywordId)
                except Exception as e: # TODO create custom foreign key violation
                    #print(type(e).__name__)
                    # if card.get('id') in failedDict:
                    #     failedDict[id].insert(0, keywordId)
                    # else:
                    #     failedDict[id] = [keywordId, text]
                    cursor.connection.rollback()

def addBGCardData(cursor, card):
    if cardHasValue(card.get('battlegrounds')):
        try:
            executeInsertCard(cursor, card)
        except Exception as e:
            cursor.connection.rollback()
        executeInsertBGCards(cursor, card)

def iterateResponseAndAdd(cursor, response, dataToAdd):
    for item, in response:
        dataToAdd(cursor, item)

def iteratePages(cursor, pageCount, dataToAdd, cardSearchUrl, **searchArguments):
    for currPage in range(1, pageCount + 1):
        currPageCards = get_data_from_bnet_api(cardSearchUrl, page=currPage, **searchArguments).get('cards')
        iterateResponseAndAdd(cursor, currPageCards, dataToAdd)

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

def executeInsertGameMode(cursor, gameMode):
    cursor.execute(insertGameModes,(
        gameMode.get('id')
    ,   gameMode.get('name')
    ,   gameMode.get('slug')
    ))
    cursor.connection.commit()

def executeInsertBGGameMode(cursor, bgGameMode):
    cursor.execute(insertBGGameModes,(
        bgGameMode.get('id')
    ,   bgGameMode.get('name')
    ,   bgGameMode.get('slug')
    ))
    cursor.connection.commit()

def executeInsertType(cursor, type):
    cursor.execute(insertTypes,(
        type.get('id')
    ,   type.get('name')
    ,   type.get('slug')
    ))
    cursor.connection.commit()

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

def executeInsertMinionType(cursor, minionType):
    cursor.execute(insertMinionType,(
        minionType.get('id')
    ,   minionType.get('name')
    ,   minionType.get('slug')
    ))
    cursor.connection.commit()

def executeInsertSpellSchool(cursor, spellSchool):
    cursor.execute(insertSpellSchool,(
        spellSchool.get('id')
    ,   spellSchool.get('name')
    ,   spellSchool.get('slug')
    ))
    cursor.connection.commit()

def executeInsertKeyword(cursor, keyword):
    cursor.execute(insertKeyword,(
        keyword.get('id')
    ,   keyword.get('name')
    ,   keyword.get('text')
    ,   keyword.get('refText')
    ,   keyword.get('slug')
    ))
    cursor.connection.commit()

def executeInsertKeywordLinkGameModes(cursor, keyword, gameMode):
    cursor.execute(insertKeywordsLinkGameModes, (
        keyword.get('id')
    ,   gameMode
    ))
    cursor.connection.commit()

def executeInsertMinionTypeLinkGameMode(cursor, minionType, gameMode):
    cursor.execute(insertMinionTypesLinkGameMode, (
        minionType.get('id')
    ,   gameMode
    ))
    cursor.connection.commit()

def executeInsertSetsLinkSetGroups(cursor, set, setGroupId):
    cursor.execute(insertSetsLinkSetGroups,(
        set.get('id')
    ,   setGroupId
    ))
    cursor.connection.commit()

def executeInsertSetsAlias(cursor, set, alias):
    cursor.execute(insertSetsAlias, (
        set.get('id')
    ,   alias
    ))
    cursor.connection.commit()

def executeInsertTypesLinkGameModes(cursor, type, mode):
    cursor.execute(insertTypesLinkGameModes,(
        type.get('id')
    ,   mode
    ))

def iterateResponseAndAdd(cursor, response, dataToAdd):
    for item in response:
        dataToAdd(cursor, item)

def import_cards_data(cursor):
    pageCount = getPageCount(cardSearchUrl, collectible=collectible, pageSize=pageSize)
    if pageCount:
        iteratePages(cursor, pageCount, addCardData, cardSearchUrl, collectible=collectible, pageSize=pageSize)
    else:
        print('Failed to fetch card data from BNET API. Check api token')

def import_bg_cards_data(cursor):
    pageCount = getPageCount(cardSearchUrl, gameMode='battlegrounds', collectible=collectible, pageSize=pageSize,)
    if pageCount:
        iteratePages(cursor, pageCount, addBGCardData, cardSearchUrl, gameMode='battlegrounds', collectible=collectible, pageSize=pageSize)

def import_meta_data(cursor):
    response = get_data_from_bnet_api(metaDataSearchUrl)
    if response:
        setGroupsResponse = response.get('setGroups')
        setsResponse = response.get('sets')
        gameModesResponse = response.get('gameModes')
        bgGameModesResponse = response.get('bgGameModes')
        typesResponse = response.get('types')
        raritiesResponse = response.get('rarities')
        classesResponse = response.get('classes') #need to add dream class for ysera cards id=11
        minionTypesResponse = response.get('minionTypes')
        spellSchoolsResponse = response.get('spellSchools')
        keywordsResponse = response.get('keywords')

        iterateResponseAndAdd(cursor, setGroupsResponse, executeInsertSetGroups)
        iterateResponseAndAdd(cursor, gameModesResponse, executeInsertGameMode)
        iterateResponseAndAdd(cursor, bgGameModesResponse, executeInsertBGGameMode)
        iterateResponseAndAdd(cursor, raritiesResponse, executeInsertRarities)
        iterateResponseAndAdd(cursor, spellSchoolsResponse, executeInsertSpellSchool)


#ask alver about clean code here. how do people only ever have one level of indentation while maintaining functions with only a single meaningful purpose
        #iterateResponseAndAdd(cursor, setsResponse, executeInsertSet)
        for set in setsResponse:
            executeInsertSet(cursor, set)
            if set.get('aliasSetIds'):
                for alias in set.get('aliasSetIds'):
                    executeInsertSetsAlias(cursor, set, alias)

            for setGroup in setGroupsResponse:
                if to_lower_kebab_case(set.get('name')) in setGroup.get('cardSets'): #the name is in kebab case
                    cursor.execute(selectSetGroupId, (setGroup.get('name'),))
                    setGroupId = cursor.fetchone()[0]
                    executeInsertSetsLinkSetGroups(cursor, set, setGroupId)

        for type in typesResponse:
            executeInsertType(cursor, type)
            if type.get('gameModes'):
                for mode in type.get('gameModes'):
                    executeInsertTypesLinkGameModes(cursor, type, mode)

        for classes in classesResponse:
            executeInsertClass(cursor, classes)
            if classes.get('alternateHeroCardIds'):
                for altHeroId in classes.get('alternateHeroCardIds'): #can this just be part of the classes Link table? if heros are card then that should work. once i find how to fetch them all from api i will make this into a single link table
                    executeInsertAlternateHeros(cursor, classes, altHeroId)
        yseraClass ={'id': 11, 'slug': 'dream', 'name': 'Dream', 'cardId':None, 'heroPowerCardId':None} #hard coded class for the ysera generated cards
        executeInsertClass(cursor, yseraClass)

        for minionType in minionTypesResponse:
            executeInsertMinionType(cursor, minionType)
            if minionType.get('gameModes'):
                for gameMode in minionType.get('gameModes'):
                    executeInsertMinionTypeLinkGameMode(cursor, minionType, gameMode)

        for keyword in keywordsResponse:
            executeInsertKeyword(cursor, keyword)
            if keyword.get('gameModes'):
                for gameMode in keyword.get('gameModes'):
                    executeInsertKeywordLinkGameModes(cursor, keyword, gameMode)

###############################################################################################


def main():

    connect = psycopg2.connect(
        database="postgres",
        user="postgres",
        port="5432",
        host="localhost",
        password=PSQL_PASSWORD
        )
    cursor = connect.cursor()


    # Initialize the HS card Table
    initialize_sql_HS = open(r"C:\Users\xwill\OneDrive\Desktop\PythonProjects\tcgDataHouse\initialize_cardsHS.sql",'r')
    cursor.execute(initialize_sql_HS.read())


    # TODO Import meta data into supporting tables
    # TODO GET SET ALIAS
    # TODO add manual data for set/setgroups?
    import_meta_data(cursor)

    # Populate card_HS with data from card search bnet api
    # TODO GET RUNE COSTS
    # TODO GET CARD REMAPS
    # TODO FILL LINK TABLES
    import_cards_data(cursor)

    # Add battlegrounds exclusive cards to cards_HS with data from bg card search bnet api
    import_bg_cards_data(cursor)

    cursor.connection.commit()
    cursor.close()

if __name__ == '__main__':
    main()