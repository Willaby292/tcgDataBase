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


# Programatic authentication has not been set up. To get API token go to 'https://develop.battle.net/documentation/hearthstone/game-data-apis'.
# Use the TRY IT button on one of the example api requests and then copy and paste in the token at the end of the given url.
# If the TRY IT button take you to a page that says state parameter not provided simply add &state='' at the end of the url.
API_TOKEN = os.getenv('API_TOKEN')

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

insertBGData = """
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
    pageSize = 500
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
                cursor.execute(insertBGData, (
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

    # Populate card_HS with data from card search bnet api
    import_cards_data(cursor)

    # Add battlegrounds exclusive cards to cards_HS with data from bg card search bnet api
    import_bg_cards_data(cursor)

    # TODO Import meta data into supporting tables
    # import_meta_data(cursor)

    cursor.connection.commit()
    cursor.close()

if __name__ == '__main__':
    main()