import pprint

from backtesting.searcher import Searcher
from data_engine.db.db_connection import DbConnection
from data_engine.model import Symbol


class Simulator:
    def __init__(self, Searcher):
        self.stats = {}
        self.searcher = Searcher(self.stats)
        self.conn = DbConnection()
        self.conn.connect()

    def _run(self):

        # Get all the symbols from the database
        symbols = self.conn.session.query(Symbol).filter(Symbol.data_status == "complete").all()

        for symbol in symbols:
            # Get the historical prices for the symbol
            historical_prices = symbol.prices
            self.searcher.search(symbol, historical_prices)

    def _report(self):
        pprint.pprint(self.stats)
    def run(self):
        self._run()
        self._report()