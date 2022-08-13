from flask import Flask, render_template, request
import pandas as pd
from db import add_data
from db import add_data, get_data, get_Item_Country, getRangeData

app = Flask(__name__)

isDataLoaded = False;

# Data Source
URL = "https://projects.fivethirtyeight.com/soccer-api/international/spi_global_rankings_intl.csv";

def loadDataFromURL():
    df = pd.read_csv(URL)
    add_data(df)

# main page
@app.route("/")
def askForData():
    return render_template('home.html')


# to fetch data
@app.route("/getData")
def getData():
    data = get_data()
    return { "data": [
        {"rank": ent['rankteam'], "team": ent['team'], "spi": ent['spi'], "off": ent['offe'], "def": ent['def'], "confed": ent['confed']}
        for ent in data
    ]}

# to fetch data by country
@app.route("/getItemByCountry")
def getItemByCountry():
    countryName = request.args.get('country', default = "Brazil", type = str)
    data = get_Item_Country(countryName)
    return { "data": data}

# to fetch data by range
@app.route("/getRangeItems")
def getItemByRange():
    minValue = request.args.get('min', default = 0, type = int)
    maxValue = request.args.get('max', default = minValue+10, type = int)
    data = getRangeData(minValue, maxValue)
    return { "data": data }

# to show add data page
@app.route("/addData")
def index():
    return render_template('index.html')

# to load data from URL and then to add to db
@app.route("/loadData")
def loadData():
    if isDataLoaded:
        return;
    else:
        loadDataFromURL()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
