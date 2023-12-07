import os
import requests
from data_fetcher import MarketStack




if __name__ == '__main__':
    marketstack = MarketStack()
    data = marketstack.get_end_of_year_data('2020-11-11','2023-11-15','aapl')

    for stock_data in data:
        print(stock_data)

