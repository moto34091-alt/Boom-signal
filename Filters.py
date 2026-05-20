def strong_bullish_candle(df):
    candle = df.iloc[-1]

    body = abs(candle['close'] - candle['open'])
    total = candle['high'] - candle['low']

    if total == 0:
        return False

    return candle['close'] > candle['open'] and body / total > 0.6



def strong_bearish_candle(df):
    candle = df.iloc[-1]

    body = abs(candle['close'] - candle['open'])
    total = candle['high'] - candle['low']

    if total == 0:
        return False

    return candle['close'] < candle['open'] and body / total > 0.6
