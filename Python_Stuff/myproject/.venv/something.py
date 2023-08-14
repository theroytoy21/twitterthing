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

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('omw-1.4')
stop_words = nltk.corpus.stopwords.words(['english'])

lem = WordNetLemmatizer()

def twitter(query, result_number):
    return main(query, result_number)

def predictions(q, r):
    past_tweets = twitter(q, r)
    
    v = TfidfVectorizer()
    # input_data = v.fit_transform(past_tweets)
    input_data = v.fit_transform(past_tweets)
    # print(input_data)

    # 0 = bad, 1 = good; average polarity goes here
    # output_data = [0, 0, 1, 0, 1]
    output_data = past_tweets['score']

    model = svm.SVC()
    model.fit(input_data, output_data)

    current_tweets = ['The food tastes bad.','My mother said the food is the best']

    x = v.transform(current_tweets)
    print(model.predict(x))
    return model.predict(x).tolist()

def cleaning(data):
    print(data)
    no_url = re.sub(r'https\S+', ' ', data)
    print(no_url)
    no_hashtags = re.sub(r'#\w+', ' ', no_url)
    print(no_hashtags)
    no_mentions = re.sub(r'@\w+', ' ', no_hashtags)
    no_mentions = re.sub(r'&amp', ' ', no_mentions)

    print(no_mentions)

    semi_clean_tweet = re.sub('[A-Za-z]+', ' ', no_mentions)

    print(semi_clean_tweet)

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

def search_tweets(query, start_date):
    tweets = twitter(query)
    tweets = clean_tweets(tweets)
    return tweets

def sentiment(query, starting_date):
    tweets = search_tweets(query)

    pos = 0
    neutral = 0
    neg = 0
    scores = []

    for tweet in tweets:
        polarity = TextBlob(tweet).sentiment.polarity
        scores.append(polarity)
        if polarity < 0:
            neg += 1
        elif polarity > 0:
            pos += 1
        else:
            neutral += 1

    avg_sentiment = sum(scores) / len(scores)
    return {'positive score': pos, 'negative score': neg, "neutral score": neutral, 'average sentiment': avg_sentiment, 'tweets': tweets, 'score': scores}

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
    print(info)
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

print(predictions("AAPL", 100))