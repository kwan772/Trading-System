import os

import finnhub
class Finnhub:
    def __init__(self):
        self.api_key = os.getenv("FINNHUB_API_KEY")

    def get_stock_data(self, symbol, start_date, end_date):
        pass

    def get_stock_info(self, symbol):
        finnhub_client = finnhub.Client(api_key=self.api_key)
        res = finnhub_client.company_profile2(symbol=symbol)
        return res
