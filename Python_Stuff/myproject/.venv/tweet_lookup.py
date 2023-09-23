import requests
import json
import datetime
import pytz
from datetime import timedelta, timezone
from translate import Translator

f = open('keys.json')
file_data = json.load(f)
bearer_token = file_data['bearer_token']
utc = pytz.UTC

# def past(stock, result_number, date, x):
#     day = 5 - x
#     end_time = (datetime.datetime.utcnow() - timedelta(days=day)).strftime("%Y-%m-%dT%H:%M:%SZ")
#     print(end_time)
#     return "https://api.twitter.com/2/tweets/search/recent?query={topic}&max_results={results}&start_time={time}&end_time={endtime}".format(topic=stock, results = result_number, time = date, endtime= end_time)

def today(stock, result_number, date):
    start_time = (datetime.datetime.utcnow() - timedelta(seconds=15)).strftime("%Y-%m-%dT%H:%M:%SZ")
    # print(start_time)
    return "https://api.twitter.com/2/tweets/search/recent?query={topic}&max_results={results}&start_time={time}&end_time={endtime}".format(topic=stock, results = result_number, time = date, endtime= start_time)


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld

    return {"tweet.fields": "lang,created_at"}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main(query, result_number, date):
    url_today = today(query, result_number, date)
    params = get_params()

    json_response_today = connect_to_endpoint(url_today, params)

    testing = []

    for x in json_response_today['data']:
        if x['lang'] == 'en':
            testing.append([x['text'], x['created_at']])
 
    # for x in json_response_past['data']:
    #     if x['lang'] == 'en':
    #         training.append([x['text'], x['created_at']])
    #         training.append(x['text'])



    # print(training)
    # print("--------------------")
    # print(testing)

    return testing

if __name__ == "__main__":
    date = (datetime.datetime.utcnow() - timedelta(days=6)).strftime("%Y-%m-%dT%H:%M:%SZ")
    main("AAPL", 10, date)
