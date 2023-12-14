from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from data_engine.db.base import Base
from data_engine.model import Symbol


class HistoricalPrice(Base):
    __tablename__ = 'historical_prices'

    symbol = Column(String(255), ForeignKey('symbols.symbol'), primary_key=True)
    datetime = Column(DATETIME, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    adj_open = Column(Float)
    adj_high = Column(Float)
    adj_low = Column(Float)
    adj_close = Column(Float)
    adj_volume = Column(Integer)
    split_factor = Column(Float)
    dividend = Column(Float)

    # Relationship to the Symbol table
    symbol_data = relationship("Symbol", back_populates="prices")

    def __init__(self, symbol, datetime, open, high, low, close, volume, adj_open, adj_high, adj_low, adj_close, adj_volume, split_factor, dividend):
        self.symbol = symbol
        self.datetime = datetime
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.adj_open = adj_open
        self.adj_high = adj_high
        self.adj_low = adj_low
        self.adj_close = adj_close
        self.adj_volume = adj_volume
        self.split_factor = split_factor
        self.dividend = dividend

    def __repr__(self):
        return f"<HistoricalPrice(symbol={self.symbol}, datetime={self.datetime}, open={self.open}, high={self.high}, low={self.low}, close={self.close}, volume={self.volume})>"

