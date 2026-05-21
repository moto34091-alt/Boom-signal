from fake_breakout_killer import fake_breakout_filter


def sniper_breakout(df):

    last = df.iloc[-1]

    score = 0
    direction = None

    resistance = df["high"].rolling(15).max().iloc[-2]
    support = df["low"].rolling(15).min().iloc[-2]

    # 🚀 breakout detection
    if last["close"] > resistance:
        direction = "BUY"
        score += 40

    elif last["close"] < support:
        direction = "SELL"
        score += 40

    else:
        return None

    # 🔥 FAKE BREAKOUT FILTER
    if not fake_breakout_filter(df, direction):
        return None

    # 📈 EMA
    if last["ema5"] > last["ema13"]:
        score += 20

    if last["ema5"] < last["ema13"]:
        score += 20

    # 📊 RSI
    if last["rsi"] > 60:
        score += 20

    if last["rsi"] < 40:
        score += 20

    # ⚡ impulsion
    candle_size = abs(last["close"] - last["open"])
    avg_size = abs(df["close"] - df["open"]).tail(10).mean()

    if candle_size > avg_size * 1.5:
        score += 20

    # 🎯 final signal
    if score >= 80:

        return {
            "signal": direction,
            "score": score,
            "rsi": round(last["rsi"], 2),
            "fake_breakout": False
        }

    return None
