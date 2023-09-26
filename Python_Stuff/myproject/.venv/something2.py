from get_info import get_stock_info, fetch_tweets
import pandas as pd
from stocks import stocks, check_exist
from ai import predict
from convert_csv import update
from firebase_admin import credentials, initialize_app, firestore
import datetime as datetime
import json
from something import sentiment_calc

cred = credentials.Certificate("fbkey.json")
initialize_app(cred, {'storageBucket': 'pizza-41ca7.appspot.com'})
db = firestore.client()

def search(name):
    x = check_exist(name)
    return f'{x}'

def prediction(name):
    ticker_num = stocks[name.upper()]
    twitter_data = pd.read_csv('sentiment.csv', header=0)
    likes = twitter_data[twitter_data['stock_num'] == ticker_num].tail(1)['likes'].values[0]
    sentiment = twitter_data[twitter_data['stock_num'] == ticker_num].tail(1)['sentiment'].values[0]
    info = get_stock_info(name).drop(columns=['ticker'])
    info = info.values.tolist()
    data = [ticker_num, likes, sentiment, info[-1][0]]
    prediction = predict(data)

    return prediction

def update_info(ticker):
    update(ticker)

def driver(ticker):
    print(sentiment_calc(ticker))
    print(prediction(ticker))

    file_to_send = {'Ticker': ticker,
                    'Prediction': '$' + str(prediction(ticker)),
                    'Date': datetime.datetime.now() 
                    }
    
    # print(file_to_send)
    db.collection("Prediction Data").document(str(ticker).upper()).set(file_to_send)
    
driver("NVDA")
