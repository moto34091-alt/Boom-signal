def smart_money_signal(df):

    last = df.iloc[-1]
    prev = df.iloc[-2]

    score = 0
    direction = None

    # 📈 EMA trend
    if last["ema5"] > last["ema13"]:
        score += 30
        direction = "BUY"
    else:
        score += 30
        direction = "SELL"

    # 📊 RSI zones
    if last["rsi"] > 70:
        score += 20
    elif last["rsi"] < 30:
        score += 20
    else:
        score += 10

    # ⚡ momentum
    if abs(last["close"] - prev["close"]) > prev["close"] * 0.0003:
        score += 20

    # 🌊 volatilité (si dispo)
    try:
        volatility = (df["high"] - df["low"]).tail(10).mean()

        if volatility > 0.05:
            score += 10
    except:
        pass

    # 🎯 RSI direction boost
    if last["rsi"] > 75:
        direction = "SELL"
    elif last["rsi"] < 25:
        direction = "BUY"

    # ✅ signal final
    if score >= 40:

        return {
            "signal": direction,
            "score": score,
            "rsi": round(last["rsi"], 2)
        }

    return None
