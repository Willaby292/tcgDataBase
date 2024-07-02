import psycopg2
import json
import requests # for handling api calls
import subprocess
import time
import os
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()
PSQL_PASSWORD = os.getenv('PSQL_PASSWORD')


# TODO change camel case to snake case in SQL
# TODO type cast variables when instanced
# TODO find hidden data like hero card data
# TODO insert or update

# TODO can i add catch blocks to catch foriegn key missing and then add it to the main value
# The plan for this is to catch execptions on the inserts and put them in a data structure to be handled at the end of the init

# Programatic authentication has not been set up. To get API token go to 'https://develop.battle.net/documentation/hearthstone/game-data-apis'.
# Use the TRY IT button on one of the example api requests and then copy and paste in the token at the end of the given url.
# If the TRY IT button take you to a page that says state parameter not provided simply add &state='' at the end of the url.
API_TOKEN = os.getenv('API_TOKEN')

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

insertClassesLink = """
    INSERT INTO classes_link_HS(
        card_id
    ,   class_id
    ) VALUES(
        %s, %s
    )
"""

insertAlternateHeros = """
    INSERT INTO alternate_heros_HS(
        class_id
    ,   alt_hero_card_id
    ) VALUES(
        %s, %s
    )
"""

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

insertSetsLinkSetGroups = """
    INSERT INTO sets_link_set_groups_HS(
        set_id
    ,   set_group_id
    ) VALUES(
        %s, %s
    )
"""


insertSetsAlias = """
    INSERT INTO set_alias_HS(
        set_id
    ,   alias_id
    ) VALUES(
        %s, %s
    )
"""

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

insertMinionTypes = """
    INSERT INTO minion_types_HS(
        minion_type_id
    ,   minion_type_name
    ,   slug
    ) VALUES(
        %s, %s, %s
    )
"""

insertMinionTypesLink = """
    INSERT INTO minion_types_link_HS(
        card_id
    ,   minion_type_id
    ) VALUES(
        %s, %s
    )
"""

insertGameModes = """
    INSERT INTO game_modes_HS(
        game_mode_id
    ,   game_mode_name
    ,   slug
    ) VALUES(
        %s, %s, %s
    )
"""

insertMinionTypesLinkGameModes = """
    INSERT INTO minion_types_link_game_modes_HS(
        minion_type_id
    ,   game_mode_id
    ) VALUES(
        %s, %s
    )
"""

insertKeywords = """
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

insertKeywordsLink = """
    INSERT INTO keywords_link_HS(
        card_id
    ,   keyword_id
    ) VALUES(
        %s, %s
    )
"""

insertKeywordsLinkGameModes = """
    INSERT INTO keywords_link_game_modes_HS(
        keyword_id
    ,   game_mode_id
    ) VALUES(
        %s, %s
    )
"""

insertTypes = """
    INSERT INTO types_HS(
        type_id
    ,   type_name
    ,   slug
    ) VALUES(
        %s, %s, %s
    )
"""

insertTypesLinkGameModes = """
    INSERT INTO types_link_game_modes_HS(
        type_id
    ,   game_mode_id
    ) VALUES(
        %s, %s
    )
"""

insertSpellSchools = """
    INSERT INTO spell_schools_HS(
        spell_school_id
    ,   spell_school_name
    ,   slug
    ) VALUES(
        %s, %s, %s
    )
"""

insertCardRemap = """
    INSERT INTO card_remap_HS(
        parent_id
    ,   child_id
    ) VALUES(
        %s, %s
    )
"""

insertBGGameModes = """
    INSERT INTO bg_game_modes_HS(
        bg_game_mode_id
    ,   bg_game_mode_name
    ,   slug
    ) VALUES(
        %s, %s, %s
    )
"""
###############################################################

def to_lower_kebab_case(str):
    str = str.replace(" ", "-").lower()
    return str


def get_data_from_bnet_api(url, **kwargs):
    # this string needs to be created by adding all the criteria needed plus the token that is generated in OAuthToken.js
    url = url + API_TOKEN
    for key, value in kwargs.items():
        url = url + "&%s=%s" % (key, value)
    print(url)
    #send request with request url and request method with the payload
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


def import_cards_data(cursor):
    pageSize = 500
    cardSearchUrl = 'https://us.api.blizzard.com/hearthstone/cards?locale=en_US&access_token='
    pageCount = get_data_from_bnet_api(cardSearchUrl, collectible='0,1', pageSize=pageSize)
    failedDict = {}
    if pageCount:
        pageCount = pageCount.get('pageCount')
        for currPage in range(1, pageCount + 1):
            currPageResponse = get_data_from_bnet_api(cardSearchUrl, collectible='0,1',page=currPage, pageSize=pageSize)
            for card in currPageResponse.get('cards'):
                if card.get('mercenaryHero'):
                    break
                executeInsertCard(cursor, card)
                if(card.get('classId')):
                    cursor.execute(insertClassesLink, (## have to have classes and cards initialized first. the entire card import should probably just be run second
                        card.get('id')
                    ,   card.get('classId')
                    ))
                if card.get('multiClassIds'):
                    for classes in card.get('multiClassIds'):
                        if classes != card.get('classId'):
                            cursor.execute(insertClassesLink, (
                                card.get('id')
                            ,   classes
                            ))
                if card.get('runeCost'):
                    cursor.execute(insertRuneCosts,(
                            card.get('id')
                        ,   card.get('runeCost').get('blood')
                        ,   card.get('runeCost').get('frost')
                        ,   card.get('runeCost').get('unholy')
                    ))
                if card.get('childIds'):
                    for childId in card.get('childIds'):
                        cursor.execute(insertCardRemap, (
                            card.get('id')
                        ,   childId
                        ))
                if card.get('multiTypeIds'):
                    for typeId in card.get('multiTypeIds'):
                        cursor.execute(insertMinionTypesLink, (
                            card.get('id')
                        ,   typeId
                        ))
                if card.get('keywordIds'):
                    for keyword in card.get('keywordIds'):
                        try:
                            cursor.execute(insertKeywordsLink, (
                                card.get('id')
                            ,   keyword
                            ))
                        except Exception as e:
                            failedDict[card.get('id')] = f"{keyword:4} : {card.get('text')}"
                            cursor.connection.rollback()

    else:
        print('Failed to fetch card data from BNET API. Check api token')
    for i in failedDict:
        print(f"{i:6} : {failedDict.get(i)}")


# these cards are already in the get all cards function above but this gets their battlegrounds information
def import_bg_cards_data(cursor):
    pageSize = 500
    cardSearchUrl = 'https://us.api.blizzard.com/hearthstone/cards?locale=en_US&gameMode=battlegrounds&access_token='
    pageCount = get_data_from_bnet_api(cardSearchUrl, pageSize=pageSize)

    if pageCount:
        pageCount = pageCount.get('pageCount')
        for currPage in range(1, pageCount + 1):
            currPageResponse = get_data_from_bnet_api(cardSearchUrl,page=currPage, pageSize=pageSize)
            for card in currPageResponse.get('cards'):
                try:
                    executeInsertCard(cursor, card)
                except Exception as e:
                    cursor.connection.rollback()

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


def import_meta_data(cursor):
    metaDataSearchUrl = 'https://us.api.blizzard.com/hearthstone/metadata?locale=en_US&access_token='
    response = get_data_from_bnet_api(metaDataSearchUrl)
    if response:
        setGroupsResponse = response.get('setGroups')
        setsResponse = response.get('sets')
        for setGroup in setGroupsResponse:
            cursor.execute(insertSetGroups,(
                setGroup.get('name')
            ,   setGroup.get('standard')
            ,   setGroup.get('svg')
            ,   setGroup.get('icon')
            ,   setGroup.get('year')
            ,   setGroup.get('yearRange')
            ,   setGroup.get('slug')
            ))
        for set in setsResponse:
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
            if set.get('aliasSetIds'):
                for alias in set.get('aliasSetIds'):
                    cursor.execute(insertSetsAlias, (
                        set.get('id')
                    ,   alias
                    ))
            for setGroup in setGroupsResponse:
                if to_lower_kebab_case(set.get('name')) in setGroup.get('cardSets'): #the name is in kebab case
                    cursor.execute("""SELECT set_group_id FROM set_groups_HS WHERE set_group_name = (%s)""", (setGroup.get('name'),))
                    setGroupId = cursor.fetchone()[0]
                    cursor.execute(insertSetsLinkSetGroups,(
                        set.get('id')
                    ,   setGroupId
                    ))
        gameModesResponse = response.get('gameModes')
        for gameMode in gameModesResponse:
            cursor.execute(insertGameModes,(
                gameMode.get('id')
            ,   gameMode.get('name')
            ,   gameMode.get('slug')
            ))
        bgGameModesResponse = response.get('bgGameModes')
        for bgGameMode in bgGameModesResponse:
            cursor.execute(insertBGGameModes,(
                bgGameMode.get('id')
            ,   bgGameMode.get('name')
            ,   bgGameMode.get('slug')
            ))
        typesResponse = response.get('types')
        for type in typesResponse:
            cursor.execute(insertTypes,(
                type.get('id')
            ,   type.get('name')
            ,   type.get('slug')
            ))
            if type.get('gameModes'):
                for mode in type.get('gameModes'):
                    cursor.execute(insertTypesLinkGameModes,(
                        type.get('id')
                    ,   mode
                    ))
        raritiesResponse = response.get('rarities')
        for rarity in raritiesResponse:
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
        classesResponse = response.get('classes') #need to add dream class for ysera cards id=11
        for classes in classesResponse:
            cursor.execute(insertClasses,(
                classes.get('id')
            ,   classes.get('cardId')
            ,   classes.get('name')
            ,   classes.get('heroPowerCardId')
            ,   classes.get('slug')
            ))
            if classes.get('alternateHeroCardIds'):
                for altHeroId in classes.get('alternateHeroCardIds'): #can this just be part of the classes Link table? if heros are card then that should work. once i find how to fetch them all from api i will make this into a single link table
                    cursor.execute(insertAlternateHeros,( #just change insertAlternateHeros to insertClassesLink
                        classes.get('id')
                    ,   altHeroId
                    ))
        cursor.execute(insertClasses,(
                11
            ,   None
            ,   'Dream'
            ,   None
            ,   'dream'
        ))
        minionTypesResponse = response.get('minionTypes')
        for minionType in minionTypesResponse:
            cursor.execute(insertMinionTypes,(
                minionType.get('id')
            ,   minionType.get('name')
            ,   minionType.get('slug')
            ))
            if minionType.get('gameModes'):
                for gameMode in minionType.get('gameModes'):
                    cursor.execute(insertMinionTypesLinkGameModes, (
                        minionType.get('id')
                    ,   gameMode
                    ))
        spellSchoolsResponse = response.get('spellSchools')
        for spellSchool in spellSchoolsResponse:
            cursor.execute(insertSpellSchools,(
                spellSchool.get('id')
            ,   spellSchool.get('name')
            ,   spellSchool.get('slug')
            ))
        keywordsResponse = response.get('keywords')
        for keyword in keywordsResponse:
            cursor.execute(insertKeywords,(
                keyword.get('id')
            ,   keyword.get('name')
            ,   keyword.get('text')
            ,   keyword.get('refText')
            ,   keyword.get('slug')
            ))
            if keyword.get('gameModes'):
                for gameMode in keyword.get('gameModes'):
                    cursor.execute(insertKeywordsLinkGameModes, (
                        keyword.get('id')
                    ,   gameMode
                    ))



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