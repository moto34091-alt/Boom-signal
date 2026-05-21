from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator


def add_indicators(df):

    # 📈 EMA
    df["ema5"] = EMAIndicator(
        close=df["close"],
        window=5
    ).ema_indicator()

    df["ema13"] = EMAIndicator(
        close=df["close"],
        window=13
    ).ema_indicator()

    # 📊 RSI
    df["rsi"] = RSIIndicator(
        close=df["close"],
        window=7
    ).rsi()

    return df
