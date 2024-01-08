import pprint

import pytz

from backtesting.searcher import Searcher
import pandas as pd

class Gaps(Searcher):
    def __init__(self, stats):
        super().__init__(stats)

    def search(self, symbol, data):
        self.analyze_data(self.process_data(data))

    def process_data(self, historical_prices):
        data = []
        for price in historical_prices:
            data.append(
                (price.symbol, price.datetime, price.open, price.high, price.low, price.close, price.volume))

        # Creating a DataFrame
        df = pd.DataFrame(data, columns=['Symbol', 'DateTime', 'Open', 'High', 'Low', 'Close', 'Volume'])
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        df.sort_values(by=['DateTime'], inplace=True)
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
        if len(historical_prices) == 0:
            return

        lastDate = historical_prices.iloc[0]['DateTime'].date()

        for index, (idx, row) in enumerate(historical_prices.iterrows()):
            if row['DateTime'].date() != lastDate:
                print(row['DateTime'].date())
                lastDate = row['DateTime'].date()
