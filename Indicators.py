from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

def add_indicators(df):
    df["ema5"] = EMAIndicator(df["close"], window=5).ema_indicator()
    df["ema13"] = EMAIndicator(df["close"], window=13).ema_indicator()
    df["rsi"] = RSIIndicator(df["close"], window=7).rsi()
    return df
