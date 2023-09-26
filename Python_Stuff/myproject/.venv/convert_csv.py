from get_info import get_stock_info, fetch_tweets
import pandas as pd
from datetime import datetime
from stocks import check_exist, stocks

def update(ticker):
    dt = datetime.now()
    day = dt.weekday()

    if day != 6:
        print("Something wong?")

    list = []
    list.append(get_stock_info(ticker))
    z = pd.concat(list)
    z.to_csv('stock_file.csv', mode='a', index=False, header=False)

    list = []
    list.append(fetch_tweets(ticker))
    z = pd.concat(list)
    z.to_csv('tweets.csv', mode='a', index=False, header=False)
