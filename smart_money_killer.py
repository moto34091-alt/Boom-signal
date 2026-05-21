def smart_money_signal(df):

    last = df.iloc[-1]
    prev = df.iloc[-2]

    score = 0
    direction = None

    rsi = last["rsi"]

    # 🔴 PRIORITÉ RSI EXTREME (signal principal)
    if rsi >= 85:
        direction = "SELL"
        score += 40

    elif rsi <= 25:
        direction = "BUY"
        score += 40

    # ⚡ RSI normal zone
    elif 45 <= rsi <= 65:
        score += 20
        direction = "BUY" if last["ema5"] > last["ema13"] else "SELL"

    else:
        # ⚡ fallback trend
        if last["ema5"] > last["ema13"]:
            direction = "BUY"
        else:
            direction = "SELL"
        score += 25

    # 📊 momentum réel
    momentum = abs(last["close"] - prev["close"])

    if momentum > prev["close"] * 0.0003:
        score += 15

    # 🌊 volatilité
    try:
        volatility = (df["high"] - df["low"]).tail(10).mean()

        if volatility > 0.05:
            score += 10
    except:
        pass

    # 📦 volume (si utile)
    try:
        avg_volume = df["volume"].tail(20).mean()

        if last["volume"] > avg_volume:
            score += 10
    except:
        pass

    # 🔥 correction conflit RSI/trend
    if rsi > 80 and direction == "BUY":
        score -= 20

    if rsi < 30 and direction == "SELL":
        score -= 20

    # 🎯 confidence
    if score >= 70:
        confidence = "HIGH"
    elif score >= 50:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    # ❌ filtre trop faible
    if score < 40:
        return None

    return {
        "signal": direction,
        "score": score,
        "rsi": round(rsi, 2),
        "confidence": confidence
    }
