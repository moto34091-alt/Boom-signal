import requests
import pandas as pd

API_KEY = "TON_API_KEY"

def get_candles(symbol="XAU/USD"):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1min&outputsize=50&apikey={API_KEY}"

    r = requests.get(url).json()

    data = r["values"]

    df = pd.DataFrame(data)
    df = df.astype(float)

    df = df.rename(columns={
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close"
    })

    return df
