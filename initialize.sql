DROP TYPE IF EXISTS layout_enum;

CREATE TYPE layout_enum AS ENUM('normal', 'split', 'flip', 'double-faced', 'token', 'plane', 'scheme', 'phenomenon', 'leveler', 'vangaurd', 'aftermath', 'prototype', 'reversible_card', 'adventure');
-- CREATE TYPE rarity_enum AS ENUM('');

DROP TABLE IF EXISTS cards CASCADE;

CREATE TABLE IF NOT EXISTS cards(
    "name"                TEXT
,   multiverse_id       TEXT
,   layout              layout_enum
,   names               TEXT
,   mana_cost           TEXT
,   cmc                 NUMERIC
,   colors              TEXT
,   color_identity      TEXT
,   "type"                TEXT
,   supertypes          TEXT
,   subtypes            TEXT
,   rarity              TEXT
,   "text"                TEXT
,   flavor              TEXT
,   artist              TEXT
,   "number"              TEXT 
,   power               TEXT
,   toughness           TEXT
,   loyalty             TEXT
,   variations          TEXT 
,   watermark           TEXT
,   border              TEXT 
,   timeshifted         TEXT
,   hand                TEXT
,   life                TEXT
--,   reserved            TEXT
,   release_date        TEXT
,   starter             TEXT
,   rulings             TEXT
,   foreign_names       TEXT
,   printings           TEXT
,   original_text       TEXT
,   original_type       TEXT
,   legalities          TEXT
,   source              TEXT
,   image_url           TEXT
,   "set"                 TEXT
,   set_name            TEXT
,   id                  TEXT
);
