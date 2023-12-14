import os

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.dialects.mysql import insert
from data_engine.db.base import Base
from sqlalchemy.orm import sessionmaker
from data_engine.model import Symbol
from data_engine.model.HistoricalPrice import HistoricalPrice
from data_engine.stock_api_fetcher import MarketStack


from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

def insert_historical_price_data(historical_prices, session):
    # Extract data from HistoricalPrice objects
    data_to_insert = [{
        'symbol': price_data.symbol,
        'datetime': price_data.datetime,
        'open': price_data.open,
        'high': price_data.high,
        'low': price_data.low,
        'close': price_data.close,
        'volume': price_data.volume,
        'adj_open': price_data.adj_open,
        'adj_high': price_data.adj_high,
        'adj_low': price_data.adj_low,
        'adj_close': price_data.adj_close,
        'adj_volume': price_data.adj_volume,
        'split_factor': price_data.split_factor,
        'dividend': price_data.dividend
    } for price_data in historical_prices]

    try:
        # Perform a bulk insert
        session.bulk_insert_mappings(HistoricalPrice, data_to_insert)
        session.commit()
    except Exception as e:
        session.rollback()
        # If a duplicate key error occurs, handle it with an update
        for data in data_to_insert:
            stmt = insert(HistoricalPrice).values(data)
            update_dict = {k: v for k, v in data.items() if k not in ['symbol', 'datetime']}
            upsert_stmt = stmt.on_duplicate_key_update(update_dict)
            session.execute(upsert_stmt)
        session.commit()

    print(f"Prices have been updated.")


if __name__ == '__main__':
    # Define the base class
    engine = create_engine(f'mysql+pymysql://root:{os.getenv("DB_PASSWORD")}@localhost/quant_trading')

    # Create all tables in the engine (this is equivalent to "Create Table" in SQL)
    Base.metadata.create_all(engine)

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    marketstack = MarketStack()

    symbols = session.query(Symbol).all()
    for symbol in symbols:
        historical_prices = marketstack.get_price_data('2022-12-21','2023-11-15',symbol)
        print(historical_prices)
        insert_historical_price_data(historical_prices, session)
        break

    # Close the session
    session.close()
