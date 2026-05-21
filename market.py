import requests
import pandas as pd
import os

TWELVE_API_KEY = os.getenv("TWELVE_API_KEY")


# =========================
# 🟡 BINANCE (crypto)
# =========================
def get_binance(symbol="BTCUSDT"):

    try:

        url = "https://api.binance.com/api/v3/klines"

        params = {
            "symbol": symbol,
            "interval": "1m",
            "limit": 100
        }

        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        if not isinstance(data, list):
            return None

        df = pd.DataFrame(data, columns=[
            "time", "open", "high", "low", "close", "volume",
            "close_time", "qav", "trades",
            "taker_base", "taker_quote", "ignore"
        ])

        df[["open","high","low","close","volume"]] = df[
            ["open","high","low","close","volume"]
        ].astype(float)

        return df

    except:
        return None


# =========================
# 🟢 TWELVE DATA (forex/crypto)
# =========================
def get_twelve(symbol="BTC/USD"):

    try:

        if not TWELVE_API_KEY:
            return None

        url = "https://api.twelvedata.com/time_series"

        params = {
            "symbol": symbol,
            "interval": "1min",
            "outputsize": 100,
            "apikey": TWELVE_API_KEY
        }

        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        if "values" not in data:
            return None

        df = pd.DataFrame(data["values"])
        df = df.iloc[::-1]

        df["open"] = df["open"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)

        # ⚡ TwelveData n'a pas vrai volume
        df["volume"] = 1  # fallback intelligent

        return df

    except:
        return None


# =========================
# 🚀 SMART SWITCH
# =========================
def get_crypto(symbol="BTCUSDT"):

    # 1️⃣ Binance first
    df = get_binance(symbol)

    if df is not None:
        return df

    # 2️⃣ fallback TwelveData
    df = get_twelve(symbol.replace("USDT", "/USD"))

    return df
