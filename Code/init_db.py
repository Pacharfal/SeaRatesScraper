import sqlite3

connection = sqlite3.connect('database.db')
cur = connection.cursor()
sql = "DROP TABLE IF EXISTS countries;"
cur.execute(sql)
sql = "DROP TABLE IF EXISTS ports;"
cur.execute(sql)
sql = "CREATE TABLE countries (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL);"
cur.execute(sql)
sql = "CREATE TABLE ports(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,country_id INT,FOREIGN KEY(country_id) REFERENCES countries(id));"
cur.execute(sql)
connection.commit()
connection.close()
