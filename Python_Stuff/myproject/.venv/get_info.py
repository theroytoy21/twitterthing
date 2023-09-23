import pandas as pd
import datetime
import requests
from tweet_lookup import main
import yfinance as yf
import json

def fetch_tweets(ticker):
    file = open("keys.json")
    data = json.load(file)

    bearer_token = data['bearer_token']
    headers = {"Authorization": 'Bearer ' + bearer_token}

    # r = the data/tweets
    r = requests.get(f'https://api.twitter.com/2/tweets/counts/recent?query={ticker}&granularity=day',
    headers=headers)
    print(r)
    r = r.json()['data']

    for i in r:
        dict = i
        dict['start'] = dict['start'][0:10]
        y, m, d = dict['start'].split('-')
        dt = datetime.datetime(int(y), int(m), int(d))
        dict['start'] = dt.weekday()
        dict['DateInt'] = (dt.year * 10000 + dt.month * 100 + dt.day)
        
    r[0]['tweet_count'] += r[-1]['tweet_count']
    r.pop(-1)
    a = pd.DataFrame(r)
    a = a.drop(columns=['end'])
    a['ticker'] = ticker

    return a

def get_stock_info(ticker):
    info = yf.download(tickers= ticker,
                       period ="1wk",
                       interval = "1d",
                       ignore_tz= True,
                       prepost=False)
   
    if(info.empty):
        raise Exception
    info = info.drop(columns = ['Volume', 'Adj Close'])
    info['ticker'] = ticker

    dList = []
    dintList = []
   
    for i in info.head().index:
        y, m, d = str(i).split('-')
        d = d.split()[0]
        dt = datetime.datetime(int(y), int(m), int(d))
        dList.append(dt.weekday())
        dintList.append(dt.year * 10000 + dt.month * 100 + dt.day)

    info['Date'] = dList
    info['DateInt'] = dintList
    info.drop(index=info.index[0], axis = 0, inplace = True)
    return info

