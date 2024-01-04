import os
from datetime import datetime, timedelta

import requests

from data_engine.model import Symbol
from data_engine.model.HistoricalPrice import HistoricalPrice


class MarketStack:

    def __init__(self):
        self.API_KEY = os.getenv('MARKETSTACK_API_KEY')
        self.BASE_URL = 'https://api.marketstack.com/v1/'

    def format_datetime_for_mysql(self, dt_str):
        # Parse the datetime string and reformat it
        dt_format = "%Y-%m-%dT%H:%M:%S%z"
        converted_datetime = datetime.strptime(dt_str, dt_format)
        mysql_format = "%Y-%m-%d %H:%M:%S"
        return converted_datetime.strftime(mysql_format)

    def get_price_data(self, start, end, symbol, price_type="eod"):
        last_day = datetime.strptime(start, "%Y-%m-%d").date()
        end_day = datetime.strptime(end, "%Y-%m-%d").date()
        data = []

        while last_day <= end_day:

            params = {
                'access_key': self.API_KEY,
                'symbols': symbol.symbol,
                'limit': 1000,
                'date_from': start,
                'sort': 'ASC',
                'interval': '1min'
            }
            result = requests.get(self.BASE_URL + price_type, params)
            response = result.json()
            last_day = datetime.strptime(response['data'][-1]['date'], "%Y-%m-%dT%H:%M:%S%z").date()
            print(f"{symbol.symbol} fetched -> start date {start}")
            if start == end_day:
                start = start + timedelta(days=1)
            else:
                start = last_day

            for price in response['data']:
                data.append(HistoricalPrice(symbol.symbol, self.format_datetime_for_mysql(price['date']), price['open'], price['high'], price['low'],
                                            price['close'], price['volume'], price['last']))
            print(f"end date: {last_day}")
        return data

    def get_stock_info(self, symbol):
        params = {
            'access_key': self.API_KEY,
            'symbols': symbol
        }
        result = requests.get(self.BASE_URL + 'tickers', params)
        response = result.json()
        print(response)
        data = response['data'][0]
        symbol = Symbol(data['name'], data['symbol'], data['stock_exchange']['name'], data['stock_exchange']['acronym'],
                        data['stock_exchange']['country_code'] + ' / ' + data['stock_exchange']['city'], None, None)
        return symbol
