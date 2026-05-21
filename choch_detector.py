def detect_choch(df):

    highs = df["high"]
    lows = df["low"]

    recent_high = highs.iloc[-2]
    old_high = highs.iloc[-5]

    recent_low = lows.iloc[-2]
    old_low = lows.iloc[-5]

    # 🔄 CHOCH bearish
    if recent_low < old_low and recent_high < old_high:

        return {
            "type": "CHOCH",
            "direction": "SELL"
        }

    # 🔄 CHOCH bullish
    if recent_high > old_high and recent_low > old_low:

        return {
            "type": "CHOCH",
            "direction": "BUY"
        }

    return None
