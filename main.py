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


def get_trending(url, api_key):
    response = requests.get(url.format(api_key))
    data = response.json()['most_actively_traded']
    return data


def get_tickers(data):
    return [i['ticker'] for i in data]


def get_ticker_news(url, api_key, ticker):
    response = requests.get(url.format(ticker, api_key)).json()
    return response


# Todo: Write ticker data to daily_tick.db (sqlite3)
# Todo: get ticker name before writing it to the trending_ticker table
# Todo: Update trending_ticker table name to trending_tickers
# Todo: update trending_tickers table to add column 'repeat integer' to count the number of repetitions of the ticker in the same day in most trending
# Todo: get the whole volume of stock available for a ticker to calculate trade_volume/total_volume to get the percentage of trade volume >>> yf.Ticker("AAPL").info['volume']
# Todo: schedule this to run once every 2 mins from 9:31 AM to 10:30 AM
# Todo: Send email with the ticker and relevant news at 10:31 AM


def get_ticker_info():
    pass


def gather_info():
    pass


def send_email():
    pass


def update_ticker_name(ticker_data):
    for ticker in ticker_data:
        ticker_name = yf.Ticker(ticker['ticker']).info['shortName']
        ticker.update({'ticker_name': ticker_name})
    return ticker_data


def convert_to_num(ticker_data):
    columns = ['change_percentage', 'change_amount', 'volume', 'price']
    for ticker in ticker_data:
        for col in columns:
            if ticker[col][-1] == '%':
                ticker[col] = ticker[col][:-1]
            ticker[col] = float(ticker[col])
    return ticker_data


def main():
    api_key = os.environ.get('ALPHAVANTAGE_FREE_APIKEY')

    config = get_config(ABS_CONFIG_PATH)

    stock_api = config['alphavantage']['stock_api']
    news_api = config['alphavantage']['news_api']

    trending_ticker_data = get_trending(stock_api, api_key)
    trending_ticker_data = update_ticker_name(trending_ticker_data)
    trending_ticker_data = convert_to_num(trending_ticker_data)

    sorted_ticker_data = sorted(
        trending_ticker_data, key=lambda x: x['change_percentage'], reverse=True)

    tickers = [i['ticker'] for i in sorted_ticker_data]

    for ticker in tickers:
        news = get_ticker_news(news_api, api_key, ticker['ticker'])

    db_name = 'daily_tick.db'

    cnx = sqlite3.connect(db_name)

    df_db = pd.read_sql_query("SELECT * FROM trending_ticker;", cnx)

    cnx.close()

    pprint(df_db.head())


if __name__ == '__main__':
    main()
