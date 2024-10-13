import unittest
from smig_trader.trader import SmigTrader


class TestSmigTrader(unittest.TestCase):
    def setUp(self):
        self.trader = SmigTrader(
            api_key="test_key", secret_key="test_secret", paper=True
        )

    def test_creds(self):
        self.assertEqual(self.trader.creds.api_key, "test_key")
        self.assertEqual(self.trader.creds.secret_key, "test_secret")
        self.assertTrue(self.trader.creds.paper)

    def test_set_symbols(self):
        self.trader.set_symbols(["AAPL", "TSLA"])
        self.assertEqual(self.trader.symbols, ["AAPL", "TSLA"])

    def test_invalid_symbols(self):
        with self.assertRaises(ValueError):
            self.trader.set_symbols("AAPL")

    # Add more test cases as needed


if __name__ == "__main__":
    unittest.main()
