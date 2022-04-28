DROP TABLE IF EXISTS countries;
DROP TABLE IF EXISTS ports;
CREATE TABLE countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    countrycode TEXT NOT NULL,
    countrycodelong TEXT NOT NULL
);

CREATE TABLE ports(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  country_id INTEGER,
  FOREIGN KEY(country_id) REFERENCES countries(id)
);
