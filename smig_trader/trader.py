import os
from collections import namedtuple
from datetime import datetime
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.trading.client import TradingClient


class SmigTrader:
    AlpacaCreds = namedtuple("AlpacaCreds", ["api_key", "secret_key", "paper"])

    def __init__(
        self,
        api_key=None,
        secret_key=None,
        paper=True,
        symbols=None,
        start=None,
        end=None,
    ):
        # Get API and secret keys from environment variables if not provided
        _api_key = api_key or os.getenv("ALPACA_PAPER_API_KEY", "").strip()
        _secret_key = secret_key or os.getenv("ALPACA_PAPER_SECRET_KEY", "").strip()
        _paper = paper

        # Raise an exception if either API key or secret key is missing or empty
        if not _api_key:
            raise ValueError("API key is required and cannot be empty.")
        if not _secret_key:
            raise ValueError("Secret key is required and cannot be empty.")
        # Set creds
        self._creds = self.AlpacaCreds(
            api_key=_api_key, secret_key=_secret_key, paper=_paper
        )

        # Handle symbols (list of strings)
        if symbols is None:
            self._symbols = []
        elif isinstance(symbols, list) and all(isinstance(s, str) for s in symbols):
            self._symbols = symbols
        else:
            raise ValueError("Symbols must be a list of strings.")

        # Handle start and end dates (convert strings to datetime objects)
        self._start = self._convert_to_datetime(start)
        self._end = self._convert_to_datetime(end)

        # init clients
        self._init_client()

        # set account
        self._account = self.trade_client.get_account()

        # set data
        self._data = {}
        self._create_request_params()

    def _init_client(self):
        self._trade_client = TradingClient(
            api_key=self.creds.api_key,
            secret_key=self.creds.secret_key,
            paper=self.creds.paper,
        )
        self._data_client = StockHistoricalDataClient(
            api_key=self.creds.api_key, secret_key=self.creds.secret_key
        )

    def _create_request_params(self, *args, **kwargs):
        _request_params = {}
        if "timeframe" in kwargs:
            _request_params["timeframe"] = kwargs["timeframe"]
        else:
            _request_params["timeframe"] = TimeFrame.Day
        if "start" in kwargs:
            _request_params["start"] = kwargs["start"]
        else:
            _request_params["start"] = self._start
        if "end" in kwargs:
            _request_params["end"] = kwargs["end"]
        else:
            _request_params["end"] = self._end
        if "symbols" in kwargs and isinstance(kwargs["symbols"], list):
            _request_params["symbol_or_symbols"] = kwargs["symbols"]
        else:
            _request_params["symbol_or_symbols"] = self._symbols
        print(f"Request params: {_request_params}")
        try:
            self._request_params = StockBarsRequest(**_request_params)
        except Exception as e:
            raise ValueError(f"Invalid request parameters: {e}")

    def _get_stock_bars(self):
        # get stock bars/data
        self._data = self.data_client.get_stock_bars(self._request_params)

    @property
    def account(self):
        return self._account

    @property
    def data(self):
        return self._data

    @property
    def trade_client(self):
        if not hasattr(self, "_trade_client"):
            self._init_client()
        return self._trade_client

    @property
    def data_client(self):
        if not hasattr(self, "_data_client"):
            self._init_client()
        return self._data_client

    @property
    def creds(self):
        return self._creds

    @property
    def symbols(self):
        return self._symbols

    @symbols.setter
    def symbols(self, value):
        if isinstance(value, list) and all(isinstance(s, str) for s in value):
            self._symbols = value
        else:
            raise ValueError("Symbols must be a list of strings.")

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = self._convert_to_datetime(value)

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = self._convert_to_datetime(value)

    def _convert_to_datetime(self, date_value):
        """Convert a string or datetime value to a datetime object."""
        if isinstance(date_value, datetime):
            return date_value
        elif isinstance(date_value, str):
            try:
                return datetime.strptime(date_value, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Date string must be in the format 'YYYY-MM-DD'.")
        elif date_value is None:
            return None
        else:
            raise ValueError(
                "Date must be a datetime object, a string in 'YYYY-MM-DD' format, or None."
            )

    def __repr__(self):
        """Return a multi-line detailed string representation of the SmigTrader object for debugging."""
        return f"""SmigTrader(
    creds=AlpacaCreds(
        api_key={self._creds.api_key!r},
        secret_key={self._creds.secret_key!r},
        paper={self._creds.paper},
    )
    symbols={self._symbols!r},
    start={self._start!r},
    end={self._end!r}
)"""

    def __str__(self):
        """Return a multi-line user-friendly string representation of the SmigTrader object."""
        return f"""SmigTrader:
  - Trading symbols: {self._symbols}
  - Start date: {self._start.date() if self._start else 'N/A'}
  - End date: {self._end.date() if self._end else 'N/A'}
  - Mode: {'Paper trading' if self._creds.paper else 'Live trading'}"""
