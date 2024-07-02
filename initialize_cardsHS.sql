
--TABLE SCHEMAS FOR HEARTHSTONE CARDS.
--cards_HS table stores all card data.
--All other tables are used to store lists that would violate first normal form.

DROP TABLE IF EXISTS cards_HS CASCADE;

CREATE TABLE IF NOT EXISTS cards_HS(
    card_id                         INT PRIMARY KEY
,   "name"                          TEXT
,   mana_cost                       INT
,   attack                          INT
,   health                          INT
,   "durability"                    INT
,   "text"                          TEXT
,   armor                           INT
,   collectible                     INT
,   flavor_text                     TEXT
,   "image"                         TEXT
,   image_gold                      TEXT
,   crop_image                      TEXT
,   artist_name                     TEXT
,   slug                            TEXT
,   class_id                        INT
,   card_type_id                    INT
,   card_set_id                     INT
,   rarity_id                       INT
,   minion_type_id                  INT
,   spell_school_id                 INT
,   copy_of_card_id                 INT
,   parent_id                       INT
,   is_zilliax_functional_module    BOOLEAN
,   is_zilliax_cosmetic_module      BOOLEAN
,   banned_from_sideboard           INT    ---after database is set up check to see if there are any non 1 or 0 values
,   max_sideboard_cards             INT
);

DROP TABLE IF EXISTS classes_HS CASCADE;

CREATE TABLE IF NOT EXISTS classes_HS(
    class_id                INT PRIMARY KEY
,   hero_card_id            INT
,   class_name              TEXT
,   hero_power_card_id      INT
,   slug                    TEXT
);

DROP TABLE IF EXISTS classes_link_HS;

CREATE TABLE IF NOT EXISTS  classes_link_HS(
    card_id      INT REFERENCES cards_HS(card_id)
,   class_id     INT REFERENCES classes_HS(class_id)
,   PRIMARY KEY (card_id, class_id)
);

DROP TABLE IF EXISTS alternate_heros_HS;

CREATE TABLE IF NOT EXISTS  alternate_heros_HS(
    class_id            INT REFERENCES classes_HS(class_id)
,   alt_hero_card_id    INT --REFERENCES cards_HS(card_id) need to find these in api and add to card table. _can do with specific card search but some are still missing like warriors main class card
,   PRIMARY KEY (class_id, alt_hero_card_id)
);

DROP TABLE IF EXISTS rarities_HS CASCADE;

CREATE TABLE IF NOT EXISTS rarities_HS(
    rarity_id                INT PRIMARY KEY
,   crafting_cost_normal     INT
,   crafting_cost_golden     INT
,   dust_value_normal        INT
,   dust_value_golden        INT
,   rarity_name              TEXT
,   slug                     TEXT
);

DROP TABLE IF EXISTS bg_cards_HS CASCADE;

CREATE TABLE IF NOT EXISTS bg_cards_HS(
    bg_id                   SERIAL PRIMARY KEY
,   card_id                 INT REFERENCES cards_HS(card_id)
,   tier                    INT
,   is_hero                 BOOLEAN
,   is_quest                BOOLEAN
,   is_reward               BOOLEAN
,   is_duos_only            BOOLEAN
,   is_solos_only           BOOLEAN
,   upgrade_id              INT
,   "image"                 TEXT
,   image_gold              TEXT
);

DROP TABLE IF EXISTS set_groups_HS CASCADE;

CREATE TABLE IF NOT EXISTS set_groups_HS(
    set_group_id          SERIAL PRIMARY KEY
,   set_group_name        TEXT
,   is_standard           BOOLEAN
,   svg                   TEXT
,   icon                  TEXT
,   year                  INT
,   year_range            TEXT
,   slug                  TEXT
);

DROP TABLE IF EXISTS sets_HS CASCADE;

CREATE TABLE IF NOT EXISTS sets_HS(
    set_id                               INT PRIMARY KEY
,   set_name                             TEXT
,   set_group_id                         INT REFERENCES set_groups_HS(set_group_id)
,   is_hyped                             BOOLEAN
,   set_type                             TEXT
,   collectible_count                    INT
,   collectible_revealed_count           INT
,   non_collectible_count                INT
,   non_collectible_reavealed_count      INT
,   slug                                 TEXT
);

DROP TABLE IF EXISTS sets_link_set_groups_HS CASCADE;

CREATE TABLE IF NOT EXISTS  sets_link_set_groups_HS(
    set_id            INT REFERENCES sets_HS(set_id)
,   set_group_id      INT REFERENCES set_groups_HS(set_group_id)
,   PRIMARY KEY (set_id, set_group_id)
);


DROP TABLE IF EXISTS set_alias_HS CASCADE;

CREATE TABLE IF NOT EXISTS set_alias_HS(
    set_id       INT REFERENCES sets_HS(set_id)
,   alias_id     INT
,   PRIMARY KEY (set_id, alias_id)
);

DROP TABLE IF EXISTS rune_costs_HS CASCADE;

CREATE TABLE IF NOT EXISTS rune_costs_HS(
    card_id                INT REFERENCES cards_HS(card_id)
,   blood_rune_count       INT
,   frost_rune_count       INT
,   unholy_rune_count      INT
,   PRIMARY KEY (card_id, blood_rune_count, frost_rune_count, unholy_rune_count)
);

DROP TABLE IF EXISTS minion_types_HS CASCADE;

CREATE TABLE IF NOT EXISTS minion_types_HS(
    minion_type_id               INT PRIMARY KEY
,   minion_type_name             TEXT
,   slug                         TEXT
);

DROP TABLE IF EXISTS minion_types_link_HS CASCADE;

CREATE TABLE IF NOT EXISTS  minion_types_link_HS(
    card_id            INT REFERENCES cards_HS(card_id)
,   minion_type_id     INT REFERENCES minion_types_HS(minion_type_id)
,   PRIMARY KEY (card_id, minion_type_id)
);

DROP TABLE IF EXISTS game_modes_HS CASCADE;

CREATE TABLE IF NOT EXISTS  game_modes_HS(
    game_mode_id      INT PRIMARY KEY
,   game_mode_name    TEXT
,   slug              TEXT
);

DROP TABLE IF EXISTS minion_types_link_game_modes_HS CASCADE;

CREATE TABLE IF NOT EXISTS  minion_types_link_game_modes_HS(
    minion_type_id         INT REFERENCES minion_types_HS(minion_type_id)
,   game_mode_id           INT REFERENCES game_modes_HS(game_mode_id)
,   PRIMARY KEY (game_mode_id, minion_type_id)
);

DROP TABLE IF EXISTS keywords_HS CASCADE;

CREATE TABLE IF NOT EXISTS  keywords_HS(
    keyword_id       INT PRIMARY KEY
,   keyword_name     TEXT
,   keyword_text     TEXT
,   ref_text         TEXT
,   slug             TEXT
);

DROP TABLE IF EXISTS keywords_link_HS CASCADE;

CREATE TABLE IF NOT EXISTS  keywords_link_HS(
    card_id          INT REFERENCES cards_HS(card_id)
,   keyword_id       INT REFERENCES keywords_HS(keyword_id)
,   PRIMARY KEY (card_id, keyword_id)
);

DROP TABLE IF EXISTS keywords_link_game_modes_HS CASCADE;

CREATE TABLE IF NOT EXISTS  keywords_link_game_modes_HS(
    keyword_id        INT REFERENCES keywords_HS(keyword_id)
,   game_mode_id      INT REFERENCES game_modes_HS(game_mode_id)
,   PRIMARY KEY (game_mode_id, keyword_id)
);

DROP TABLE IF EXISTS types_HS CASCADE;

CREATE TABLE IF NOT EXISTS  types_HS(
    type_id          INT PRIMARY KEY
,   type_name        TEXT
,   slug             TEXT
);

DROP TABLE IF EXISTS types_link_game_modes_HS CASCADE;

CREATE TABLE IF NOT EXISTS  types_link_game_modes_HS(
    type_id           INT REFERENCES types_HS(type_id)
,   game_mode_id      INT REFERENCES game_modes_HS(game_mode_id)
,   PRIMARY KEY (game_mode_id, type_id)
);

DROP TABLE IF EXISTS spell_schools_HS CASCADE;

CREATE TABLE IF NOT EXISTS  spell_schools_HS(
    spell_school_id       INT PRIMARY KEY
,   spell_school_name     TEXT
,   slug                  TEXT
);

DROP TABLE IF EXISTS card_remap_HS CASCADE;

CREATE TABLE IF NOT EXISTS  card_remap_HS(
    parent_id      INT REFERENCES cards_HS(card_id)
,   child_id       INT
,   PRIMARY KEY (parent_id, child_id)
);

DROP TABLE IF EXISTS bg_game_modes_HS CASCADE;

CREATE TABLE IF NOT EXISTS  bg_game_modes_HS(
    bg_game_mode_id    INT PRIMARY KEY
,   bg_game_mode_name  TEXT
,   slug               TEXT
);
