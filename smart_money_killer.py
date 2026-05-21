score = 0
direction = None

# EMA
if last["ema5"] > last["ema13"]:
    score += 30
    direction = "BUY"
else:
    score += 30
    direction = "SELL"

# RSI zones
if last["rsi"] > 70:
    score += 20
elif last["rsi"] < 30:
    score += 20
else:
    score += 10

# micro momentum
if abs(last["close"] - prev["close"]) > prev["close"] * 0.0003:
    score += 20

# volatilité
if volatility > 0.05:
    score += 10

# 🔥 seuil plus bas
if score >= 40:
    return {
        "signal": direction,
        "score": score,
        "rsi": last["rsi"]
    }

return None
