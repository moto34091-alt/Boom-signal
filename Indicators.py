import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator


def calculate_indicators(df):
    df['ema5'] = EMAIndicator(df['close'], window=5).ema_indicator()
    df['ema13'] = EMAIndicator(df['close'], window=13).ema_indicator()

    rsi = RSIIndicator(df['close'], window=7)
    df['rsi'] = rsi.rsi()

    return df
