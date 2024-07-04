import psycopg2
import requests # for handling api calls
import os
from dbFunctions import *
from dotenv import load_dotenv

# TODO create versioning of the data so that each time its updated I can check to see changes
# TODO type cast variables when instanced
# TODO find hidden data like hero card data
# TODO change instances of classes to singleClass or some other name


# Programatic authentication has not been set up. To get API token go to 'https://develop.battle.net/documentation/hearthstone/game-data-apis'.
# Use the TRY IT button on one of the example api requests and then copy and paste in the token at the end of the given url.
# If the TRY IT button take you to a page that says state parameter not provided simply add &state='' at the end of the url.

load_dotenv()
PSQL_PASSWORD = os.getenv('PSQL_PASSWORD')
API_TOKEN = os.getenv('API_TOKEN')

pageSize  = 500
cardSearchUrl = 'https://us.api.blizzard.com/hearthstone/cards?locale=en_US&access_token='+API_TOKEN
metaDataSearchUrl = 'https://us.api.blizzard.com/hearthstone/metadata?locale=en_US&access_token='+API_TOKEN
singleCardSearchUrl = 'https://us.api.blizzard.com/hearthstone/cards/78066?locale=en_US&access_token='+API_TOKEN
collectible = '0,1'

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

def to_lower_kebab_case(str: str):
    str = str.replace(" ", "-").lower()
    return str

def cardHasValue(value) -> bool:
    return bool(value)

def iterateResponseAndAdd(cursor, response, dataToAdd):
    for item in response:
        dataToAdd(cursor, item)

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
        try:
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
        except Exception as e:
            print('card: ' + card.get('name') + ' already exists')
            cursor.connection.rollback()

def addBGCardData(cursor, card):
    if cardHasValue(card.get('battlegrounds')):
        try:
            executeInsertCard(cursor, card)
        except Exception as e:
            cursor.connection.rollback()
        executeInsertBGCards(cursor, card)

def iteratePages(cursor, pageCount, dataToAdd, cardSearchUrl, **searchArguments):
    for currPage in range(1, pageCount + 1):
        currPageCards = get_data_from_bnet_api(cardSearchUrl, page=currPage, **searchArguments).get('cards')
        iterateResponseAndAdd(cursor, currPageCards, dataToAdd)

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
                for altHeroId in classes.get('alternateHeroCardIds'):
                    singleCardSearchUrl = 'https://us.api.blizzard.com/hearthstone/cards/'+str(altHeroId)+'?locale=en_US&access_token='+API_TOKEN
                    card = get_data_from_bnet_api(singleCardSearchUrl)
                    addCardData(cursor, card)
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

def main():
    connect = psycopg2.connect(
        database="postgres",
        user="postgres",
        port="5432",
        host="localhost",
        password=PSQL_PASSWORD
        )
    cursor = connect.cursor()

    # Initialize the HS tables
    initialize_sql_HS = open(r"C:\Users\xwill\OneDrive\Desktop\PythonProjects\tcgDataHouse\initialize_cardsHS.sql",'r')
    cursor.execute(initialize_sql_HS.read())

    import_meta_data(cursor)

    # Populate card_HS with data from card search bnet api
    import_cards_data(cursor)

    # Add battlegrounds exclusive data to cards_HS with data from bg card search bnet api
    import_bg_cards_data(cursor)

    cursor.connection.commit()
    cursor.close()

if __name__ == '__main__':
    main()