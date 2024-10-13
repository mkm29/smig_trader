from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional
import ulid


class StockObservation(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(ulid.new()), primary_key=True)
    symbol: str
    timestamp: datetime = Field(index=True, unique=True)
    open: float
    high: float
    low: float
    close: float
    volume: float
    trade_count: float
    vwap: float


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
