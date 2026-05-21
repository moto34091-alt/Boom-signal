def detect_trap(df):

    if df is None or len(df) < 20:
        return True

    last = df.iloc[-1]

    body = abs(last["close"] - last["open"])

    wick = last["high"] - last["low"]

    # ❌ marché manipulation / fake move
    if wick > body * 5:
        return True

    # ❌ range trop plat
    volatility = (df["high"] - df["low"]).tail(10).mean()

    if volatility < 0.03:
        return True

    return False
