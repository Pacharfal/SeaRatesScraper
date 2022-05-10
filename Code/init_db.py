import sqlite3

connection = sqlite3.connect('database.db')
cur = connection.cursor()
sql = "DROP TABLE IF EXISTS countries;"
cur.execute(sql)
sql = "DROP TABLE IF EXISTS ports;"
cur.execute(sql)
connection.commit()
sql = "CREATE TABLE countries (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL);"
cur.execute(sql)
sql = "CREATE TABLE ports(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,country_id INT, address TEXT, port_auth TEXT, phone INT, fax INT, email TEXT, cords TEXT, cords_dec TEXT, un TEXT, type TEXT, size TEXT, website TEXT, terminal TEXT,FOREIGN KEY(country_id) REFERENCES countries(id));"
cur.execute(sql)
connection.commit()
connection.close()
