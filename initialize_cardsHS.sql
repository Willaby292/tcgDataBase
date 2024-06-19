
--TABLE SCHEMAS FOR HEARTHSTONE CARDS.
--cards_HS table stores all card data.
--All other tables are used to store lists that would violate first normal form.

DROP TABLE IF EXISTS cards_HS_raw CASCADE;

CREATE TABLE IF NOT EXISTS cards_HS_raw(
    id                           INTEGER PRIMARY KEY
,   collectible                  INTEGER
,   slug                         TEXT
,   classId                      INTEGER
,   multiClassIds                TEXT    --this is an array of data and should not be TEXT
,   spellSchoolId                INTEGER
,   cardTypeId                   INTEGER
,   cardSetId                    INTEGER
,   rarityId                     INTEGER  
,   artistName                   TEXT
,   manaCost                     INTEGER
,   "name"                       TEXT
,   "text"                       TEXT
,   "image"                      TEXT
,   imageGold                    TEXT
,   flavorText                   TEXT
,   cropImage                    TEXT
,   keywordIds                   TEXT ---this needs to be a different table i believe
,   isZilliaxFunctionalModule    BOOLEAN
,   isZilliaxCosmeticModule      BOOLEAN
,   copyOfCardId                 INTEGER
,   attack                       INTEGER
,   health                       INTEGER
,   minionTypeId                 INTEGER
,   childIds                     TEXT   -- this value is an array

);


DROP TABLE IF EXISTS cards_HS CASCADE;

CREATE TABLE IF NOT EXISTS cards_HS(
    card_id            SERIAL PRIMARY KEY
,   dbfid              INT
,   id                 TEXT
,   "name"             TEXT
,   "type"             TEXT
,   card_class         TEXT
,   player_class       TEXT
,   collectible        BOOLEAN
,   "set"              TEXT
,   rarity             TEXT
,   cost               INT
,   faction            TEXT
,   race               TEXT
,   attack             INT
,   health             INT
,   "durability"       INT
,   mercenary          BOOLEAN
,   mercenary_role     TEXT
,   "text"             TEXT
,   flavor             TEXT
,   artist             TEXT
);

DROP TABLE IF EXISTS audio_HS CASCADE;

CREATE TABLE IF NOT EXISTS audio_HS(
    audio_id           INT PRIMARY KEY
,   card_id            INT
,   audio_type         TEXT
,   audio              TEXT
,   FOREIGN KEY(card_id)
        REFERENCES cards_HS(card_id)
);


DROP TABLE IF EXISTS classes_HS CASCADE;

CREATE TABLE IF NOT EXISTS classes_HS(
    class_id           INT PRIMARY KEY
,   class_name         TEXT
);

DROP TABLE IF EXISTS classes_link_HS CASCADE;

CREATE TABLE IF NOT EXISTS classes_link_HS(
    card_id            INT
,   class_id           INT
,   FOREIGN KEY(card_id)
        REFERENCES cards_HS(card_id)
,   FOREIGN KEY(class_id)
        REFERENCES classes_HS(class_id)
);

DROP TABLE IF EXISTS mechanics_HS CASCADE;

CREATE TABLE IF NOT EXISTS mechanics_HS(
    mechanic_id        TEXT PRIMARY KEY
,   mechanic_name      TEXT
);

DROP TABLE IF EXISTS mechanics_link_HS CASCADE;

CREATE TABLE IF NOT EXISTS mechanics_link_HS(
    card_id            INT
,   mechanic_id        TEXT
,   FOREIGN KEY(card_id)
        REFERENCES cards_HS(card_id)
,   FOREIGN KEY(mechanic_id)
        REFERENCES mechanics_HS(mechanic_id)
);

DROP TABLE IF EXISTS referenced_tags_HS CASCADE;

CREATE TABLE IF NOT EXISTS referenced_tags_HS(
    tag_id             INT PRIMARY KEY
,   tag_name           TEXT
);

DROP TABLE IF EXISTS referenced_tags_link_HS CASCADE;

CREATE TABLE IF NOT EXISTS referenced_tags_link_HS(
    card_id            INT
,   tag_id             INT
,   FOREIGN KEY(card_id)
        REFERENCES cards_HS(card_id)
,   FOREIGN KEY(tag_id)
        REFERENCES referenced_tags_HS(tag_id)
);

DROP TABLE IF EXISTS counterpart_cards_HS CASCADE;

CREATE TABLE IF NOT EXISTS counterpart_cards_HS(
    card_id_main           INT
,   card_id_counterpart    INT
,   FOREIGN KEY(card_id_main)
        REFERENCES cards_HS(card_id)
,   FOREIGN KEY(card_id_counterpart)
        REFERENCES cards_HS(card_id)
);

DROP TABLE IF EXISTS races_HS CASCADE;

CREATE TABLE IF NOT EXISTS races_HS(
    race_id     TEXT PRIMARY KEY
,   race_name   TEXT
);

DROP TABLE IF EXISTS races_link_HS CASCADE;

CREATE TABLE IF NOT EXISTS races_link_HS(
    card_id            INT
,   race_id            TEXT
,   FOREIGN KEY(card_id)
        REFERENCES cards_HS(card_id)
,   FOREIGN KEY(race_id)
        REFERENCES races_HS(race_id)
);

DROP TABLE IF EXISTS spellschools_HS CASCADE;

CREATE TABLE IF NOT EXISTS spellschools_HS(
    spellschool_id     INT PRIMARY KEY
,   spellschool_name   TEXT
);

DROP TABLE IF EXISTS spellschools_link_HS CASCADE;

CREATE TABLE IF NOT EXISTS spellschools_link_HS(
    card_id            INT
,   spellschool_id     INT
,   FOREIGN KEY(card_id)
        REFERENCES cards_HS(card_id)
,   FOREIGN KEY(spellschool_id)
        REFERENCES spellschools_HS(spellschool_id)
);