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

def sentiment(list):
    # tweets = search_tweets(query, result_number)

    pos = 0
    neutral = 0
    neg = 0
    scores = []
 
    for tweet in list:
        polarity = TextBlob(tweet[0]).sentiment.polarity
        scores.append(polarity)

        if polarity < 0:
            neg += 1
        elif polarity > 0:
            pos += 1
        else:
            neutral += 1


    avg_sentiment = sum(scores) / len(scores)
    return {'positive score': pos, 'negative score': neg, "neutral score": neutral, 'average sentiment': avg_sentiment, 'tweets': list, 'score': scores}


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


def ml_data(list, score, ticker, today):
    input = []
    output = []
    for x in list:
        if x[2] == ticker and int(x[0]) != int(today):
            input.append(score)
            output.append(x[1])
    return [input, output]


def testing_data(list, score, ticker, today):
    input = []
   
    for x in list:
        if x[2] == ticker and int(x[0]) == int(today):
            input.append(score)
    # print(input[1])
    # print(output[1])

    return input

def sentiment_calc(ticker):
    date = (datetime.datetime.utcnow() - timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
    testing = []
    num_of_tweets = 10
    # ticker_list = save_sp500_tickers()
    list = []
    # print("---------------")
    # print(ticker_list)
    # print("---------------")

    # ticker = input("Please select a valid ticker. ")

    tweet_list = main(ticker, num_of_tweets, date)
    for y in tweet_list:
        testing.append(sentiment(y))

    list = testing[0]
    # print(list['average sentiment'])
    return list['average sentiment']
