from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from data_engine.db.base import Base
from data_engine.model.HistoricalPrice import HistoricalPrice


# Define the symbols class which represents the table
class Symbol(Base):
    __tablename__ = 'symbols'
    name = Column(String(255), nullable=False)
    symbol = Column(String(255), nullable=False, primary_key=True)
    stock_exchange = Column(String(255), nullable=False)
    stock_exchange_short = Column(String(255), nullable=False)
    timezone = Column(String(255))
    industry = Column(String(255))
    market_cap_category = Column(String(255))

    # Adding a relationship to the Symbol class
    prices = relationship("HistoricalPrice", order_by=HistoricalPrice.datetime, back_populates="symbol_data")
    def __init__(self, name, symbol, stock_exchange, stock_exchange_short, timezone, industry, market_cap_category):
        self.name = name
        self.symbol = symbol
        self.stock_exchange = stock_exchange
        self.stock_exchange_short = stock_exchange_short
        self.timezone = timezone
        self.industry = industry
        self.market_cap_category = market_cap_category

    def __repr__(self):
        return f"Symbol(name={self.name}, symbol={self.symbol}, stock_exchange={self.stock_exchange}, stock_exchange_short={self.stock_exchange_short}, timezone={self.timezone}, industry={self.industry}, market_cap_category={self.market_cap_category})"


