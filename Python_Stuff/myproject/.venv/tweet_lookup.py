import requests
import json

f = open('keys.json')
file_data = json.load(f)
# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = file_data['bearer_token']


def create_url(stock, result_number):
    return "https://api.twitter.com/2/tweets/search/recent?query={topic}&max_results={results}".format(topic=stock, results = result_number)


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld

    return {"tweet.fields": "lang"}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main(query, result_number):
    url = create_url(query, result_number)
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    newlist = []
    for x in json_response['data']:
        if x['lang'] == 'en':
            newlist.append(x['text'])
    print(json.dumps(newlist, indent=4, sort_keys=True))
    return newlist

if __name__ == "__main__":
    main()