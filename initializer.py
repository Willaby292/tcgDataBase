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

# Programatic authentication has not been set up. To get API token go to 'https://develop.battle.net/documentation/hearthstone/game-data-apis'.
# Use the TRY IT button on one of the example api requests and then copy and paste in the token at the end of the given url.
# If the TRY IT button take you to a page that says state parameter not provided simply add &state='' at the end of the url.
API_TOKEN = os.getenv('API_TOKEN')

###############################################################
insertCard = """
    INSERT INTO cards_HS (
        cardId
    ,   "name"
    ,   manaCost
    ,   attack
    ,   health
    ,   "durability"
    ,   "text"
    ,   armor
    ,   collectible
    ,   flavorText
    ,   "image"
    ,   imageGold
    ,   cropImage
    ,   artistName
    ,   slug
    ,   classId
    ,   cardTypeId
    ,   cardSetId
    ,   rarityId
    ,   minionTypeId
    ,   spellSchoolId
    ,   copyOfCardId
    ,   parentId
    ,   isZilliaxFunctionalModule
    ,   isZilliaxCosmeticModule
    ,   bannedFromSideboard
    ,   maxSideboardCards
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    );
"""

insertClasses = """
    INSERT INTO classes_HS(
        classId
    ,   heroCardId
    ,   className
    ,   heroPowerCardId
    ,   slug
    ) VALUES(
        %s, %s, %s, %s, %s
    )
"""

insertClassesLink = """
    INSERT INTO classes_link_HS(
        cardId
    ,   classId
    ) VALUES(
        %s, %s
    )
"""

insertAlternateHeros = """
    INSERT INTO alternate_heros_HS(
        classId
    ,   altHeroCardId
    ) VALUES(
        %s, %s
    )
"""

insertRarities = """
    INSERT INTO rarities_HS(
        rarityId
    ,   craftingCostNormal
    ,   craftingCostGolden
    ,   dustValueNormal
    ,   dustValueGolden
    ,   rarityName
    ,   slug
    ) VALUES(
        %s, %s, %s, %s, %s, %s, %s
    )
"""

insertBGCards = """
    INSERT INTO bg_cards_HS(
        cardId
    ,   tier
    ,   isHero
    ,   isQuest
    ,   isReward
    ,   isDuosOnly
    ,   isSolosOnly
    ,   upgradeId
    ,   "image"
    ,   imageGold
    ) VALUES(
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
"""

insertSetGroups = """
    INSERT INTO set_groups_HS(
        setGroupName
    ,   isStandard
    ,   svg
    ,   icon
    ,   year
    ,   yearRange
    ,   slug
    ) VALUES(
        %s, %s, %s, %s, %s, %s, %s
    )
"""

insertSets = """
    INSERT INTO sets_HS(
        setId
    ,   setName
    ,   isHyped
    ,   setType
    ,   collectibleCount
    ,   collectibleRevealedCount
    ,   nonCollectibleCount
    ,   nonCollectibleReavealedCount
    ,   slug
    ) VALUES(
        %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
"""

insertSetsLinkSetGroups = """
    INSERT INTO sets_link_set_groups_HS(
        setId
    ,   setGroupId
    ) VALUES(
        %s, %s
    )
"""


insertSetsAlias = """
    INSERT INTO sets_alias_HS(
        setId
    ,   aliasId
    ) VALUES(
        %s, %s
    )
"""

insertRuneCosts = """
    INSERT INTO rune_costs_HS(
        card_id
    ,   bloodRuneCount
    ,   frostRuneCount
    ,   unholyRuneCount
    ) VALUES(
        %s, %s, %s, %s
    )
"""

insertMinionTypes = """
    INSERT INTO minion_types_HS(
        minionTypeId
    ,   minionTypeName
    ,   slug
    ) VALUES(
        %s, %s, %s
    )
"""

insertMinionTypesLink = """
    INSERT INTO minion_types_link_HS(
        cardId
    ,   minionTypeId
    ) VALUES(
        %s, %s
    )
"""

insertGameModes = """
    INSERT INTO game_modes_HS(
        gameModeId
    ,   gameModeName
    ,   slug
    ) VALUES(
        %s, %s, %s,
    )
"""

insertMinionTypesLinkGameModes = """
    INSERT INTO minion_types_link_game_modes_HS(
        gameModeId
    ,   minionTypeId
    ) VALUES(
        %s, %s
    )
"""

insertKeywords = """
    INSERT INTO keywords_HS(
        keywordId
    ,   keywordName
    ,   keywordText
    ,   refText
    ,   slug
    ) VALUES(
        %s, %s, %s, %s, %s
    )
"""

insertKeywordsLink = """
    INSERT INTO keywords_link_cards_HS(
        cardsId
    ,   keywordId
    ) VALUES(
        %s, %s
    )
"""

insertKeywordsLinkGameModes = """
    INSERT INTO keywords_link_game_modes_HS(
        gameModeId
    ,   keywordId
    ) VALUES(
        %s, %s
    )
"""

insertTypes = """
    INSERT INTO types_HS(
        typeId
    ,   typeName
    ,   slug
    ) VALUES(
        %s, %s, %s
    )
"""

insertTypesLinkGameModes = """
    INSERT INTO types_link_game_modes_HS(
        gameModeId
    ,   typeId
    ) VALUES(
        %s, %s
    )
"""

insertSpellSchools = """
    INSERT INTO spell_schools_HS(
        spellSchoolId
    ,   spellSchoolName
    ,   slug
    ) VALUES(
        %s, %s, %s
    )
"""

insertCardRemap = """
    INSERT INTO bg_game_modes(
        parentId
    ,   childId
    ) VALUES(
        %s, %s
    )
"""

insertBGGameModes = """
    INSERT INTO bg_game_modes(
        bgGameModeId
    ,   bgGameModeName
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

def import_cards_data(cursor):
    pageSize = 200
    cardSearchUrl = 'https://us.api.blizzard.com/hearthstone/cards?locale=en_US&access_token='
    pageCount = get_data_from_bnet_api(cardSearchUrl, collectible='0,1', pageSize=pageSize)
    if pageCount:
        pageCount = pageCount.get('pageCount')
        for currPage in range(1, pageCount + 1):
            currPageResponse = get_data_from_bnet_api(cardSearchUrl, collectible='0,1',page=currPage, pageSize=pageSize)
            for card in currPageResponse.get('cards'):
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
    else:
        print('Failed to fetch card data from BNET API. Check api token')

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


def import_meta_data(cursor):
    metaDataSearchUrl = 'https://us.api.blizzard.com/hearthstone/metadata?locale=en_US&access_token='
    if get_data_from_bnet_api(metaDataSearchUrl):
        response = get_data_from_bnet_api(metaDataSearchUrl)
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
            for setGroup in setGroupsResponse:
                if to_lower_kebab_case(set.get('name')) in setGroup.get('cardSets'): #the name is in kebab case
                    cursor.execute("""SELECT setGroupId FROM set_groups_HS WHERE setGroupName = (%s)""", (setGroup.get('name'),))
                    setGroupId = cursor.fetchone()[0]
                    cursor.execute(insertSetsLinkSetGroups,(
                        set.get('id')
                    ,   setGroupId
                    ))

        # gameModesResponse = response.get('gameModes')
        # for gameMode in gameModesResponse:
        #     cursor.execute(insertGameModes,(

        #     ))
        # bgGameModesResponse = response.get('bgGameModes')
        # for bgGameMode in bgGameModesResponse:
        #     cursor.execute(insertBGGameModes,(

        #     ))
        # typesResponse = response.get('types')
        # for type in typesResponse:
        #     cursor.execute(insertTypes,(

        #     ))
        raritiesResponse = response.get('rarities')
        for rarity in raritiesResponse:
            try:
                craftingCostNormal = min(rarity.get('crafingCost'))
                craftingCostGold = max(rarity.get('crafingCost'))
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
        # minionTypesResponse = response.get('minionTypes')
        # for minionType in minionTypesResponse:
        #     cursor.execute(insertMinionTypes,(

        #     ))
        # spellSchoolsResponse = response.get('spellSchools')
        # for spellSchool in spellSchoolsResponse:
        #     cursor.execute(insertSpellSchools,(

        #     ))
        # keywordsResponse = response.get('keywords')
        # for keyword in keywordsResponse:
        #     cursor.execute(insertKeywords,(

        #     ))




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