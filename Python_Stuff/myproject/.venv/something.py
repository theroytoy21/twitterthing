from sklearn import *
from sklearn import ensemble
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
import requests
import pandas as pd
from nltk.tokenize import TweetTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
import re
import yfinance as yf
import datetime
import json
from tweet_lookup import main
from requests.structures import CaseInsensitiveDict
from datetime import timedelta
from esg_info import save_sp500_tickers
from stocks import stocks
# nltk.download('wordnet')
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('omw-1.4')

f = open('keys.json')
file_data = json.load(f)
bearer_token = file_data['bearer_token']

today = datetime.datetime.today()
stop_words = nltk.corpus.stopwords.words(['english'])
lem = WordNetLemmatizer()

def twitter(query, result_number):
    return tweet_list

def predictions(training, testing):
    print(training[0])
    print(training[1])
    model = ensemble.RandomForestRegressor()
    model.fit([training[0]], [training[1]])
    print(model.predict([testing]))

def cleaning(data):
    no_url = re.sub(r'https\S+', ' ', data)
    no_hashtags = re.sub(r'#\w+', ' ', no_url)
    no_mentions = re.sub(r'@\w+', ' ', no_hashtags)
    no_mentions = re.sub(r'&amp', ' ', no_mentions)

    semi_clean_tweet = re.sub('[A-Za-z]+', ' ', no_mentions)

    tweet_token = TweetTokenizer().tokenize(semi_clean_tweet)
    no_punc = [w for w in tweet_token if w.isalnum()]
    no_stopwords = [t for t in no_punc if t not in stop_words]
    clean_text = [lem.lemmatize(t) for t in no_stopwords]
    return " ".join(clean_text)

def clean_tweets(tweets):
    cleaned_tweets = []
    for tweet in tweets:
        cleaned_tweets.append(cleaning(tweet))
    return cleaned_tweets

def search_tweets(query, result_number):
    tweets = twitter(query, result_number)
    tweets = clean_tweets(tweets)
    return tweets

def sentiment(query, result_number, list):
    # tweets = search_tweets(query, result_number)

    pos = 0
    neutral = 0
    neg = 0
    scores = []

    for tweet in list:
        polarity = TextBlob(tweet).sentiment.polarity
      
        scores.append(polarity)

        if polarity < 0:
            neg += 1
        elif polarity > 0:
            pos += 1
        else:
            neutral += 1

    avg_sentiment = sum(scores) / len(scores)
    return {'positive score': pos, 'negative score': neg, "neutral score": neutral, 'average sentiment': avg_sentiment, 'tweets': list, 'score': scores}

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
    # print(info.head().index)
    
    for i in info.head().index:
        y, m, d = str(i).split('-')
        d = d.split()[0]
        dt = datetime.datetime(int(y), int(m), int(d))
        dList.append(dt.weekday())
        dintList.append(dt.year * 10000 + dt.month * 100 + dt.day)

    # print(dList)
    info['Date'] = dList
    info['DateInt'] = dintList
    info.drop(index=info.index[0], axis = 0, inplace = True)
    return info

def stock_info(ticker):
    info = get_stock_info(ticker).drop(columns=['ticker'])
    info = info.values.tolist()
    return info

def format_to_csv(ticker_list):
    today = datetime.datetime.now()
    wk = today.weekday()

    if wk != 6:
        print("Error")

    list = []
    failed_tickers = []
    for ticker in ticker_list:
        try:
            list.append(get_stock_info(ticker))
        except:
            failed_tickers.append(ticker)
            print("Ticker has no data: ", ticker)
    newlist = pd.concat(list)
    newlist.to_csv("stock_file.csv", mode='a', index=False, header=False)

def format_data(stockCSV):
    file = pd.read_csv(stockCSV)
    list = []

    for index, row in file.iterrows():
        list.append([row['DateInt'], row['High'], row['ticker']])
    # print(list)
    return list

def training_data(list, score, ticker, today):
    input = []
    output = []
    
    for x in list:
        if x[2] == ticker and int(x[0]) != int(today):
            input.append([x[2], score, x[0]])
            output.append(x[1])
    # print(input[1])
    # print(output[1])

    final_list = [input, output]
    return final_list

def testing_data(list, score, ticker, today):
    input = []
    
    for x in list:
        if x[2] == ticker and int(x[0]) == int(today):
            input.append([x[2], score])
    # print(input[1])
    # print(output[1])

    return input


date = (datetime.datetime.utcnow() - timedelta(days=6)).strftime("%Y-%m-%dT%H:%M:%SZ")
date2 = datetime.datetime.today().strftime('%Y%m%d')

ticker_list = save_sp500_tickers()
print("---------------")
print(ticker_list)
print("---------------")

ticker = input("Please select a valid ticker. ")

training = []
testing = []
count = 0
num_of_tweets = 100

# due to Twitter limitations, we cannot search every tweet found in the list of tickers at the same time

# for x in ticker_list:
#     tweet_list = main(x, 10, date)
#     print(x)
#     for y in tweet_list:
#         if len(y) == 0:
#             print("Insufficient tweets")
#             break
#         if count == 0:
#             training = sentiment(x, 10, y)
#             count += 1
#         else:
#             testing = sentiment(x, 10, y)
    
tweet_list = main(ticker, num_of_tweets, date)

for y in tweet_list:
    if len(y) == 0:
        print("Insufficient tweets")
        break
    if count == 0:
        training = sentiment(ticker, num_of_tweets, y)
        count += 1
    else:
        testing = sentiment(ticker, num_of_tweets, y)

# format_to_csv(ticker_list)
training_list = training_data(format_data("stock_file.csv"), training['average sentiment'], ticker, date2)
print(training_list)

print("---------------")

testing_list = testing_data(format_data("stock_file.csv"), testing['average sentiment'], ticker, date2)
print(testing_list)

predictions(training_list, testing_list)