def smart_money_signal(df):

    if df is None or len(df) < 20:
        return None

    last = df.iloc[-1]
    prev1 = df.iloc[-2]
    prev2 = df.iloc[-3]

    volatility = (df["high"] - df["low"]).tail(10).mean()

    if volatility < 0.04:
        return None

    # ─────────────────────
    # 🔨 HAMMER
    # ─────────────────────
    body = abs(last["close"] - last["open"])
    lower_wick = min(last["open"], last["close"]) - last["low"]

    if lower_wick > body * 2:
        return {
            "signal": "BUY",
            "score": 90,
            "strategy": "🔨 HAMMER"
        }

    # ─────────────────────
    # ⭐ MORNING STAR
    # ─────────────────────
    if (
        prev2["close"] < prev2["open"] and
        prev1["close"] < prev1["open"] and
        last["close"] > last["open"]
    ):
        return {
            "signal": "BUY",
            "score": 92,
            "strategy": "⭐ MORNING STAR"
        }

    # ─────────────────────
    # ☀ EVENING STAR
    # ─────────────────────
    if (
        prev2["close"] > prev2["open"] and
        prev1["close"] > prev1["open"] and
        last["close"] < last["open"]
    ):
        return {
            "signal": "SELL",
            "score": 92,
            "strategy": "☀ EVENING STAR"
        }

    # ─────────────────────
    # 📈 3 BULLISH
    # ─────────────────────
    if (
        prev2["close"] > prev2["open"] and
        prev1["close"] > prev1["open"] and
        last["close"] > last["open"]
    ):
        return {
            "signal": "BUY",
            "score": 80,
            "strategy": "📈 3 BULLISH"
        }

    # ─────────────────────
    # 📉 3 BEARISH
    # ─────────────────────
    if (
        prev2["close"] < prev2["open"] and
        prev1["close"] < prev1["open"] and
        last["close"] < last["open"]
    ):
        return {
            "signal": "SELL",
            "score": 80,
            "strategy": "📉 3 BEARISH"
        }

    return None
