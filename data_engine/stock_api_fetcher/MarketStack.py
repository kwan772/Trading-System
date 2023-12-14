import os
from datetime import datetime, timedelta

import requests


class MarketStack:

    def __init__(self):
        self.API_KEY = os.getenv('MARKETSTACK_API_KEY');

    def get_end_of_year_data(self, start, end, symbol):
        last_day = datetime.strptime(start, "%Y-%m-%d").date()
        end_day = datetime.strptime(end, "%Y-%m-%d").date()
        eod = []

        if end_day.weekday() >= 5:
            end_day -= timedelta(days=end_day.weekday()-4)

        while last_day < end_day:

            params = {
                'access_key': self.API_KEY,
                'symbols': 'aapl',
                'limit': 1000,
                'date_from': start,
                'sort': 'ASC'
            }
            result = requests.get('http://api.marketstack.com/v1/eod', params)
            response = result.json()
            last_day = datetime.strptime(response['data'][-1]['date'], "%Y-%m-%dT%H:%M:%S%z").date()
            start = last_day + timedelta(days=1)
            eod.extend(response['data'])

            for i in range(len(eod)-1, -1, -1):
                if datetime.strptime(eod[i]['date'], "%Y-%m-%dT%H:%M:%S%z").date() > end_day:
                    eod.pop(i)
        return eod