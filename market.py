import os
import requests
import pandas as pd


# ─────────────────────────────
# 🔐 API
# ─────────────────────────────
TWELVE_API_KEY = os.getenv(
    "TWELVE_API_KEY"
)

print("TWELVE_API_KEY =", TWELVE_API_KEY)


# ─────────────────────────────
# 📊 GET MARKET DATA
# ─────────────────────────────
def get_crypto(symbol="BTCUSDT"):

    try:

        # ─────────────────────
        # 🪙 CRYPTO
        # ─────────────────────
        crypto_pairs = [

            "BTCUSDT",
            "ETHUSDT",
            "SOLUSDT",
            "BNBUSDT"
        ]

        # ─────────────────────
        # 💱 FOREX
        # ─────────────────────
        forex_pairs = [

            "EURUSD",
            "GBPUSD",
            "USDJPY",
            "AUDUSD",
            "USDCAD",
            "NZDUSD"
        ]

        # ─────────────────────
        # 🪙 CRYPTO BINANCE
        # ─────────────────────
        if symbol in crypto_pairs:

            url = (
                "https://api.binance.com/api/v3/klines"
                f"?symbol={symbol}"
                "&interval=1m"
                "&limit=100"
            )

            print("BINANCE URL =", url)

            response = requests.get(
                url,
                timeout=10
            )

            data = response.json()

            print("BINANCE DATA =", data)

            if not isinstance(data, list):

                return None

            df = pd.DataFrame(data)

            df = df.iloc[:, :6]

            df.columns = [

                "time",
                "open",
                "high",
                "low",
                "close",
                "volume"
            ]

        # ─────────────────────
        # 💱 FOREX TWELVE DATA
        # ─────────────────────
        elif symbol in forex_pairs:

            pair = (
                f"{symbol[:3]}/"
                f"{symbol[3:]}"
            )

            url = (
                "https://api.twelvedata.com/time_series"
                f"?symbol={pair}"
                "&interval=1min"
                "&outputsize=100"
                f"&apikey={TWELVE_API_KEY}"
            )

            print("FOREX URL =", url)

            response = requests.get(
                url,
                timeout=10
            )

            data = response.json()

            print("FOREX DATA =", data)

            if "values" not in data:

                return None

            df = pd.DataFrame(
                data["values"]
            )

            df = df.rename(columns={
                "datetime": "time"
            })

            if "volume" not in df.columns:

                df["volume"] = 0

            df = df[[
                "time",
                "open",
                "high",
                "low",
                "close",
                "volume"
            ]]

        else:

            print("UNKNOWN SYMBOL =", symbol)

            return None

        # ─────────────────────
        # 🔢 FLOAT
        # ─────────────────────
        for col in [

            "open",
            "high",
            "low",
            "close",
            "volume"
        ]:

            df[col] = df[col].astype(
                float
            )

        # ─────────────────────
        # 📈 SORT
        # ─────────────────────
        df = df.iloc[::-1].reset_index(
            drop=True
        )

        print("MARKET OK =", symbol)

        return df

    except Exception as e:

        print("MARKET ERROR =", e)

        return None
