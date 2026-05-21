def detect_strategy(df):

    last = df.iloc[-1]
    prev1 = df.iloc[-2]
    prev2 = df.iloc[-3]

    # ─────────────
    # 🔨 HAMMER
    # ─────────────
    body = abs(last["close"] - last["open"])
    wick_low = last["open"] - last["low"]

    if wick_low > body * 2 and last["close"] > last["open"]:
        return "HAMMER_BUY"

    # ─────────────
    # ⭐ MORNING STAR
    # ─────────────
    if (
        prev2["close"] < prev2["open"] and
        prev1["close"] < prev1["open"] and
        last["close"] > last["open"]
    ):
        return "MORNING_STAR"

    # ─────────────
    # ☀ EVENING STAR
    # ─────────────
    if (
        prev2["close"] > prev2["open"] and
        prev1["close"] > prev1["open"] and
        last["close"] < last["open"]
    ):
        return "EVENING_STAR"

    # ─────────────
    # 📈 3 BULLISH
    # ─────────────
    if (
        prev2["close"] > prev2["open"] and
        prev1["close"] > prev1["open"] and
        last["close"] > last["open"]
    ):
        return "THREE_BULLISH"

    # ─────────────
    # 📉 3 BEARISH
    # ─────────────
    if (
        prev2["close"] < prev2["open"] and
        prev1["close"] < prev1["open"] and
        last["close"] < last["open"]
    ):
        return "THREE_BEARISH"

    return None
