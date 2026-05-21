def detect_structure(df):

    highs = df["high"]
    lows = df["low"]

    last_high = highs.iloc[-2]
    prev_high = highs.iloc[-4]

    last_low = lows.iloc[-2]
    prev_low = lows.iloc[-4]

    # 📈 BOS bullish
    if last_high > prev_high:

        return {
            "type": "BOS",
            "direction": "BUY"
        }

    # 📉 BOS bearish
    if last_low < prev_low:

        return {
            "type": "BOS",
            "direction": "SELL"
        }

    return None
