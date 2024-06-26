import psycopg2
import json
import requests # for handling api calls
import subprocess
import time
from collections import defaultdict

API_TOKEN = 'USndlfuh25NGZOZJmlXdmMaAt6Ctj5JT79'

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
insertClasses = """
    INSERT INTO classes_HS (
        class_id
,       class_name

    ) VALUES (
        %s, %s
    );
"""
insertClassesLink = """
    INSERT INTO classes_link_HS (
        card_id
,       class_id

    ) VALUES (
        %s, %s
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
insertKeyword = """
    INSERT INTO keywords_HS (
        keyword_id
,       keyword_name

    ) VALUES (
        %s, %s
    );
"""
insertKeywordLink = """
    INSERT INTO keywords_link_HS (
        card_id
,       keyword_id

    ) VALUES (
        %s, %s
    );
"""

def get_posts_cards(**kwargs):
    # this string needs to be created by adding all the criteria needed plus the token that is generated in OAuthToken.js    
    url = 'https://us.api.blizzard.com/hearthstone/cards?locale=en_US&access_token='+ API_TOKEN
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

def get_posts_meta_data(**kwargs):
    url = 'https://us.api.blizzard.com/hearthstone/metadata?locale=en_US&access_token=' + API_TOKEN
    for key, value in kwargs.items():
        url = url + "&%s=%s" % (key, value)
    print(url)
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

def intitalize_cards(cursor, currPage):
    curPageCardsList = currPage.get('cards') # get post returns 4 dictionaries: cards, cardCount, pageCount, and page
    for card in curPageCardsList:
        cursor.execute(insertCard, ( #inserst all card information into card table
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
        
        # #inserts class info into classes link tables
        # multiClassIds = card.get('multiClassIds')
        # if multiClassIds:
        #     for classId in multiClassIds:
        #         cursor.execute(insertClassesLink,(
        #             card.get('id')
        #         ,   classId
        #         ))
        
        # #inserts keyword info into keywords_link tables
        # keywordIds = card.get('keywordIds') 
        # if keywordIds:
        #     for keywordId in keywordIds:
        #         cursor.execute(insertKeywordLink,(
        #             card.get('id')
        #         ,   keywordId
        #         ))




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
    initialize_sql_HS = open(r"C:\Users\xwill\OneDrive\Desktop\projects\Scryfall2.0\initialize_cardsHS.sql",'r')
    cursor.execute(initialize_sql_HS.read())

    pageCount = get_posts_cards(collectible='0,1').get('pageCount')
    if pageCount:
        for page in range(1, pageCount + 1): #loop over this for each page
            currPage = get_posts_cards(colletible='0,1',page=str(page))
            intitalize_cards(cursor, currPage)
    else:
        print('Failed to fetch from API')
    print('all cards initialized')


    # meta_data = get_posts_meta_data()
    # classes = meta_data.get('classes')
    # for eachClass in classes:
    #     cursor.execute(insertClasses,
    #        eachClass.get()
    #     ,  eachClass.get()
    #     ,  eachClass.get()
    #     ,  eachClass.get()
    #     ,  eachClass.get()
    #     )
    # allMetaKeys = []
    # for key in meta_data:
    #     allMetaKeys.append(key)
    # print(allMetaKeys)
    #intitalize_cards(cursor)
    
    cursor.connection.commit()
    cursor.close()

if __name__ == '__main__':
    main()