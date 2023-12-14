from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

# Define the base class
Base = declarative_base()

# Define the symbols class which represents the table
class Symbol(Base):
    __tablename__ = 'symbols'

    id = Column(Integer, primary_key=True)
    symbol_name = Column(String(255), nullable=False)
    symbol_info = Column(Text)