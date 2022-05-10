from flask import Flask, render_template, redirect, url_for
from flask import send_file
from bs4 import BeautifulSoup
import pathlib
import requests
import sqlite3
import pandas as pd
app = Flask(__name__)




#database connection estabilishment
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn




#landing page
@app.route("/")
def index():
    return render_template('index.html')

#list of countries page
@app.route("/scrape")
def scrape():
    #get db connection
    conn = get_db_connection()
    #get all countries in DB
    countries = conn.execute('SELECT * FROM countries').fetchall()
    #render template for list of countries, returning list of countries as param
    return render_template('scrape.html', countries=countries)
    conn.close()

#list of ports page, getting id via url_for for dynamic content
@app.route("/country/<id>")
def country(id):
    conn = get_db_connection()
    #selecting all ports based on country given by param of function
    country = conn.execute('SELECT * FROM ports WHERE country_id = ?', [id]).fetchall()
    return render_template("country.html", country=country)
    conn.close()

#table of data about port, dynamicaly managed by id given via url_for
@app.route("/port/<int:id>")
def port(id):
    conn = get_db_connection()
    #selecting all data from port based on port id given by param of function
    port = conn.execute('SELECT * FROM ports WHERE id = ?', [id]).fetchall()
    return render_template("port.html", port=port)
    conn.close()

@app.route("/download")
def download():
    conn = sqlite3.connect('database.db', isolation_level=None,
                           detect_types=sqlite3.PARSE_COLNAMES)
    db_df = pd.read_sql_query("SELECT * FROM countries JOIN ports ON countries.id = ports.country_id", conn)
    db_df.to_csv('database.csv', index=False)
    dir = str(pathlib.Path().resolve())
    path = dir+"/database.csv"
    return send_file(path, as_attachment=True)
    #return render_template('index.html')
