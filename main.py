import os
import json
import sqlite3

import pandas as pd

from pprint import pprint

import requests

import yfinance as yf

# from requests.auth import HTTPBasicAuth

JSONFILE = "config.json"
ABS_CONFIG_PATH = os.path.join(os.path.abspath('.'), JSONFILE)


def get_config(config_file):
    with open(file=config_file) as jsp:
        config = json.load(jsp)
    return config


config = get_config(ABS_CONFIG_PATH)

stock_api = config['api']['stock_api']
news_api = config['api']['news_api']

api_key = config['api']['api_key']


def get_trending(url, api_key):
    response = requests.get(url.format(api_key))
    data = response.json()['most_actively_traded']
    return data


data = get_trending(stock_api, api_key)


def get_tickers(data):
    return [i['ticker'] for i in data]


tickers = get_tickers(data=data)


def get_ticker_news(url, api_key, tickers):
    news = {}
    for ticker in tickers:
        response = requests.get(url.format(ticker, api_key))
        news.update({ticker: response.json()})
    return news


news = get_ticker_news(news_api, api_key, tickers)

db_name = 'daily_tick.db'

cnx = sqlite3.connect(db_name)

df = pd.read_sql_query("SELECT * FROM trending_ticker;", cnx)


cnx.close()

pprint(df.head())


# Todo: Write ticker data to daily_tick.db (sqlite3)
# Todo: get ticker name before writing it to the trending_ticker table
# Todo: Update trending_ticker table name to trending_tickers
# Todo: update trending_tickers table to add column 'repeat integer' to count the number of repetitions of the ticker in the same day in most trending
# Todo: get the whole volume of stock available for a ticker to calculate trade_volume/total_volume to get the percentage of trade volume >>> yf.Ticker("AAPL").info['volume']
# Todo: schedule this to run once every 2 mins from 9:31 AM to 10:30 AM
# Todo: Send email with the ticker and relevant news at 10:31 AM

# pprint(news)


def get_ticker_info():
    pass


def gather_info():
    pass


def send_email():
    pass
