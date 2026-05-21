def smart_money_signal(df):

    if df is None or len(df) < 20:
        return None

    last = df.iloc[-1]
    prev1 = df.iloc[-2]
    prev2 = df.iloc[-3]

    ema_up = last["ema5"] > last["ema13"]
    ema_down = last["ema5"] < last["ema13"]

    rsi = last["rsi"]

    volatility = (df["high"] - df["low"]).tail(10).mean()

    volume = last.get("volume", 0)

    # ❌ filtre marché mort
    if volatility < 0.05:
        return None

    if volume == 0:
        return None

    signal = None
    score = 0
    strategy = "NONE"

    # ⭐ MORNING STAR
    if (
        prev2["close"] < prev2["open"] and
        prev1["close"] < prev1["open"] and
        last["close"] > last["open"] and
        ema_up and rsi < 45
    ):
        signal = "BUY"
        score = 90
        strategy = "⭐ MORNING STAR"

    # ☀ EVENING STAR
    elif (
        prev2["close"] > prev2["open"] and
        prev1["close"] > prev1["open"] and
        last["close"] < last["open"] and
        ema_down and rsi > 55
    ):
        signal = "SELL"
        score = 90
        strategy = "☀ EVENING STAR"

    # 📈 3 BULLISH
    elif (
        prev2["close"] > prev2["open"] and
        prev1["close"] > prev1["open"] and
        last["close"] > last["open"] and
        ema_up and rsi < 50
    ):
        signal = "BUY"
        score = 80
        strategy = "📈 3 BULLISH"

    # 📉 3 BEARISH
    elif (
        prev2["close"] < prev2["open"] and
        prev1["close"] < prev1["open"] and
        last["close"] < last["open"] and
        ema_down and rsi > 50
    ):
        signal = "SELL"
        score = 80
        strategy = "📉 3 BEARISH"

    if signal is None:
        return None

    return {
        "signal": signal,
        "rsi": round(rsi, 2),
        "score": score,
        "strategy": strategy
    }
