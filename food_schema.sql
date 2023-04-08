DROP TABLE IF EXISTS origin;
DROP TABLE IF EXISTS food;

CREATE TABLE origin (
countryID INTEGER PRIMARY KEY AUTOINCREMENT,
country TEXT NOT NULL
);


INSERT INTO origin(country) VALUES ('American'), ('British'), ('Chinese'), ('Italian');

CREATE TABLE food (
foodID INTEGER PRIMARY KEY NOT NULL,
foodName TEXT,
image TEXT,
recipie TEXT,
ingredients TEXT,
cost TEXT,
trackcountryID INTEGER,

FOREIGN KEY (trackcountryID)
REFERENCES origin(countryID)
);

