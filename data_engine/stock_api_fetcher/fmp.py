import pprint

import requests
import os
from datetime import datetime, timedelta

import requests

from data_engine.model import Symbol
from data_engine.model.HistoricalPrice import HistoricalPrice


class Fmp:
    def __init__(self):
        self.API_KEY = os.getenv('FMP_API_KEY')
        self.BASE_URL = 'https://financialmodelingprep.com/api/v3/'

    def format_datetime_for_mysql(self, dt):
        return datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

    def get_price_data(self, start, end, symbol):
        end_day = datetime.strptime(start, "%Y-%m-%d").date()
        last_day = datetime.strptime(end, "%Y-%m-%d").date()
        data = []
        repeat_day_count = 0

        while last_day >= end_day:
            params = {
                'apikey': self.API_KEY,
                'from': start,
                'to': end,
            }

            result = requests.get(self.BASE_URL + "historical-chart/1min/" + symbol, params)
            response = result.json()
            print(params)
            # pprint.pprint(response)
            try:
                last_day = datetime.strptime(response[-1]['date'], "%Y-%m-%d %H:%M:%S").date()
            except Exception as e:
                print(e)
                print(response)
                raise e
            print(f"{symbol} fetched -> start date {start}")

            if last_day == end:
                repeat_day_count += 1

            if repeat_day_count > 3:
                raise Exception("Repeated day count exceeded 5")

            if end == end_day:
                end = end - timedelta(days=1)
            else:
                end = last_day

            for price in response:
                data.append(
                    HistoricalPrice(symbol, self.format_datetime_for_mysql(price['date']), price['open'], price['high'],
                                    price['low'],
                                    price['close'], price['volume'], None))
            print(f"end date: {last_day}")
        return data