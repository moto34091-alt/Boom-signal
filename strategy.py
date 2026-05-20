def generate_signal(df):

    last = df.iloc[-1]

    score = 0
    direction = None

    # trend EMA
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
