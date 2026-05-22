import os
import requests
import pandas as pd


API_KEY = os.getenv("TWELVE_API_KEY")


def get_crypto(symbol="BTCUSDT"):

    try:

        symbols = {

            # CRYPTO
            "BTCUSDT": "BTC/USD",
            "ETHUSDT": "ETH/USD",
            "SOLUSDT": "SOL/USD",
            "BNBUSDT": "BNB/USD",

            # FOREX
            "EURUSD": "EUR/USD",
            "GBPUSD": "GBP/USD",
            "USDJPY": "USD/JPY",
            "AUDUSD": "AUD/USD",
            "USDCAD": "USD/CAD",
            "NZDUSD": "NZD/USD"
        }

        real_symbol = symbols.get(symbol)

        url = (
            "https://api.twelvedata.com/time_series"
            f"?symbol={real_symbol}"
            "&interval=1min"
            "&outputsize=100"
            f"&apikey={API_KEY}"
        )

        response = requests.get(url)

        data = response.json()

        if "values" not in data:

            print(data)

            return None

        values = data["values"]

        df = pd.DataFrame(values)

        for col in [
            "open",
            "high",
            "low",
            "close"
        ]:

            df[col] = df[col].astype(float)

        df = df.iloc[::-1]

        df.reset_index(
            drop=True,
            inplace=True
        )

        return df

    except Exception as e:

        print("MARKET ERROR:", e)

        return None
