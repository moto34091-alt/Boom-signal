import requests
import pandas as pd

TWELVE_API = "TON_API_KEY"


# 🌍 FOREX (réel)
def get_forex(symbol="EUR/USD"):

    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&outputsize=50&apikey={TWELVE_API}"

    r = requests.get(url).json()

    if "values" not in r:
        return None

    df = pd.DataFrame(r["values"]).astype(float)
    return df.iloc[::-1].reset_index(drop=True)


# ₿ CRYPTO (réel)
def get_crypto(symbol="BTCUSDT"):

    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=50"

    data = requests.get(url).json()

    df = pd.DataFrame(data)

    df = df[[1,2,3,4]]
    df.columns = ["open","high","low","close"]

    return df.astype(float)
