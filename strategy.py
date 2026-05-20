from filters import strong_bullish_candle, strong_bearish_candle


def generate_signal(df):
    last = df.iloc[-1]

    confidence = 0

    buy = False
    sell = False

    if last['ema5'] > last['ema13']:
        confidence += 25
        buy = True

    if last['ema5'] < last['ema13']:
        confidence += 25
        sell = True

    if last['rsi'] > 55:
        confidence += 20

    if last['rsi'] < 45:
        confidence += 20

    if strong_bullish_candle(df):
        confidence += 20

    if strong_bearish_candle(df):
        confidence += 20

    if confidence >= 70:
        if buy:
            return {
                "signal": "BUY",
                "confidence": confidence,
                "rsi": round(last['rsi'], 2)
            }

        if sell:
            return {
                "signal": "SELL",
                "confidence": confidence,
                "rsi": round(last['rsi'], 2)
            }

    return None
