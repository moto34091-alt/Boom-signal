import os
import requests
import pandas as pd


TWELVE_API_KEY = os.getenv(
    "TWELVE_API_KEY"
)


# ─────────────────────────────
# 📊 GET MARKET DATA
# ─────────────────────────────
def get_crypto(symbol="BTCUSDT"):

    try:

        # ─────────────────────
        # 🪙 CRYPTO BINANCE
        # ─────────────────────
        crypto_pairs = [

            "BTCUSDT",
            "ETHUSDT",
            "SOLUSDT",
            "BNBUSDT"
        ]

        # ─────────────────────
        # 💱 FOREX TWELVE DATA
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
        # 🪙 CRYPTO
        # ─────────────────────
        if symbol in crypto_pairs:

            url = (
                "https://api.binance.com/api/v3/klines"
                f"?symbol={symbol}"
                "&interval=1m"
                "&limit=100"
            )

            response = requests.get(
                url,
                timeout=10
            )

            data = response.json()

            if not isinstance(data, list):

                print("BINANCE ERROR:", data)

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
        # 💱 FOREX
        # ─────────────────────
        elif symbol in forex_pairs:

            pair = f"{symbol[:3]}/{symbol[3:]}"

            url = (
                "https://api.twelvedata.com/time_series"
                f"?symbol={pair}"
                "&interval=1min"
                "&outputsize=100"
                f"&apikey={TWELVE_API_KEY}"
            )

            response = requests.get(
                url,
                timeout=10
            )

            data = response.json()

            if "values" not in data:

                print("FOREX ERROR:", data)

                return None

            df = pd.DataFrame(
                data["values"]
            )

            df = df.rename(columns={

                "datetime": "time"
            })

            df = df[[
                "time",
                "open",
                "high",
                "low",
                "close",
                "volume"
            ]]

        else:

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

            df[col] = df[col].astype(float)

        # ─────────────────────
        # 📈 ORDER
        # ─────────────────────
        df = df.iloc[::-1].reset_index(
            drop=True
        )

        return df

    except Exception as e:

        print("MARKET ERROR:", e)

        return None
