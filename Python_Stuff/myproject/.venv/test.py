import requests
import json
from datetime import timedelta,datetime,date
from requests.structures import CaseInsensitiveDict

#define search twitter function
def search_twitter(crypto,bearer_token,start_date,max_results = '100'):
  f = open('keys.json')
  file_data = json.load(f)
  bearer_token = file_data['bearer_token']
  
  headers = CaseInsensitiveDict()
  headers["Authorization"] = bearer_token
  end_date = str(datetime.today())[:10]+'T00:00:00Z'
  # print(end_date)
  start_date  +='T00:00:00Z'
  # print(start_date)
  # print(end_dat
  r = requests.get('https://api.twitter.com/2/tweets/search/recent?query=%23' +
                   crypto+'&max_results='+max_results+'&start_time='+start_date+'&end_time='+end_date+'&tweet.fields=lang,created_at',
                   headers=headers)

  tweets = []
  if r.status_code == 200:
    res = r.json()
    print(res)
    if 'data' in res:
      for record in res['data']:
        # print(record)
        if record['lang'] == 'en':
          tweets.append(record['text'])
  return tweets