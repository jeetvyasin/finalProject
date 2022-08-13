from flask import Flask, render_template, request
import pandas as pd
from db import add_data
from db import add_data, get_data

app = Flask(__name__)

isDataLoaded = False;

PASSWORD ="Jeet13@90"
PUBLIC_IP_ADDRESS ="34.130.225.172"
DBNAME ="finalDB"
PROJECT_ID ="newagent-pmyw"
INSTANCE_NAME ="finalprojectdb"

URL = "https://projects.fivethirtyeight.com/soccer-api/international/spi_global_rankings_intl.csv";

def loadDataFromURL():
    df = pd.read_csv(URL)
    add_data(df)

@app.route("/")
def askForData():
    return render_template('home.html')


@app.route("/getData")
def getData():
    data = get_data()
    return { "data": [
        {"rank": ent['rankteam'], "team": ent['team'], "spi": ent['spi'], "off": ent['offe'], "def": ent['def'], "confed": ent['confed']}
        for ent in data
    ]}

@app.route("/addData")
def index():
    return render_template('index.html')

@app.route("/loadData")
def loadData():
    if isDataLoaded:
        return;
    else:
        loadDataFromURL()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
