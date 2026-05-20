def price_changed(df):
    last = df.iloc[-1]["close"]
    prev = df.iloc[-2]["close"]

    return abs(last - prev) > 0.0003


def generate_signal(df):

    last = df.iloc[-1]

    # 🔴 BLOQUE si pas de mouvement
    if not price_changed(df):
        return None

    score = 0
    direction = None

    # TREND
    if last["ema5"] > last["ema13"]:
        score += 30
        direction = "BUY"

    if last["ema5"] < last["ema13"]:
        score += 30
        direction = "SELL"

    # RSI
    if 50 < last["rsi"] < 70:
        score += 20
    elif 30 < last["rsi"] < 50:
        score += 20

    if score >= 75:
        return {
            "signal": direction,
            "score": score,
            "rsi": round(last["rsi"], 2)
        }

    return None
