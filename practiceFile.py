import psycopg2
from mtgsdk import Card 

connect = psycopg2.connect(
    database="postgres",
    user="postgres",
    port="5432",
    host="localhost",
    password="walvarez00"
)

#CREATE CURSOR FOR CONNECTION
cursor_obj = connect.cursor()

initialize_sql = open(r"C:\Users\xwill\OneDrive\Desktop\psqlPractice\initialize.sql",'r')
cursor_obj.execute(initialize_sql.read())

cardList = Card.where(cmc='10')\
            .all()

# FETCH ALL CARDS
# cardList = Card.all();

insertCard = "INSERT INTO cards (name, multiverse_id, layout, names, mana_cost, cmc, colors, color_identity, type, supertypes, subtypes, rarity, text, flavor, artist, number, power, toughness, loyalty, variations, watermark, border, timeshifted, hand, life, release_date, starter, rulings, foreign_names, printings, original_text, original_type, legalities, source, image_url, set, set_name, id) VALUES ($${0}$$, $${1}$$, $${2}$$, $${3}$$, $${4}$$, $${5}$$, $${6}$$, $${7}$$, $${8}$$, $${9}$$, $${10}$$, $${11}$$, $${12}$$, $${13}$$, $${14}$$, $${15}$$, $${16}$$, $${17}$$, $${18}$$, $${19}$$, $${20}$$, $${21}$$, $${22}$$, $${23}$$, $${24}$$, $${25}$$, $${26}$$, $${27}$$, $${28}$$, $${29}$$, $${30}$$, $${31}$$, $${32}$$, $${33}$$, $${34}$$, $${35}$$, $${36}$$, $${37}$$);"

for x in cardList:
    cursor_obj.execute(insertCard.format(x.name, x.multiverse_id, x.layout, x.names, str(x.mana_cost),  x.cmc, x.colors, x.color_identity, x.type, x.supertypes, x.subtypes, x.rarity, x.text, x.flavor, x.artist, x.number, x.power, x.toughness, x.loyalty, x.variations, x.watermark, x.border, x.timeshifted, x.hand, x.life, x.release_date, x.starter, x.rulings, x.foreign_names, x.printings, x.original_text, x.original_type, x.legalities, x.source, x.image_url, x.set, x.set_name, x.id))
cursor_obj.execute("SELECT * from cards order by name;")

result = cursor_obj.fetchall()
print("Result Set: \n")
for x in result:
    print(x)

cursor_obj.connection.commit()
cursor_obj.close()