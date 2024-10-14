from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint
from typing import Optional, List
import ulid


class StockSymbol(SQLModel, table=True):
    __tablename__ = "stock_symbol"

    id: str = Field(default_factory=lambda: str(ulid.new()), primary_key=True)
    symbol: str = Field(unique=True, index=True)

    # Define relationship to StockObservation
    observations: List["StockObservation"] = Relationship(back_populates="stock_symbol")


class StockObservation(SQLModel, table=True):
    __tablename__ = "stock_observation"
    id: str = Field(default_factory=lambda: str(ulid.new()), primary_key=True)
    symbol_id: str = Field(foreign_key="stock_symbol.id")
    timestamp: datetime = Field(index=True)
    open: float
    high: float
    low: float
    close: float
    volume: Optional[float] = None
    trade_count: Optional[float] = None
    vwap: Optional[float] = None

    stock_symbol: StockSymbol = Relationship(back_populates="observations")

    __table_args__ = (UniqueConstraint("symbol_id", "timestamp"),)


# Example usage:
# stock = StockObservation(
#     symbol="GOOG",
#     timestamp=datetime(2023, 1, 3, 5, 0, tzinfo=TzInfo('UTC')),
#     open=89.83,
#     high=91.55,
#     low=89.02,
#     close=89.7,
#     volume=24084543.0,
#     trade_count=202681.0,
#     vwap=89.821833
# )
