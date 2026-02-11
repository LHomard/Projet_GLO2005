USE glo2005_database;

CREATE TABLE IF NOT EXISTS cartes  (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    color JSON,
    type_line VARCHAR(50),
    oracle_text TEXT,
    keyword JSON,
    color_identity JSON,
    cmc INT,
    Mana_cost VARCHAR(50),
    price INT
);

CREATE TABLE IF NOT EXISTS Extension  (
    id_extension INT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    date_sortie DATE
);

CREATE TABLE IF NOT EXISTS rules  (
    id_rules INT PRIMARY KEY,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Deck  (
    id_deck INT PRIMARY KEY,
    date_creation date NOT NULL,
    prix_total INT,
    card_quantity INT,
    cout_par_pillier JSON
);

CREATE TABLE IF NOT EXISTS Format  (
    id_format INT PRIMARY KEY,
    card_quantity INT NOT NULL,
    name TEXT,
    card_ban JSON
);

CREATE TABLE IF NOT EXISTS User  (
    id_utilisateur INT PRIMARY KEY,
    date_inscription DATE NOT NULL,
    username TEXT,
    password TEXT,
    email TEXT
);

SHOW TABLES;

SELECT * FROM cartes;

