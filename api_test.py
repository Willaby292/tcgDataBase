import psycopg2
import json
import requests # for handling api calls
import subprocess
import time
from collections import defaultdict

API_TOKEN = 'USndlfuh25NGZOZJmlXdmMaAt6Ctj5JT79'

def get_posts_cards(**kwargs): #set collectable=0,1 to see all cards
    # this string needs to be created by adding all the criteria needed plus the token that is generated in OAuthToken.js    
    url = 'https://us.api.blizzard.com/hearthstone/cards?locale=en_US&access_token='+API_TOKEN
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
    url = 'https://us.api.blizzard.com/hearthstone/metadata?locale=en_US&access_token='+API_TOKEN
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
    

def get_posts_generic(url):
    url += API_TOKEN
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


def check_meta_data():  
    response = get_posts_meta_data()
    del response['arenaIds']
    del response['filterableFields']
    del response['numericFields']

    for category in response:
        print(category)
        uniqueKeys = {}
        for data in response.get(category):
            for key in data:
                if key not in uniqueKeys:
                    uniqueKeys[key] = str(type(data.get(key)))[8:-2]
                # if key == 'aliasSetIds':
                #     oddData.append(data.get('name'))
        print(len(uniqueKeys))
        for enu, i in enumerate(uniqueKeys, 1):
            print(str(enu) + ': '+str(i) + ' -- ' + str(uniqueKeys.get(i)))
        # print(oddData)



def check_bg_card_search_data():
    BGResponse = get_posts_generic('https://us.api.blizzard.com/hearthstone/cards?locale=en_US&gameMode=battlegrounds&tier=hero%2C3&access_token=')
    uniqueKeys = {}
    uniqueKeysMain = {}
    for entry in BGResponse:
        for card in BGResponse.get('cards'):   
            for keyMain in card:
                if keyMain not in uniqueKeysMain:
                     uniqueKeysMain[keyMain] = str(type(card.get(keyMain)))[8:-2]
            for key in card.get('battlegrounds'):
                if key not in uniqueKeys:
                    uniqueKeys[key] = str(type(card.get('battlegrounds').get(key)))[8:-2]
    print('unique bg keys: ' +str(len(uniqueKeys)))
    for enu, i in enumerate(uniqueKeys, 1):
        print(str(enu) + ': '+str(i) + ' -- ' + str(uniqueKeys.get(i)))
    print('unique card keys: ' +str(len(uniqueKeysMain)))
    for enu, i in enumerate(uniqueKeysMain, 1):
        print(str(enu) + ': '+str(i) + ' -- ' + str(uniqueKeysMain.get(i)))



def check_card_search_data():
    pageCount = get_posts_cards(collectible='0,1').get('pageCount')
    uniqueKeysCards = {}
    altHeros = [2827, 46116, 53187, 57757, 61596, 61886, 64732, 67519] #the last 5 of these values are missing from the cards response from the api. these were random and implys that we are missing a lot more
    altHeroNames = []                                                   # it seems like the ones that are missing are differnt arts for uther
    for currPage in range(1, pageCount):
        CardResponse = get_posts_cards(collectible='0,1',page=currPage)
        for card in CardResponse.get('cards'):
            for key in card:
                if key not in uniqueKeysCards:
                    uniqueKeysCards[key] = str(type(card.get(key)))[8:-2]
    print('number of keys: '+ str(len(uniqueKeysCards)))
    for enu, i in enumerate(uniqueKeysCards, 1):
        print(str(enu) + ': '+str(i) + ' -- ' + str(uniqueKeysCards.get(i)))

    

 

def main():

    #make sure I have been doing all the pages of each of these responses

    #check_meta_data()
    #check_bg_card_search_data()
    #CardResponse = get_posts_cards(collectible='0,1')
    #check_card_search_data()
    print('done')

if __name__ == '__main__':
    main()