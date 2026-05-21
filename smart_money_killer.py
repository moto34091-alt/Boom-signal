def smart_money_signal(df):

    last = df.iloc[-1]
    prev = df.iloc[-2]

    rsi = last["rsi"]
    score = 0
    direction = None

    # 🔴 1. RSI EXTREME (priorité haute)
    if rsi <= 30:
        direction = "BUY"
        score += 55

    elif rsi >= 70:
        direction = "SELL"
        score += 55

    # 🟡 2. RANGE MARKET (IMPORTANT AJOUT)
    elif 40 <= rsi <= 60:
        if last["ema5"] > last["ema13"]:
            direction = "BUY"
        else:
            direction = "SELL"
        score += 35

    # ⚡ 3. TREND NORMAL (fallback)
    else:
        if last["ema5"] > last["ema13"]:
            direction = "BUY"
        else:
            direction = "SELL"
        score += 25

    # 📊 4. MOMENTUM
    move = abs(last["close"] - prev["close"]) / prev["close"]

    if move > 0.001:
        score += 20
    elif move < 0.0003:
        score -= 10

    # 🌊 5. VOLATILITÉ
    try:
        volatility = (df["high"] - df["low"]).tail(10).mean()

        if volatility > 0.05:
            score += 15
        elif volatility < 0.02:
            score -= 10
    except:
        pass

    # 📦 6. VOLUME
    try:
        avg_volume = df["volume"].tail(20).mean()

        if last["volume"] > avg_volume:
            score += 10
    except:
        pass

    # ⚠️ 7. CORRECTION CONTRADICTION
    if rsi <= 30 and direction == "SELL":
        score -= 25

    if rsi >= 70 and direction == "BUY":
        score -= 25

    # 🔵 8. RENFORCEMENT TREND
    if last["ema5"] < last["ema13"]:
        score += 10

    # ❌ 9. FILTRE FINAL (AJUSTÉ)
    if score < 20:
        return None

    # 🎯 10. CONFIDENCE
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
