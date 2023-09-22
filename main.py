import os
import json

from pprint import pprint

import requests
# from requests.auth import HTTPBasicAuth

URL = "https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={}"
JSONFILE = "config.json"
TO_EMAILS = ["gautham.kolluru@gmail.com"]
FROM_EMAILS = ["gautham.kolluru@gmail.com"]

abs_json_path = os.path.join(os.path.abspath('.'), JSONFILE)

with open(abs_json_path) as jsp:
  config = json.load(jsp)

# auth = HTTPBasicAuth('apiKey', config['api_key'])


def get_trending(url, apikey):
	response = requests.get(url.format(apikey))
	data = response.json()['most_actively_traded']
	return data

pprint(get_trending(URL, config['api_key']))


def get_ticker_info():
	pass

def get_ticker_news():
	pass

def gather_info():
	pass

def send_email():
	pass



