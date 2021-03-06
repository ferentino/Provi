--
-- PostgreSQL port of the MySQL "World" database.
--
-- The sample data used in the world database is Copyright Statistics 
-- Finland, http://www.stat.fi/worldinfigures.
--

BEGIN;

SET client_encoding = 'UTF8';

CREATE TABLE db_pokemon (
    id_pokemon integer NOT NULL,
    name text NOT NULL,
    base_experience integer NOT NULL,
    weight integer NOT NULL,
    height integer NOT NULL,
    is_default boolean not null,
    PRIMARY KEY (id_pokemon)
);

CREATE TABLE db_abilities (
    id_ability integer NOT NULL,
    name text NOT NULL,
    effect_entries text NOT NULL,
    PRIMARY KEY (id_ability)
);

CREATE TABLE db_types (
    id_type integer NOT NULL,
    name text NOT NULL,
    damage_relations text,
    type_relation integer,
    PRIMARY KEY (id_type)
);

CREATE TABLE db_vinc_pokemon_ability(
    PRIMARY KEY (id_pokemon, id_ability),
    FOREIGN KEY (id_pokemon) REFERENCES db_pokemon(id_pokemon) ON UPDATE CASCADE,
    FOREIGN KEY (id_ability) REFERENCES db_abilities(id_ability) ON UPDATE CASCADE
);

CREATE TABLE db_vinc_pokemon_type(
    PRIMARY KEY (id_pokemon, id_type),
    FOREIGN KEY (id_pokemon) REFERENCES db_pokemon(id_pokemon) ON UPDATE CASCADE,
    FOREIGN KEY (id_type) REFERENCES db_types(id_type) ON UPDATE CASCADE
);

COPY db_pokemon (id_pokemon, name, base_experience, weight, height, is_default) FROM stdin;
1	bulbasaur	64	69	7   True 
2	ivysaur	142 130 10  False
3	venusaur   263  1000    20  True
\.


--
-- Data for Name: country; Type: TABLE DATA; Schema: public; Owner: chriskl
--

COPY db_abilities (id_ability, name, effect_entries) FROM stdin;
65	overgrow	When this Pokémon has 1/3 or less of its HP remaining, its grass-type moves inflict 1.5× as much regular damage.	
34	chlorophyll This Pokémons Speed is doubled during strong sunlight.\n\nThis bonus does not count as a stat modifier.
\.


--
-- Data for Name: countrylanguage; Type: TABLE DATA; Schema: public; Owner: chriskl
--

COPY db_types (id_type, name, damage_relations, type_relation) FROM stdin;
4   grass	double_damage_from	5
4   grass	double_damage_from	14
4   grass   double_damage_to    12
4   grass   double_damage_to    18
4   grass   half_damage_from    2
4   grass   half_damage_from    7
4   grass   half_damage_to  4
12  poison  double_damage_from  3
12  poison  half_damage_from    5
12  poison  half_damage_from    11
12  poison  half_damage_to  3
\.

COPY db_vinc_pokemon_ability(id_pokemon,id_ability) FROM stdin;
1   65
1   34
2   34
3   65
3   34
\.

COPY db_vinc_pokemon_type(id_pokemon,id_type) FROM stdin;
1   4
1   4
2   12
2   12
3   12
\.

COMMIT;

ANALYZE db_pokemon;
ANALYZE db_abilities;
ANALYZE db_types;
ANALYSE db_vinc_pokemon_ability;
ANALYSE db_vinc_pokemon_type;

