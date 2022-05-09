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

#substrings to remove
substring1 = "/"
substring2 = ";"
substring3 = "tel"

#COUNTRIES SCRAPE
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
                url_out = out
                out = out.replace("_", " ")
                conn.execute("INSERT INTO countries(name) VALUES(?)",[out])
                conn.commit()


                url2 = "https://www.searates.com/maritime/"+out
                result2 = requests.get(url2)
                doc2 = BeautifulSoup(result2.text, "html.parser")
                for a in doc2.find_all('a', href=True):
                    out2 = a['href'].replace("/port/","")
                    if not search(substring1, out2):
                        if not search(substring2, out2):
                            if not search(substring3, out2):
                                out2 = out2[:- 3]
                                out2 = out2.replace("_", " ")
                                cursor = conn.cursor()
                                result = cursor.execute('SELECT id FROM countries WHERE name = ?', [out])
                                rows = result.fetchone()
                                c_id = rows[0]
                                conn.execute("INSERT INTO ports(name, country_id) VALUES (?, ?)",[out2, c_id])
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
    conn.close()
    return render_template('scrape.html', countries=countries)

@app.route("/country/<id>")
def country(id):
    conn = get_db_connection()
    country = conn.execute('SELECT * FROM ports WHERE country_id = ?', [id]).fetchall()
    print(country)
    conn.close()

    return render_template("country.html", country=country)

@app.route("/port/<int:id>")
def port(id):
    conn = get_db_connection()
    port = conn.execute('SELECT * FROM ports WHERE id = ?',[id])
    conn.close()
    return render_template("port.html", port=port)
