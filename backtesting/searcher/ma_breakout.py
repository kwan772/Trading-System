from pprint import pprint
from datetime import datetime, timedelta

import pytz
from backtesting.searcher import Searcher

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class MaBreakout(Searcher):
    def __init__(self, stats):
        super().__init__(stats)

    def search(self, symbol, data):
        # Assuming your current timezone is 'Pacific/Auckland'
        # and you want to convert to 'America/New_York'
        # self.status[symbol.symbol] = self.analyze_data(data)
        self.analyze_data(self.process_data(data))

    def process_data(self, historical_prices):
        sorted_data = sorted(historical_prices, key=lambda x: x.datetime)
        grouped_data = {}
        for d in sorted_data:
            converted_time = self.convert_timezone(d.datetime, 'UTC', 'America/New_York')
            d.datetime = converted_time
            if 9 <= d.datetime.hour <= 16:
                if 9 != d.datetime.hour or d.datetime.minute >= 30:
                    date_key = d.datetime.date().strftime("%Y-%m-%d")
                    grouped_data.setdefault(date_key, []).append(d)
        # df = pd.DataFrame(grouped_data)

        # Flattening the dictionary into a list of tuples
        data = []
        for date, prices in grouped_data.items():
            for price in prices:
                data.append(
                    (date, price.symbol, price.datetime, price.open, price.high, price.low, price.close, price.volume))

        # Creating a DataFrame
        df = pd.DataFrame(data, columns=['Date', 'Symbol', 'DateTime', 'Open', 'High', 'Low', 'Close', 'Volume'])
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        df.set_index('Date', inplace=True)
        # Replace NaN values in 'Close' with the average of 'High', 'Low', and 'Open'
        # df['Close'] = df.apply(
        #     lambda row: np.mean([row['High'], row['Low'], row['Open']]) if np.isnan(row['Close']) else row['Close'],
        #     axis=1
        # )
        # df['200_MA'] = df['Close'].rolling(window=200).mean()
        return df
    def convert_timezone(self, utc_time, from_zone, to_zone):
        from_zone = pytz.timezone(from_zone)
        to_zone = pytz.timezone(to_zone)

        utc = from_zone.localize(utc_time)
        return utc.astimezone(to_zone)

    def analyze_data(self, historical_prices):
        for date in historical_prices:
            print(date)