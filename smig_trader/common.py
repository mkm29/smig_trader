import os
from smig_trader.trader import SmigTrader
from smig_trader.settings import Settings

assert isinstance(
    os.environ.get("ALPACA_PAPER_API_KEY"), str
), "ALPACA_PAPER_API_KEY must be a string"
assert isinstance(
    os.environ.get("ALPACA_PAPER_SECRET_KEY"), str
), "ALPACA_PAPER_SECRET_KEY must be a string"

# Load settings from environment variables
settings = Settings(
    api_key=os.environ.get("ALPACA_PAPER_API_KEY"),
    secret_key=os.environ.get("ALPACA_PAPER_SECRET_KEY"),
)
# print(f"Settings: {settings}")
print(f"database_uri: {settings.database_uri}")
# if no API_KEY or SECRET_KEY are passed this will raise and exception
trader = SmigTrader(
    symbols=[
        "AAPL",
        "TSLA",
        "MSFT",
        "FB",
        "GOOG",
        "AMZN",
        "NVDA",
        "NFLX",
        "SPX",
        "QQQ",
        "DJI",
        "VIX",
    ],
    start="2023-01-01",
    end="2023-12-31",
    paper=True,
)
# print(repr(trader))
