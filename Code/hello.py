from flask import Flask, render_template, redirect, url_for
import datetime
import sqlite3

app = Flask(__name__)

import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn



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

@app.route("/country/<int:id>")
def country(id):
    conn = get_db_connection()
    country = conn.execute('SELECT * FROM ports WHERE country_id = ?',[id]).fetchall()
    conn.close()
    return render_template("country.html", country=country)

@app.route("/port/<int:id>")
def port(id):
    conn = get_db_connection()
    port = conn.execute('SELECT * FROM ports WHERE id = ?',[id])
    conn.close()
    return render_template("port.html", port=port)
