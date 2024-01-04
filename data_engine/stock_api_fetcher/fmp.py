import requests


class Fmp:
    def get_stock_data(self, symbol, start_date, end_date):
        pass

    def get_stock__list(self):
        response = requests.get("https://financialmodelingprep.com/api/v3/stock/list?apikey=Vd9ssubiPDeQ3leyYb6xH9ZlOq5knw4v")
        return response.json()