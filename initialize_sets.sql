DROP TABLE IF EXISTS sets CASCADE;

CREATE TABLE IF NOT EXISTS sets(
    code                    TEXT
,   "name"                  TEXT
,   gatherer_code           TEXT
,   old_code                TEXT
,   magic_cards_info_code   TEXT
,   release_date            TEXT
,   border                  TEXT
,   "type"                  TEXT
,   block                   TEXT
,   online_only             TEXT
,   booster                 TEXT
,   mkm_id                  TEXT
,   mkm_name                TEXT
);