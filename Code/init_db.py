import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO countries VALUES(1,'Afghanistan','AF','AFG'),(2,'Aland Islands','AX','ALA'),(3,'Albania','AL','ALB'),(4,'Algeria','DZ','DZA'),(5,'American Samoa','AS','ASM'),(6,'Andorra','AD','AND'),(7,'Angola','AO','AGO'),(8,'Anguilla','AI','AIA'),(9,'Antarctica','AQ','ATA');")
connection.commit()
cur.execute("INSERT INTO ports VALUES(1, 'port1', 1)")
cur.execute("INSERT INTO ports VALUES(2, 'port2', 1)")
connection.commit()
connection.close()
