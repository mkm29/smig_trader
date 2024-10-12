import os
from collections import namedtuple

AlpacaCreds = namedtuple("AlpacaCreds", ["api_key", "secret_key", "paper"])
creds = AlpacaCreds(
    os.getenv("ALPACA_PAPER_API_KEY"), os.getenv("ALPACA_PAPER_SECRET_KEY"), True
)

# if __name__ == "__main__":
#     print(creds)
