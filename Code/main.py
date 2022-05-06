from flask import Flask

app = Flask(__name__)

@app.route("/")
def heading_number_one():
    return "<h1> Sea Rates Scraper </h1>"
