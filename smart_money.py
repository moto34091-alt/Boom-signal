def liquidity_sweep(df):
    last = df.iloc[-1]

    upper_wick = last["high"] - max(last["open"], last["close"])
    lower_wick = min(last["open"], last["close"]) - last["low"]

    if upper_wick > abs(last["close"] - last["open"]) * 2:
        return True

    if lower_wick > abs(last["close"] - last["open"]) * 2:
        return True

    return False


def consolidation(df):
    diff = abs(df["ema5"].iloc[-1] - df["ema13"].iloc[-1])
    return diff < 0.0002
