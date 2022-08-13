import pandas as pd 


URL = "https://projects.fivethirtyeight.com/soccer-api/international/spi_global_rankings_intl.csv";

df = pd.read_csv(URL)

data = []

for index, row in df.iterrows():
    data.append({'team': row['name'], 'spi': row['spi']})