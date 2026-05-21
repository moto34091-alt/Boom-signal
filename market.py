import requests
import pandas as pd


def get_crypto(symbol="BTCUSDT"):

    url = (
        f"https://api.binance.com/api/v3/klines"
        f"?symbol={symbol}&interval=1m&limit=100"
    )

    response = requests.get(url)

    data = response.json()

    # ❌ erreur API
    if not isinstance(data, list):
        return None

    # 📊 dataframe
    df = pd.DataFrame(data, columns=[

        "time",
        "open",
        "high",
        "low",
        "close",
        "volume",

        "close_time",
        "quote_asset_volume",
        "trades",
        "taker_buy_base",
        "taker_buy_quote",
        "ignore"
    ])

    # 🔢 convertir nombres
    numeric_cols = [
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col])

    return df
