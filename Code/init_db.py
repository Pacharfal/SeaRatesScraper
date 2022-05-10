import sqlite3
from bs4 import BeautifulSoup
import requests
import sqlite3

#getting connection to db
connection = sqlite3.connect('database.db')
cur = connection.cursor()

#deleting all if any previous data exists --> removing duplicates
sql = "DROP TABLE IF EXISTS countries;"
cur.execute(sql)
sql = "DROP TABLE IF EXISTS ports;"
cur.execute(sql)
connection.commit()

#creating tables with all attributes, ports and countries are connected via foreign key in table ports
sql = "CREATE TABLE countries (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL);"
cur.execute(sql)
sql = "CREATE TABLE ports(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,country_id INT, address TEXT, port_auth TEXT, phone INT, fax INT, email TEXT, cords TEXT, cords_dec TEXT, un TEXT, type TEXT, size TEXT, website TEXT, terminal TEXT,FOREIGN KEY(country_id) REFERENCES countries(id));"
cur.execute(sql)
connection.commit()
conn.close()


#selection of substrings contained in data that is needed to be removed
substring1 = "/"
substring2 = ";"
substring3 = "tel"


#base page with list of all countries
url = "https://www.searates.com/maritime/"
#using requests to get data from url
result = requests.get(url)
#parsing all data using BS4
doc = BeautifulSoup(result.text, "html.parser")
conn = get_db_connection()
#delete all posible data in DB
conn.execute("DELETE FROM countries")
conn.commit()

#looping thru all 'a href' tags using find_all
for a in doc.find_all('a', href=True):
    #removing string from previous result to get just the name of the port
    out = a['href'].replace("/maritime/","")
    #sequence of ifs to remove all results with given substrings to remove parasitic data
    if not search(substring1, out):
        if not search(substring2, out):
            if not search(substring3, out):
                #saving result as another variable before changing it any more to use it later for new url
                out_url = out
                out = out.replace("_", " ")
                #inserting name of country into table
                conn.execute("INSERT INTO countries(name) VALUES(?)",[out])
                conn.commit()

                #navigating to page of each country eg. https://www.searates.com/maritime/czech_republic
                url2 = "https://www.searates.com/maritime/"+out_url
                result2 = requests.get(url2)
                doc2 = BeautifulSoup(result2.text, "html.parser")
                #getting all 'a href' tags listed as a port
                for a in doc2.find_all('a', href=True):
                    out2 = a['href'].replace("/port/","")
                    #removing all parasitic data
                    if not search(substring1, out2):
                        if not search(substring2, out2):
                            if not search(substring3, out2):
                                #saving result to another variable to use it later
                                out2_url = out2
                                #removing last 3 chars of result to get rid of eg. '_al' at the end of the name of port
                                out2 = out2[:- 3]
                                out2 = out2.replace("_", " ")
                                #logging out to console
                                print(out2)

                                #country id has to be selected from countries to use it in later insert
                                cursor = conn.cursor()
                                result = cursor.execute('SELECT id FROM countries WHERE name = ?', [out])
                                rows = result.fetchone()
                                c_id = rows[0]

                                #inserting port name and linking it with country using country id obtained earlier
                                conn.execute("INSERT INTO ports(name, country_id) VALUES (?, ?)",[out2, str(c_id)])
                                conn.commit()

                                #url for page of given port e.g. https://www.searates.com/port/durres_al
                                url3 = "https://www.searates.com/port/"+out2_url
                                page = requests.get(url3)
                                soup = BeautifulSoup(page.text, "html.parser")

                                #setting up a variable to have break point for loop
                                x = 0
                                #getting all spans with given class name
                                for a in soup.find_all('span', class_="incoterms-block__text"):
                                    #adding one for each cycle
                                    x=x+1
                                    #stopping after 25 cycles
                                    if x == 25:
                                        break
                                    #each even step works with value, each odd step is just name of field which we dont need
                                    if x%2 == 0:
                                        #logging
                                        print(a.text)
                                        #using .text to get text of each 'a' tag
                                        value = a.text
                                        #selecting which value needs to be updated
                                        if x==2:
                                            conn.execute("UPDATE ports SET address = ? WHERE name = ?",[value, out2])
                                        if x==4:
                                            conn.execute("UPDATE ports SET port_auth = ? WHERE name = ?",[value, out2])
                                        if x==6:
                                            conn.execute("UPDATE ports SET phone = ? WHERE name = ?",[value, out2])
                                        if x==8:
                                            conn.execute("UPDATE ports SET fax = ? WHERE name = ?",[value, out2])
                                        if x==10:
                                            conn.execute("UPDATE ports SET email = ? WHERE name = ?",[value, out2])
                                        if x==12:
                                            conn.execute("UPDATE ports SET cords = ? WHERE name = ?",[value, out2])
                                        if x==14:
                                            conn.execute("UPDATE ports SET cords_dec = ? WHERE name = ?",[value, out2])
                                        if x==16:
                                            conn.execute("UPDATE ports SET un = ? WHERE name = ?",[value, out2])
                                        if x==18:
                                            conn.execute("UPDATE ports SET type = ? WHERE name = ?",[value, out2])
                                        if x==20:
                                            conn.execute("UPDATE ports SET size = ? WHERE name = ?",[value, out2])
                                        if x==22:
                                            conn.execute("UPDATE ports SET website = ? WHERE name = ?",[value, out2])
                                        if x==24:
                                            conn.execute("UPDATE ports SET terminal = ? WHERE name = ?",[value, out2])
                                        conn.commit()
conn.close()
connection.close()
