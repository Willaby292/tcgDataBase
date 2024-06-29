
--TABLE SCHEMAS FOR HEARTHSTONE CARDS.
--cards_HS table stores all card data.
--All other tables are used to store lists that would violate first normal form.

DROP TABLE IF EXISTS cards_HS CASCADE;

CREATE TABLE IF NOT EXISTS cards_HS(
    cardId                          INT PRIMARY KEY
,   "name"                          TEXT
,   manaCost                        INT
,   attack                          INT
,   health                          INT
,   "durability"                    INT
,   "text"                          TEXT
,   armor                           INT
,   collectible                     INT
,   flavorText                      TEXT
,   "image"                         TEXT
,   imageGold                       TEXT
,   cropImage                       TEXT
,   artistName                      TEXT
,   slug                            TEXT
,   classId                         INT
,   cardTypeId                      INT
,   cardSetId                       INT
,   rarityId                        INT
,   minionTypeId                    INT
,   spellSchoolId                   INT
,   copyOfCardId                    INT
,   parentId                        INT
,   isZilliaxFunctionalModule       BOOLEAN
,   isZilliaxCosmeticModule         BOOLEAN
,   bannedFromSideboard             INT    ---after database is set up check to see if there are any non 1 or 0 values
,   maxSideboardCards               INT
);

DROP TABLE IF EXISTS classes_HS CASCADE;

CREATE TABLE IF NOT EXISTS classes_HS(
    classId                 INT PRIMARY KEY
,   heroCardId              INT
,   className               TEXT
,   heroPowerCardId         INT
,   slug                    TEXT
);

DROP TABLE IF EXISTS classes_link_HS;

CREATE TABLE IF NOT EXISTS  classes_link_HS(
    cardId      INT REFERENCES cards_HS(cardId)
,   classId     INT REFERENCES classes_HS(classId)
,   PRIMARY KEY (cardId, classId)
);

DROP TABLE IF EXISTS alternate_heros_HS;

CREATE TABLE IF NOT EXISTS  alternate_heros_HS(
    classId        INT REFERENCES classes_HS(classId)
,   altHeroCardId  INT --REFERENCES cards_HS(cardId) need to find these in api and add to card table. Can do with specific card search but some are still missing like warriors main class card
,   PRIMARY KEY (classId, altHeroCardId)
);

DROP TABLE IF EXISTS rarities_HS CASCADE;

CREATE TABLE IF NOT EXISTS rarities_HS(
    rarityId               INT PRIMARY KEY
,   craftingCostNormal     INT
,   craftingCostGolden     INT
,   dustValueNormal        INT
,   dustValueGolden        INT
,   rarityName             TEXT
,   slug                   TEXT
);

DROP TABLE IF EXISTS bg_cards_HS CASCADE;

CREATE TABLE IF NOT EXISTS bg_cards_HS(
    bgId                    SERIAL PRIMARY KEY
,   cardId                  INT REFERENCES cards_HS(cardId)
,   tier                    INT
,   isHero                  BOOLEAN
,   isQuest                 BOOLEAN
,   isReward                BOOLEAN
,   isDuosOnly              BOOLEAN
,   isSolosOnly             BOOLEAN
,   upgradeId               INT
,   "image"                 TEXT
,   imageGold               TEXT
);

DROP TABLE IF EXISTS set_groups_HS CASCADE;

CREATE TABLE IF NOT EXISTS set_groups_HS(
    setGroupId          SERIAL PRIMARY KEY
,   setGroupName        TEXT
,   isStandard          BOOLEAN
,   svg                 TEXT
,   icon                TEXT
,   year                INT
,   yearRange           TEXT
,   slug                TEXT
);

DROP TABLE IF EXISTS sets_HS CASCADE;

CREATE TABLE IF NOT EXISTS sets_HS(
    setId                               INT PRIMARY KEY
,   setName                             TEXT
,   setGroupId                          INT REFERENCES set_groups_HS(setGroupId)
,   isHyped                             BOOLEAN
,   setType                             TEXT
,   collectibleCount                    INT
,   collectibleRevealedCount            INT
,   nonCollectibleCount                 INT
,   nonCollectibleReavealedCount        INT
,   slug                                TEXT
);

DROP TABLE IF EXISTS sets_link_set_groups_HS CASCADE;

CREATE TABLE IF NOT EXISTS  sets_link_set_groups_HS(
    setId           INT REFERENCES sets_HS(setId)
,   setGroupId      INT REFERENCES set_groups_HS(setGroupId)
,   PRIMARY KEY (setId, setGroupId)
);


DROP TABLE IF EXISTS set_alias_HS CASCADE;

CREATE TABLE IF NOT EXISTS set_alias_HS(
    setId       INT REFERENCES sets_HS(setId)
,   aliasId     INT
,   PRIMARY KEY (setId, aliasId)
);

DROP TABLE IF EXISTS rune_costs_HS CASCADE;

CREATE TABLE IF NOT EXISTS rune_costs_HS(
    runeId               SERIAL PRIMARY KEY
,   card_id              INT REFERENCES cards_HS(cardId)
,   bloodRuneCount       INT
,   frostRuneCount       INT
,   unholyRuneCount      INT
);

DROP TABLE IF EXISTS minion_types_HS CASCADE;

CREATE TABLE IF NOT EXISTS minion_types_HS(
    minionTypeId                 INT PRIMARY KEY
,   minionTypeName               TEXT
,   slug                         TEXT
);

DROP TABLE IF EXISTS minion_types_link_HS CASCADE;

CREATE TABLE IF NOT EXISTS  minion_types_link_HS(
    cardId           INT REFERENCES cards_HS(cardId)
,   minionTypeId     INT REFERENCES minion_types_HS(minionTypeId)
,   PRIMARY KEY (cardId, minionTypeId)
);

DROP TABLE IF EXISTS game_modes_HS CASCADE;

CREATE TABLE IF NOT EXISTS  game_modes_HS(
    gameModeId      INT PRIMARY KEY
,   gameModeName    TEXT
,   slug            TEXT
);

DROP TABLE IF EXISTS minion_types_link_game_modes_HS CASCADE;

CREATE TABLE IF NOT EXISTS  minion_types_link_game_modes_HS(
    gameModeId           INT REFERENCES game_modes_HS(gameModeId)
,   minionTypeId         INT REFERENCES minion_types_HS(minionTypeId)
,   PRIMARY KEY (gameModeId, minionTypeId)
);

DROP TABLE IF EXISTS keywords_HS CASCADE;

CREATE TABLE IF NOT EXISTS  keywords_HS(
    keywordId       INT PRIMARY KEY
,   keywordName     TEXT
,   keywordText     TEXT
,   refText         TEXT
,   slug            TEXT
);

DROP TABLE IF EXISTS keywords_link_HS CASCADE;

CREATE TABLE IF NOT EXISTS  keywords_link_HS(
    cardId          INT REFERENCES cards_HS(cardId)
,   keywordId       INT REFERENCES keywords_HS(keywordId)
,   PRIMARY KEY (cardId, keywordId)
);

DROP TABLE IF EXISTS keywords_link_game_modes_HS CASCADE;

CREATE TABLE IF NOT EXISTS  keywords_link_game_modes_HS(
    gameModeId      INT REFERENCES game_modes_HS(gameModeId)
,   keywordId       INT REFERENCES keywords_HS(keywordId)
,   PRIMARY KEY (gameModeId, keywordId)
);

DROP TABLE IF EXISTS types_HS CASCADE;

CREATE TABLE IF NOT EXISTS  types_HS(
    typeId          INT PRIMARY KEY
,   typeName        TEXT
,   slug            TEXT
);

DROP TABLE IF EXISTS types_link_game_modes_HS CASCADE;

CREATE TABLE IF NOT EXISTS  types_link_game_modes_HS(
    gameModeId      INT REFERENCES game_modes_HS(gameModeId)
,   typeId           INT REFERENCES types_HS(typeId)
,   PRIMARY KEY (gameModeId, typeId)
);

DROP TABLE IF EXISTS spell_schools_HS CASCADE;

CREATE TABLE IF NOT EXISTS  spell_schools_HS(
    spellSchoolId       INT PRIMARY KEY
,   spellSchoolName     TEXT
,   slug                TEXT
);

DROP TABLE IF EXISTS card_remap_HS CASCADE;

CREATE TABLE IF NOT EXISTS  card_remap_HS(
    parentId    INT REFERENCES cards_HS(cardId)
,   childId               INT
,   PRIMARY KEY (parentId, childId)
);

DROP TABLE IF EXISTS bg_game_modes_HS CASCADE;

CREATE TABLE IF NOT EXISTS  bg_game_modes_HS(
    bgGameModeId    INT PRIMARY KEY
,   bgGameModeName  TEXT
,   slug            TEXT
);
