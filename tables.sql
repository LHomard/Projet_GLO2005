USE MGT_db;

DROP TABLE Card_oracle;
DROP TABLE Sets;
DROP TABLE Card_printing;
DROP TABLE Colors;
DROP TABLE Card_color;
DROP TABLE Formats;
DROP TABLE Legality;
DROP TABLE Players;
DROP TABLE Decks;
DROP TABLE Deck_composition;


-- Nouvelles Tables
CREATE TABLE IF NOT EXISTS Card_oracle (
    id_oracle INT AUTO_INCREMENT PRIMARY KEY,
    name varchar(50) NOT NULL,
    oracle_text TEXT,
    mana_cost VARCHAR(50),
    cmc INT,
    power VARCHAR(10),
    toughness VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS Sets (
    id_sets INT  AUTO_INCREMENT PRIMARY KEY,
    set_name VARCHAR(200) NOT NULL,
    set_code CHAR(3),
    date_sortie DATE
);

CREATE TABLE IF NOT EXISTS Card_printing (
    id_printing INT  AUTO_INCREMENT PRIMARY KEY,
    id_oracle INT REFERENCES Card_oracle(id_oracle) ON DELETE CASCADE,
    id_extension INT REFERENCES Sets(id_sets),
    rarity VARCHAR(20),
    artist VARCHAR(100),
    image_url VARCHAR (300),
    price DECIMAL(7, 2)
);


CREATE TABLE IF NOT EXISTS Colors (
    id_color INT  AUTO_INCREMENT PRIMARY KEY,
    color_name VARCHAR(20) NOT NULL UNIQUE,
    color_symbol CHAR(1)
);


CREATE TABLE IF NOT EXISTS Card_color (
    id_oracle INT REFERENCES Card_oracle(id_oracle) ON DELETE CASCADE,
    id_color INT REFERENCES Colors(id_color),
    PRIMARY KEY (id_oracle, id_color)
);


CREATE TABLE IF NOT EXISTS Formats (
    id_format INT AUTO_INCREMENT PRIMARY KEY,
    format_name VARCHAR(50) NOT NULL UNIQUE,
    max_card_quantity INT
);


CREATE TABLE IF NOT EXISTS Legality (
    id_oracle INT REFERENCES Card_oracle(id_oracle) ON DELETE CASCADE,
    id_format INT REFERENCES Formats(id_format),
    status VARCHAR(20) DEFAULT 'Legal',
    PRIMARY KEY (id_oracle, id_format)
);


CREATE TABLE IF NOT EXISTS Players (
    id_players INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR (255) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    register_date DATE DEFAULT (CURRENT_DATE)
);


CREATE TABLE IF NOT EXISTS Decks (
    id_deck INT  AUTO_INCREMENT PRIMARY KEY,
    id_user INT REFERENCES Players(id_players),
    id_format INT REFERENCES Formats(id_format),
    deck_name VARCHAR(100) NOT NULL,
    deck_image_url VARCHAR (300),
    deck_description TEXT,
    date_creation date NOT NULL
);


CREATE TABLE IF NOT EXISTS Deck_composition (
    id_deck INT REFERENCES Decks(id_deck) ON DELETE CASCADE,
    id_printing INT REFERENCES Card_printing(id_printing),
    quantity INT,
    pillar_cost INT,
    PRIMARY KEY (id_deck, id_printing)
);

SHOW TABLES;

