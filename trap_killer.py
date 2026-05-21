def detect_trap(df):

    last = df.iloc[-1]

    resistance = df["high"].rolling(20).max().iloc[-2]
    support = df["low"].rolling(20).min().iloc[-2]

    body = abs(last["close"] - last["open"])
    full = last["high"] - last["low"]

    if full == 0:
        return None

    wick_ratio = body / full

    # 🔴 bull trap
    if last["high"] > resistance and last["close"] < resistance:
        if wick_ratio < 0.4:
            return {"type": "BULL_TRAP", "signal": "SELL"}

    # 🟢 bear trap
    if last["low"] < support and last["close"] > support:
        if wick_ratio < 0.4:
            return {"type": "BEAR_TRAP", "signal": "BUY"}

    return None
