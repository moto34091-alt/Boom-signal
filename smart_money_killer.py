def smart_money_signal(df):

    last = df.iloc[-1]
    prev = df.iloc[-2]

    rsi = last["rsi"]
    score = 0
    direction = None

    # 🔴 PRIORITÉ RSI (zone extrême = signal fort)
    if rsi >= 90:
        direction = "SELL"
        score += 55

    elif rsi >= 80:
        direction = "SELL"
        score += 45

    elif rsi <= 20:
        direction = "BUY"
        score += 55

    elif rsi <= 30:
        direction = "BUY"
        score += 45

    else:
        # ⚡ trend normal
        if last["ema5"] > last["ema13"]:
            direction = "BUY"
        else:
            direction = "SELL"
        score += 25

    # 📊 momentum réel
    move = abs(last["close"] - prev["close"]) / prev["close"]

    if move > 0.001:
        score += 20
    elif move < 0.0003:
        score -= 10

    # 🌊 volatilité (vraie dynamique marché)
    try:
        volatility = (df["high"] - df["low"]).tail(10).mean()

        if volatility > 0.05:
            score += 15
        elif volatility < 0.02:
            score -= 10
    except:
        pass

    # 📦 volume (si disponible)
    try:
        avg_volume = df["volume"].tail(20).mean()

        if last["volume"] > avg_volume:
            score += 10
    except:
        pass

    # ⚠️ correction incohérence RSI / direction
    if rsi > 85 and direction == "BUY":
        score -= 25

    if rsi < 25 and direction == "SELL":
        score -= 25

    # ❌ filtre anti bruit
    if score < 45:
        return None

    # 🎯 confidence system
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
