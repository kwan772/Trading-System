import os
import time

import sqlalchemy
from finnhub import FinnhubAPIException
from sqlalchemy import create_engine, Column, Integer, String, Text
from data_engine.db.base import Base
from sqlalchemy.orm import sessionmaker
from data_engine.model import Symbol
from data_engine.stock_api_fetcher import MarketStack, Fmp, Finnhub
from sqlalchemy.inspection import inspect


from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound


def add_or_update_symbol(session: Session, symbol_instance: Symbol):
    """
    Adds a Symbol instance to the session if a matching record does not exist.
    Updates all attributes of the Symbol instance if it already exists in the database.
    Assumes that 'symbol_name' is a unique identifier for Symbol instances.

    :param session: SQLAlchemy Session
    :param symbol_instance: An instance of the Symbol model
    """
    try:
        # Try to find an existing symbol
        existing_symbol = session.query(Symbol).filter_by(symbol=symbol_instance.symbol).one()

        # Update all attributes
        for attr, value in inspect(symbol_instance).attrs.items():
            if attr == "prices":
                continue
            setattr(existing_symbol, attr, value.value)

        session.commit()
        return existing_symbol

    except NoResultFound:
        # If not found, add a new symbol
        session.add(symbol_instance)
        session.commit()
        return symbol_instance

def categorize_market_cap(market_cap):
    if market_cap >= 100_000_000_000:
        return "Mega Cap"
    elif market_cap >= 10_000_000_000:
        return "Large Cap"
    elif market_cap >= 2_000_000_000:
        return "Mid Cap"
    elif market_cap >= 300_000_000:
        return "Small Cap"
    elif market_cap >= 50_000_000:
        return "Micro Cap"
    else:
        return "Nano Cap"


if __name__ == '__main__':
    # Define the base class
    engine = create_engine(f'mysql+pymysql://root:{os.getenv("DB_PASSWORD")}@localhost/quant_trading')

    # Create all tables in the engine (this is equivalent to "Create Table" in SQL)
    Base.metadata.create_all(engine)

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    marketstack = MarketStack()
    fmp = Fmp()
    finnhub = Finnhub()

    tickers = fmp.get_stock__list()
    failed_symbols = {}

    company_profile = finnhub.get_stock_info("MSFT")
    print(company_profile)

    company_profile = finnhub.get_stock_info("TSLA")
    print(company_profile)

    company_profile = finnhub.get_stock_info("U")
    print(company_profile)

    company_profile = finnhub.get_stock_info("NVTS")
    print(company_profile)

    for ticker in tickers:
        if ticker['exchangeShortName'] in ["NASDAQ", "NYSE"] and ticker['type'] == "stock":
            try:
                company_profile = finnhub.get_stock_info(ticker['symbol'])
                symbol = Symbol(ticker['name'], ticker['symbol'], ticker['exchange'], ticker['exchangeShortName'], None, company_profile['finnhubIndustry'], None, "finnhub")
                symbol.market_cap_category = categorize_market_cap(company_profile['marketCapitalization'] * 1_000_000)
                if symbol.symbol is not None:
                    added_symbol = add_or_update_symbol(session, symbol)
                print(added_symbol)
            except Exception as e:
                failed_symbols[ticker['symbol']] = e
                print(e)
                if isinstance(e, FinnhubAPIException) and e.status_code == 429:
                    # If it's a FinnhubAPIException with a status code of 429
                    time.sleep(60)

    # Close the session
    session.close()
