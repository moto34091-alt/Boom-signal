def detect_trap(df):

    last = df.iloc[-1]
    prev = df.iloc[-2]

    # 📏 zones
    resistance = df["high"].rolling(20).max().iloc[-2]
    support = df["low"].rolling(20).min().iloc[-2]

    # 📊 taille bougie
    body = abs(last["close"] - last["open"])
    full = last["high"] - last["low"]

    if full == 0:
        return None

    wick_ratio = body / full

    # 🔴 BULL TRAP
    if last["high"] > resistance:

        # rejet violent
        if last["close"] < resistance:

            # longue mèche
            if wick_ratio < 0.4:

                return {
                    "type": "BULL_TRAP",
                    "signal": "SELL"
                }

    # 🟢 BEAR TRAP
    if last["low"] < support:

        if last["close"] > support:

            if wick_ratio < 0.4:

                return {
                    "type": "BEAR_TRAP",
                    "signal": "BUY"
                }

    return None
