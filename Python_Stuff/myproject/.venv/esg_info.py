import requests
import json
import yfinance as yf
import bs4 as bs
import pickle

def esg_getter(ticker):
    response = requests.get("https://www.refinitiv.com/bin/esg/esgsearchresult?ricCode=" + ticker + ".O")
    data = data_pull(response)
    if data is not None:
        return data
    else:
        response = requests.get("https://www.refinitiv.com/bin/esg/esgsearchresult?ricCode=" + ticker)
        data = data_pull(response)
        if data is not None:
            return data_pull(response)
        else:
            response = requests.get("https://www.refinitiv.com/bin/esg/esgsearchresult?ricCode=" + ticker + ".K")
            return data_pull(response)

def data_pull(response):
    if response.status_code == 200:
        json_data = response.json()
        if "esgScore" in json_data:
            value = json_data["esgScore"]
            esg_value = value["TR.TRESG"]
            return esg_value["score"]
    return None

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker[:-1]
        tickers.append(ticker)     
    return tickers

sp_tickers = save_sp500_tickers()
for ticker in sp_tickers:
    print(ticker + ", " +  str(esg_getter(ticker)))