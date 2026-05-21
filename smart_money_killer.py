def smart_money_signal(df):

    last = df.iloc[-1]
    prev = df.iloc[-2]

    rsi = last["rsi"]
    score = 0
    direction = None

    # 🔴 1. RSI PRIORITÉ FORTE (structure principale)
    if rsi >= 90:
        direction = "SELL"
        score += 60

    elif rsi >= 80:
        direction = "SELL"
        score += 50

    elif rsi >= 75:
        direction = "SELL"
        score += 40

    elif rsi <= 25:
        direction = "BUY"
        score += 60

    elif rsi <= 30:
        direction = "BUY"
        score += 50

    elif 70 <= rsi < 75:
        score += 25
        direction = "SELL" if last["ema5"] < last["ema13"] else "BUY"

    else:
        # ⚡ trend normal
        if last["ema5"] > last["ema13"]:
            direction = "BUY"
        else:
            direction = "SELL"
        score += 25

    # 📊 2. MOMENTUM
    move = abs(last["close"] - prev["close"]) / prev["close"]

    if move > 0.001:
        score += 20
    elif move < 0.0003:
        score -= 10

    # 🌊 3. VOLATILITÉ
    try:
        volatility = (df["high"] - df["low"]).tail(10).mean()

        if volatility > 0.05:
            score += 15
        elif volatility < 0.02:
            score -= 10
    except:
        pass

    # 📦 4. VOLUME (si dispo)
    try:
        avg_volume = df["volume"].tail(20).mean()

        if last["volume"] > avg_volume:
            score += 10
    except:
        pass

    # ⚠️ 5. CORRECTION CONTRADICTION
    if rsi > 85 and direction == "BUY":
        score -= 25

    if rsi < 25 and direction == "SELL":
        score -= 25

    # ❌ 6. FILTRE FINAL (IMPORTANT MODIFIÉ)
    if score < 35:
        return None

    # 🎯 7. CONFIDENCE SYSTEM
    if score >= 80:
        confidence = "HIGH"
    elif score >= 60:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    return {
        "signal": direction,
        "score": round(score, 2),
        "rsi": round(rsi, 2),
        "confidence": confidence
    }
