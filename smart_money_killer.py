from trap_killer import detect_trap


def smart_money_signal(df):

    trap = detect_trap(df)

    if not trap:
        return None

    last = df.iloc[-1]

    score = 50

    # 📈 EMA confirmation
    if trap["signal"] == "BUY":

        if last["ema5"] > last["ema13"]:
            score += 20

        if last["rsi"] > 50:
            score += 20

    # 📉 EMA bearish
    if trap["signal"] == "SELL":

        if last["ema5"] < last["ema13"]:
            score += 20

        if last["rsi"] < 50:
            score += 20

    # ⚡ impulsive rejection
    candle_size = abs(last["close"] - last["open"])

    avg_size = abs(
        df["close"] - df["open"]
    ).tail(10).mean()

    if candle_size > avg_size:
        score += 10

    # 🎯 final signal
    if score >= 80:

        return {
            "type": trap["type"],
            "signal": trap["signal"],
            "score": score,
            "rsi": round(last["rsi"], 2)
        }

    return None
