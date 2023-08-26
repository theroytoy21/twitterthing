from sklearn import *
from sklearn import svm
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
    v = TfidfVectorizer()
    # input_data = v.fit_transform(past_tweets)
    input_data = v.fit_transform(training['tweets'])

    # 0 = bad, 1 = good; average polarity goes here
    # output_data = [0, 0, 1, 0, 1]
    output_data = training['score']
    model = svm.SVR()
    model.fit(input_data, output_data)

    x = v.transform(testing['tweets'])
    # print(model.predict(x))
    return model.predict(x).tolist()

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
    print(clean_text)
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

def format_to_csv():
    today = datetime.datetime.now()
    wk = today.weekday()

    if wk != 6:
        print("Error")

    list = []
    for ticker in stocks.keys():
        list.append(get_stock_info(ticker))
    # print(list)
    newlist = pd.concat(list)
    newlist.to_csv("stock_file.csv", mode='a', index=False, header=False)

def format_data(stockCSV):
    file = pd.read_csv(stockCSV)
    list = []

    for index, row in file.iterrows():
        list.append([row['Date'], row['Open'], row['ticker']])
    print(list)
    return list

def prediction_data(list, score):
    # input = [ticker name, sentiment]
    # output = [price]
    input = []
    output = []
    input.append([list[0][2], score])
    print(input)
    output.append(list[0][1])
    print(output)

date = (datetime.datetime.utcnow() - timedelta(days=6)).strftime("%Y-%m-%dT%H:%M:%SZ")
ticker = "AAPL"
tweet_list = main(ticker, 10, date)

training = []
testing = []
count = 0

for x in tweet_list:
    if count == 0:
        training = sentiment(ticker, 100, x)
        count += 1
    else:
        testing = sentiment(ticker, 100, x)

print("Training\n", training)
print("---------------")
print("Testing\n", testing)
print("---------------")

# print(get_stock_info("AAPL"))
# print(stock_info("AAPL"))
format_to_csv()
prediction_data(format_data("stock_file.csv"), training['average sentiment'])