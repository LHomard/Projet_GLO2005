USE MGT_db;


CREATE TABLE IF NOT EXISTS Card_oracle (
    id_oracle INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT,
    oracle_text TEXT,
    mana_cost VARCHAR(50),
    cmc INT,
    power VARCHAR(10),
    toughness VARCHAR(10),
    type_line TEXT
);

CREATE TABLE IF NOT EXISTS Sets (
    id_set INT AUTO_INCREMENT PRIMARY KEY,
    card_count INT,
    set_name VARCHAR(200) NOT NULL,
    set_code TEXT,
    icon_url VARCHAR(300),
    release_date DATE
);

CREATE TABLE IF NOT EXISTS Card_printing (
    id_printing INT  AUTO_INCREMENT PRIMARY KEY,
    id_oracle INT REFERENCES Card_oracle(id_oracle) ON DELETE CASCADE,
    id_set INT REFERENCES Sets(id_set),
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


CREATE TABLE IF NOT EXISTS Card_colors (
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
    id_player INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR (255) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    register_date DATE DEFAULT (CURRENT_DATE)
);


CREATE TABLE IF NOT EXISTS Decks (
    id_deck INT  AUTO_INCREMENT PRIMARY KEY,
    id_user INT REFERENCES Players(id_player),
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

CREATE TABLE IF NOT EXISTS Ai_chats (
    id_chat INT AUTO_INCREMENT PRIMARY KEY,
    id_player INT NOT NULL,
    title VARCHAR(255) DEFAULT 'New Chat',
    chats JSON,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_player) REFERENCES Players(id_player) ON DELETE CASCADE
);

