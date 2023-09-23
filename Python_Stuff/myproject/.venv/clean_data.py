import pandas as pd

def get_file_data(tweetCSV, stockCSV):
    tweets = pd.read_csv(tweetCSV)
    tweets_list = []

    for index, row in tweets.iterrows():
        if row['start'] != 4 and row['start'] != 5:
            tweets_list.append([row['start'], row['tweet_count'], row['ticker']])
    
    stocks = pd.read_csv(stockCSV)
    stock_list = []
    for index, row in stocks.iterrows():
        stock_list.append([row['Date'], row['Open'], row['ticker']])

    return clean_data(stock_list, tweets_list)
                          
def clean_data(stocks, tweets):
    input_data = []
    output_data = []
    i = 0
    ticker = tweets[0][2] #AAPL
    tickerNum = 0 #STARTING NUMBER
    for tweet in tweets[:-1]:
        try:
            if ticker != stocks[i+1][2]: #AAPL != newTicker
                ticker = stocks[i+1][2]
                tickerNum += 1
                i += 1
                continue
        except:
            pass
        point = [tweet[1],stocks[i][1], tickerNum]
        
        try:
            output_data.append(stocks[i+1][1])
            input_data.append(point)
            i += 1
        except:
            continue

    return input_data, output_data