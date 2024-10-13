from trader import SmigTrader

# Example usage
try:
    trader = SmigTrader(
        symbols=["AAPL", "TSLA"], start="2023-01-01", end="2023-12-31", paper=False
    )
    print(repr(trader))
except ValueError as e:
    print(f"Error: {e}")
