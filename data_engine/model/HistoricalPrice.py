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
    last = Column(Float)

    # Relationship to the Symbol table
    symbol_data = relationship("Symbol", back_populates="prices")

    def __init__(self, symbol, datetime, open, high, low, close, volume, last):
        self.symbol = symbol
        self.datetime = datetime
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.last = last

    def __repr__(self):
        return f"<HistoricalPrice(symbol={self.symbol}, datetime={self.datetime}, open={self.open}, high={self.high}, low={self.low}, close={self.close}, volume={self.volume})>"

