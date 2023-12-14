import os

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from data_engine.model import Symbol

# Define the base class
Base = declarative_base()

engine = create_engine(f'mysql+pymysql://root:{os.getenv("DB_PASSWORD")}@localhost/quant_trading_data')

# Create all tables in the engine (this is equivalent to "Create Table" in SQL)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Example: Insert a new record into the table
new_symbol = Symbol(symbol_name='ExampleSymbol', symbol_info='This is an example symbol')
session.add(new_symbol)
session.commit()

# Close the session
session.close()
