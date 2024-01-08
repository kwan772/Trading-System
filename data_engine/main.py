import os
import requests
from stock_api_fetcher import MarketStack, Fmp




if __name__ == '__main__':
    fmp = Fmp()
    data = fmp.get_price_data('2023-12-22','2024-01-04','AAPL')

    for stock_data in data:
        print(stock_data)

