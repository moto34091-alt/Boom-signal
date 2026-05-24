import os
import requests
import pandas as pd


# ─────────────────────────────
# 🔐 API KEY
# ─────────────────────────────
API_KEY = os.getenv("TWELVE_API_KEY")


# ─────────────────────────────
# 📊 GET MARKET DATA
# ─────────────────────────────
def get_crypto(symbol="BTCUSDT"):

    try:

        # ─────────────────────
        # 🔄 SYMBOLS
        # ─────────────────────
        symbols = {

            # 🪙 CRYPTO
            "BTCUSDT": "BTC/USD",
            "ETHUSDT": "ETH/USD",
            "SOLUSDT": "SOL/USD",
            "BNBUSDT": "BNB/USD",

            # 💱 FOREX
            "EURUSD": "EUR/USD",
            "GBPUSD": "GBP/USD",
            "USDJPY": "USD/JPY",
            "AUDUSD": "AUD/USD",
            "USDCAD": "USD/CAD",
            "NZDUSD": "NZD/USD"
        }

        # ❌ UNKNOWN SYMBOL
        if symbol not in symbols:

            print("UNKNOWN SYMBOL:", symbol)

            return None

        real_symbol = symbols[symbol]

        # ─────────────────────
        # 🌐 TWELVEDATA API
        # ─────────────────────
        url = (
            "https://api.twelvedata.com/time_series"
            f"?symbol={real_symbol}"
            "&interval=1min"
            "&outputsize=100"
            "&format=JSON"
            f"&apikey={API_KEY}"
        )

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        # ❌ API ERROR
        if "values" not in data:

            print("API ERROR:", data)

            return None

        values = data["values"]

        # ─────────────────────
        # 📊 DATAFRAME
        # ─────────────────────
        df = pd.DataFrame(values)

        # 🔢 FLOAT
        for col in [
            "open",
            "high",
            "low",
            "close"
        ]:

            df[col] = df[col].astype(float)

        # 🔄 OLD → NEW
        df = df.iloc[::-1]

        df.reset_index(
            drop=True,
            inplace=True
        )

        return df

    except Exception as e:

        print("MARKET ERROR:", e)

        return None
