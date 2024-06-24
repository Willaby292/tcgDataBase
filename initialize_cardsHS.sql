
--TABLE SCHEMAS FOR HEARTHSTONE CARDS.
--cards_HS table stores all card data.
--All other tables are used to store lists that would violate first normal form.

DROP TABLE IF EXISTS cards_HS CASCADE;

CREATE TABLE IF NOT EXISTS cards_HS(
    id                           INTEGER PRIMARY KEY
,   collectible                  INTEGER --need to pull cards with collectable = 0
,   slug                         TEXT
,   classId                      INTEGER --need to create new table which maps class id to a class name. multiclass cards seem to take the first class id in their list of classes. triclass cards seem to take the nuetral class id
--,   multiClassIds                TEXT   --list
,   spellSchoolId                INTEGER --need to map id to spellschool name
,   cardTypeId                   INTEGER -- need to map card type id to card type name
,   cardSetId                    INTEGER --needs mapping
,   rarityId                     INTEGER --needs mapping
,   artistName                   TEXT
,   manaCost                     INTEGER
,   "name"                       TEXT
,   "text"                       TEXT
,   "image"                      TEXT
,   imageGold                    TEXT
,   flavorText                   TEXT
,   cropImage                    TEXT
--,   keywordIds                   TEXT   --list
,   isZilliaxFunctionalModule    BOOLEAN
,   isZilliaxCosmeticModule      BOOLEAN
,   copyOfCardId                 INTEGER --this data seems to be a remap to the card that it was copied from
,   health                       INTEGER
,   attack                       INTEGER
,   minionTypeId                 INTEGER --needs a map to minion type name
--,   childIds                     TEXT   --list
,   armor                        INTEGER
--,   multiTypeIds                 TEXT   --list
,   "durability"                 INTEGER
--,   runeCost                     TEXT   --dictionary
,   parentId                     INTEGER --this seems to be the id of the card who is the actual parent of the character in the card. IE magni bronzebeards parent id is 7 and his parent is gromash? I believe most of the parent IDs refrence uncollectible cards
,   bannedFromSideboard          INTEGER --should be boolean? seems like all banned from sideboard cards are 1 and everything else is null
,   maxSideboardCards            INTEGER
);


DROP TABLE IF EXISTS classes_HS CASCADE;

CREATE TABLE IF NOT EXISTS classes_HS(
    class_id                    INTEGER PRIMARY KEY
,   class_name                  TEXT
,   slug                        TEXT
,   hero_card_id                INTEGER
,   hero_power_card_id          INTEGER
,   alternative_hero_card_ids   INTEGER -- list this needs to be its own table
);

DROP TABLE IF EXISTS classes_link_HS CASCADE;

CREATE TABLE IF NOT EXISTS classes_link_HS(
    card_id            INTEGER
,   class_id           INTEGER 
,   FOREIGN KEY(card_id)
        REFERENCES cards_HS(id)
,   FOREIGN KEY(class_id)
        REFERENCES classes_HS(class_id)
);

DROP TABLE IF EXISTS keywords_HS CASCADE;

CREATE TABLE IF NOT EXISTS keywords_HS(
    keyword_id        TEXT PRIMARY KEY
,   keyword_name      TEXT
);

DROP TABLE IF EXISTS keywords_link_HS CASCADE;

CREATE TABLE IF NOT EXISTS keywords_link_HS(
    card_id                 INTEGER 
,   keyword_id              TEXT
,   FOREIGN KEY(card_id)
        REFERENCES cards_HS(id)
,   FOREIGN KEY(keyword_id)
        REFERENCES keywords_HS(keyword_id)
);

DROP TABLE IF EXISTS referenced_tags_HS CASCADE;

CREATE TABLE IF NOT EXISTS referenced_tags_HS(
    tag_id             INTEGER PRIMARY KEY
,   tag_name           TEXT
);

DROP TABLE IF EXISTS referenced_tags_link_HS CASCADE;

CREATE TABLE IF NOT EXISTS referenced_tags_link_HS(
    card_id                 INTEGER
,   tag_id             INTEGER
,   FOREIGN KEY(card_id)
        REFERENCES cards_HS(id)
,   FOREIGN KEY(tag_id)
        REFERENCES referenced_tags_HS(tag_id)
);

DROP TABLE IF EXISTS counterpart_cards_HS CASCADE;

CREATE TABLE IF NOT EXISTS counterpart_cards_HS(
    id_main           INTEGER
,   id_counterpart    INTEGER
,   FOREIGN KEY(id_main)
        REFERENCES cards_HS(id)
,   FOREIGN KEY(id_counterpart)
        REFERENCES cards_HS(id)
);

DROP TABLE IF EXISTS races_HS CASCADE;

CREATE TABLE IF NOT EXISTS races_HS(
    race_id     TEXT PRIMARY KEY
,   race_name   TEXT
);

DROP TABLE IF EXISTS races_link_HS CASCADE;

CREATE TABLE IF NOT EXISTS races_link_HS(
    card_id             INTEGER
,   race_id            TEXT
,   FOREIGN KEY(card_id)
        REFERENCES cards_HS(id)
,   FOREIGN KEY(race_id)
        REFERENCES races_HS(race_id)
);

DROP TABLE IF EXISTS spellschools_HS CASCADE;

CREATE TABLE IF NOT EXISTS spellschools_HS(
    spellschool_id     INTEGER PRIMARY KEY
,   spellschool_name   TEXT
);

DROP TABLE IF EXISTS spellschools_link_HS CASCADE;

CREATE TABLE IF NOT EXISTS spellschools_link_HS(
    card_id                 INTEGER
,   spellschool_id     INTEGER
,   FOREIGN KEY(card_id)
        REFERENCES cards_HS(id)
,   FOREIGN KEY(spellschool_id)
        REFERENCES spellschools_HS(spellschool_id)
);