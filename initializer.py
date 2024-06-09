import psycopg2
import json
from collections import defaultdict
from mtgsdk import Card 
from mtgsdk import Set 

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


# Opening JSON file
f = open(r"C:\Users\xwill\OneDrive\Desktop\cards_enUS_TEST.json", encoding='utf-8')
# returns JSON object as 
# a dictionary
data = json.load(f)

insertCard = """
    INSERT INTO cards_HS (
        card_id
,       id
,       "name"
,       "type"
,       card_class
,       player_class
,       collectible
,       "set"
,       rarity
,       cost
,       faction
,       race
,       attack
,       health
,       durability
,       mercenary
,       mercenary_role
,       text
,       flavor
,       artist
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    );
"""
insertRaces = """
    INSERT INTO races_HS (
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

# Iterating through the json
# list

mechanicIdNum = 0
for i in data:

    cursor.execute(insertCard, (
        i.get('dbfId')
    ,   i.get('id')
    ,   i.get('name')
    ,   i.get('type')
    ,   i.get('cardClass')
    ,   i.get('playerClass')
    ,   i.get('collectible')
    ,   i.get('set')
    ,   i.get('rarity')
    ,   i.get('cost')
    ,   i.get('faction')
    ,   i.get('race') # race is redundant, races has all minion race information. keep this until we make sure of that
    ,   i.get('attack')
    ,   i.get('health')
    ,   i.get('durability')
    ,   i.get('mercenary')
    ,   i.get('mercenaryRole')
    ,   i.get('text')
    ,   i.get('flavor')
    ,   i.get('artist')
        ))
    

    # fill races table
    racesArr = i.get('races')
    if racesArr is not None:
        for race in racesArr:
            cursor.execute(insertRaces, (
                i.get('dbfId')
            ,   race
            ))

    # fill mechanics table
    mechanicIdNum += 1
    mechanicArr = i.get('mechanics')
    if mechanicArr is not None:
        for mechanic in mechanicArr:
            if mechanic not in mechanicArr:
                cursor.execute(insertMechanic, (
                    'm' + str(mechanicIdNum)
                ,   mechanic
                ))




# Closing file
f.close()



cursor.connection.commit()


# Initialize the tables in the database for MTG
# initialize_sql = open(r"C:\Users\xwill\OneDrive\Desktop\Scryfall2.0\initialize_cards.sql",'r')
# cursor.execute(initialize_sql.read())


# insert card information into mtg cards table
# def insert_cards():
#     print("Inserting Cards into cards table...")
#     cardList = Card.all()  
#     insertCard = """
#     INSERT INTO cards (name, multiverse_id, layout, names, mana_cost, cmc, colors, color_identity, type, supertypes, subtypes, rarity, text, flavor, artist, number, power, toughness, loyalty, variations, watermark, border, timeshifted, hand, life, release_date, starter, rulings, foreign_names, printings, original_text, original_type, legalities, source, image_url, set, set_name, id) 
#     VALUES ($${0}$$, $${1}$$, $${2}$$, $${3}$$, $${4}$$, $${5}$$, $${6}$$, $${7}$$, $${8}$$, $${9}$$, $${10}$$, $${11}$$, $${12}$$, $${13}$$, $${14}$$, $${15}$$, $${16}$$, $${17}$$, $${18}$$, $${19}$$, $${20}$$, $${21}$$, $${22}$$, $${23}$$, $${24}$$, $${25}$$, $${26}$$, $${27}$$, $${28}$$, $${29}$$, $${30}$$, $${31}$$, $${32}$$, $${33}$$, $${34}$$, $${35}$$, $${36}$$, $${37}$$);"
#     """
#     for x in cardList:
#         cursor.execute(insertCard.format(x.name, x.multiverse_id, x.layout, x.names, str(x.mana_cost),  x.cmc, x.colors, x.color_identity, x.type, x.supertypes, x.subtypes, x.rarity, x.text, x.flavor, x.artist, x.number, x.power, x.toughness, x.loyalty, x.variations, x.watermark, x.border, x.timeshifted, x.hand, x.life, x.release_date, x.starter, x.rulings, x.foreign_names, x.printings, x.original_text, x.original_type, x.legalities, x.source, x.image_url, x.set, x.set_name, x.id))
    
#     cursor.connection.commit()

# insert set info into mtg sets table
# def insert_sets():
#     print("Inserting Sets into sets table...")
#     setList = sets = Set.all()
#     insertSets = "INSERT INTO sets (code, name, gatherer_code, old_code, magic_cards_info_code, release_date, border, type, block, online_only, booster, mkm_id, mkm_name) VALUES ($${0}$$, $${1}$$, $${2}$$, $${3}$$, $${4}$$, $${5}$$, $${6}$$, $${7}$$, $${8}$$, $${9}$$, $${10}$$, $${11}$$, $${12}$$);"
#     for x in setList:
#         cursor.execute(insertSets.format(x.code, x.name, x.gatherer_code, x.old_code, x.magic_cards_info_code,  x.release_date, x.border, x.type, x.block, x.online_only, x.booster, x.mkm_id, x.mkm_name))
    
#     cursor.connection.commit()

# insert_cards()
# insert_sets()

cursor.close()