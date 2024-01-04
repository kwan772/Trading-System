import os

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Text
from data_engine.db.base import Base
from sqlalchemy.orm import sessionmaker
from data_engine.model import Symbol
from data_engine.stock_api_fetcher import MarketStack


from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

def add_if_not_exists(session: Session, symbol_instance: Symbol):
    """
    Adds a Symbol instance to the session if a matching record does not exist.
    Assumes that 'symbol_name' is a unique identifier for Symbol instances.

    :param session: SQLAlchemy Session
    :param symbol_instance: An instance of the Symbol model
    """
    try:
        existing_symbol = session.query(Symbol).filter_by(symbol=symbol_instance.name).one()
        print(f"Symbol with name {symbol_instance.name} already exists.")
        return existing_symbol
    except NoResultFound:
        session.add(symbol_instance)
        session.commit()
        print(f"Added new symbol with name {symbol_instance.name}.")
        return symbol_instance


if __name__ == '__main__':
    # Define the base class
    engine = create_engine(f'mysql+pymysql://root:{os.getenv("DB_PASSWORD")}@localhost/quant_trading')

    # Create all tables in the engine (this is equivalent to "Create Table" in SQL)
    Base.metadata.create_all(engine)

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    marketstack = MarketStack()



    tickers = {"high volatility": {"tech": ["NCTY", "EBIX"],
                             "real estate": ["WHLR"],
                             "shipment": ["OP"],
                             "biotech": ["AXLA", "BNOX", "GRCL"],
                             "healthcare": ["FEMY", "GRTS"],
                             "space": ["MNTS"]
                                   },
               "large cap": {"tech": ["MARA", "CVNA"],
                             "travel services": ["CCL"],
                             "auto manufacturers": ["XPEV"],
                             "energy": ["RIG"]},
               "mega cap": {"tech": ["TSLA", "META"]}
               }

    for market_cap in tickers:
        for industry in tickers[market_cap]:
            print(market_cap)
            for symbol in tickers[market_cap][industry]:
                print(industry)
                print(symbol)
                symbol = marketstack.get_stock_info(symbol)
                symbol.industry = industry
                symbol.market_cap_category = market_cap
                added_symbol = add_if_not_exists(session, symbol)

    # Close the session
    session.close()
