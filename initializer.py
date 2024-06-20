import psycopg2
import json
import requests # for handling api calls
import subprocess
import time
from collections import defaultdict
from mtgsdk import Card 
from mtgsdk import Set


insertCard = """
    INSERT INTO cards_HS (
        id
    ,   collectible
    ,   slug
    ,   classId
    ,   spellSchoolId
    ,   cardTypeId
    ,   cardSetId
    ,   rarityId
    ,   artistName
    ,   manaCost
    ,   name
    ,   text
    ,   image
    ,   imageGold
    ,   flavorText
    ,   cropImage
    ,   isZilliaxFunctionalModule
    ,   isZilliaxCosmeticModule
    ,   copyOfCardId
    ,   health
    ,   attack
    ,   minionTypeId
    ,   armor
    ,   durability
    ,   parentId
    ,   bannedFromSideboard
    ,   maxSideboardCards
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    );
"""

insertRace = """
    INSERT INTO races_HS (
        race_id
,       race_name

    ) VALUES (
        %s, %s
    );
"""
insertRaceLink = """
    INSERT INTO races_link_HS (
        card_id
,       race_id

    ) VALUES (
        %s, %s
    );
"""
insertMechanic = """
    INSERT INTO mechanics_HS (
        mechanic_id
,       mechanic_name

    ) VALUES (
        %s, %s
    );
"""
insertMechanicLink = """
    INSERT INTO mechanics_link_HS (
        card_id
,       mechanic_id

    ) VALUES (
        %s, %s
    );
"""

def get_posts(**kwargs):
    # this string needs to be created by adding all the criteria needed plus the token that is generated in OAuthToken.js
    
    url = 'https://us.api.blizzard.com/hearthstone/cards?locale=en_US&access_token=USySTrAtR6Ads4rR9qRY4FTF7TGsEQJs4z'
    for key, value in kwargs.items():
        url = url + "&%s=%s" % (key, value)
        print(url)
    #send request with request url and request method with the payload
    try:
        response = requests.get(url)

        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None


def main():

    connect = psycopg2.connect(
        database="postgres",
        user="postgres",
        port="5432",
        host="localhost",
        password="walvarez00"
        )
    cursor = connect.cursor()

    # Initialize the HS card Table
    initialize_sql_HS = open(r"C:\Users\xwill\OneDrive\Desktop\Scryfall2.0\initialize_cardsHS.sql",'r')
    cursor.execute(initialize_sql_HS.read())

    # this is commented out until i can close the server when I finish

    pageCount = get_posts().get('pageCount')
    allKeys = {}
    for page in range(1, pageCount + 1): #loop over this for each page
        cards = get_posts(page = str(page))
        curPageCardsList = cards.get('cards') # get post returns 4 dictionaries: cards, cardCount, pageCount, and page
        if cards:
            for card in curPageCardsList:
                # keyList = list(card.keys())
                # for key in keyList:
                #     if key not in allKeys:
                #         allKeys[key] = type(card.get(key))
                cursor.execute(insertCard, (
                    card.get('id')
                ,   card.get('collectible')
                ,   card.get('slug')
                ,   card.get('classId')
                #,   card.get('multiClassIds') -> needs own table
                ,   card.get('spellSchoolId')
                ,   card.get('cardTypeId')
                ,   card.get('cardSetId')
                ,   card.get('rarityId')
                ,   card.get('artistName')
                ,   card.get('manaCost')
                ,   card.get('name')
                ,   card.get('text')
                ,   card.get('image')
                ,   card.get('imageGold')
                ,   card.get('flavorText')
                ,   card.get('cropImage')
                #,   card.get('keywordIds') -> needs own table
                ,   card.get('isZilliaxFunctionalModule')
                ,   card.get('isZilliaxCosmeticModule')
                ,   card.get('copyOfCardId')   
                ,   card.get('health')
                ,   card.get('attack')
                ,   card.get('minionTypeId')
                #,   card.get('childIds') -> needs own table
                ,   card.get('armor')
                #,   card.get('multiTypeIds') -> needs own table
                ,   card.get('durability')
                #,   card.get('runeCost') dictionary -> needs own table
                ,   card.get('parentId')
                ,   card.get('bannedFromSideboard')
                ,   card.get('maxSideboardCards')
                ))
        else:
            print('failed to fetch posts from api')
    # print(allKeys)
    cursor.connection.commit()
    cursor.close()

if __name__ == '__main__':
    main()