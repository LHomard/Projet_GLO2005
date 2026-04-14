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
    age INT NOT NULL,
    password_hash TEXT NOT NULL,
    register_date DATE DEFAULT (CURRENT_DATE)
);


-- Trigger permettant de vérifier l'âge ainsi que la validité du email lors de la création d'un joueur
DELIMITER $$

CREATE TRIGGER before_insert_player
BEFORE INSERT ON Players
FOR EACH ROW
BEGIN
    IF NEW.age < 1 OR NEW.age > 100 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid age: must be between 1 and 100.';
    END IF;

    IF NEW.username = '' OR NEW.username IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Username cannot be empty.';
    END IF;

    IF NEW.email NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid email format.';
    END IF;
END$$

DELIMITER ;

-- Trigger permettant de vérifier l'âge ainsi que la validité du email lors de la mise à jour d'un joueur
DELIMITER $$

CREATE TRIGGER before_update_player
BEFORE UPDATE ON Players
FOR EACH ROW
BEGIN
    IF NEW.age < 1 OR NEW.age > 120 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid age: must be between 1 and 120.';
    END IF;

    IF NEW.username = '' OR NEW.username IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Username cannot be empty.';
    END IF;

    IF NEW.email NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid email format.';
    END IF;
END$$

DELIMITER ;


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

-- Trigger called before deck creation to verify its legality
CREATE TRIGGER before_insert_deck_composition
BEFORE INSERT ON Deck_composition
FOR EACH ROW
BEGIN
    DECLARE card_status VARCHAR(20);
    DECLARE format_id INT;
    DECLARE max_qty INT;
    DECLARE current_qty INT;

    -- Retrieves deck format
    SELECT id_format INTO format_id
    FROM Decks
    WHERE id_deck = NEW.id_deck;

    -- Verifies deck legality
    SELECT l.status INTO card_status
    FROM Legality l
    JOIN Card_printing cp ON l.id_oracle = cp.id_oracle
    WHERE cp.id_printing = NEW.id_printing
    AND l.id_format = format_id;

    IF card_status IS NULL OR card_status != 'Legal' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'This card is not legal in this deck format.';
    END IF;

    -- Verifies if card quantity is legal
    SELECT max_card_quantity INTO max_qty
    FROM Formats
    WHERE id_format = format_id;

    SELECT COALESCE(quantity, 0) INTO current_qty
    FROM Deck_composition
    WHERE id_deck = NEW.id_deck AND id_printing = NEW.id_printing;

    IF max_qty IS NOT NULL AND (current_qty + NEW.quantity) > max_qty THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Card quantity exceeds the format limit.';
    END IF;
END$$

DELIMITER ;



CREATE TABLE IF NOT EXISTS Ai_chats (
    id_player INT REFERENCES Players(id_player) ON DELETE CASCADE,
    chats TEXT
)

