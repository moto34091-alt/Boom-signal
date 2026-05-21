def fake_breakout_filter(df, direction):

    last = df.iloc[-1]
    prev = df.iloc[-2]

    # 📏 breakout zones
    resistance = df["high"].rolling(15).max().iloc[-2]
    support = df["low"].rolling(15).min().iloc[-2]

    # 📊 taille bougie
    candle_body = abs(last["close"] - last["open"])

    candle_range = last["high"] - last["low"]

    # ⚠️ grosse mèche = danger
    wick_ratio = candle_body / candle_range

    # 🔴 évite petites clôtures
    if wick_ratio < 0.5:
        return False

    # 🟢 BUY breakout valide
    if direction == "BUY":

        # breakout faible
        if last["close"] <= resistance:
            return False

        # retour sous résistance
        if prev["close"] > resistance and last["close"] < resistance:
            return False

    # 🔴 SELL breakout valide
    if direction == "SELL":

        if last["close"] >= support:
            return False

        if prev["close"] < support and last["close"] > support:
            return False

    return True
