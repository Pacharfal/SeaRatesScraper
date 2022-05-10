from flask import Flask, render_template, redirect, url_for
from bs4 import BeautifulSoup
from re import search
import requests
import datetime
import sqlite3
import re
app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn



substring1 = "/"
substring2 = ";"
substring3 = "tel"


url = "https://www.searates.com/maritime/"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")
conn = get_db_connection()
conn.execute("DELETE FROM countries")
conn.commit()
for a in doc.find_all('a', href=True):
    out = a['href'].replace("/maritime/","")
    if not search(substring1, out):
        if not search(substring2, out):
            if not search(substring3, out):
                out_url = out
                out = out.replace("_", " ")
                conn.execute("INSERT INTO countries(name) VALUES(?)",[out])
                conn.commit()
                url2 = "https://www.searates.com/maritime/"+out_url
                result2 = requests.get(url2)
                doc2 = BeautifulSoup(result2.text, "html.parser")
                for a in doc2.find_all('a', href=True):
                    out2 = a['href'].replace("/port/","")
                    if not search(substring1, out2):
                        if not search(substring2, out2):
                            if not search(substring3, out2):
                                out2_url = out2
                                out2 = out2[:- 3]
                                out2 = out2.replace("_", " ")
                                print(out2)
                                cursor = conn.cursor()
                                result = cursor.execute('SELECT id FROM countries WHERE name = ?', [out])
                                rows = result.fetchone()
                                c_id = rows[0]
                                conn.execute("INSERT INTO ports(name, country_id) VALUES (?, ?)",[out2, str(c_id)])
                                conn.commit()
                                url3 = "https://www.searates.com/port/"+out2_url
                                page = requests.get(url3)
                                soup = BeautifulSoup(page.text, "html.parser")
                                x = 0
                                for a in soup.find_all('span', class_="incoterms-block__text"):
                                    x=x+1
                                    if x == 25:
                                        break
                                    if x%2 == 0:
                                        print(a.text)
                                        value = a.text
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


@app.route("/")
def index():
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/scrape")
def scrape():
    conn = get_db_connection()
    countries = conn.execute('SELECT * FROM countries').fetchall()
    return render_template('scrape.html', countries=countries)
    conn.close()

@app.route("/country/<id>")
def country(id):
    conn = get_db_connection()
    country = conn.execute('SELECT * FROM ports WHERE country_id = ?', [id]).fetchall()
    return render_template("country.html", country=country)
    conn.close()

@app.route("/port/<int:id>")
def port(id):
    conn = get_db_connection()
    port = conn.execute('SELECT * FROM ports WHERE id = ?', [id]).fetchall()
    return render_template("port.html", port=port)
    conn.close()
