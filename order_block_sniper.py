from order_block import detect_order_block


def order_block_sniper(df):

    ob = detect_order_block(df)

    if not ob:
        return None

    last = df.iloc[-1]

    score = 0

    # 🟢 BUY setup
    if ob["type"] == "BUY":

        # prix revient dans zone
        if ob["low"] <= last["close"] <= ob["high"]:

            score += 40

            # EMA bullish
            if last["ema5"] > last["ema13"]:
                score += 20

            # RSI bullish
            if last["rsi"] > 55:
                score += 20

            # rejet haussier
            if last["close"] > last["open"]:
                score += 20

            if score >= 80:

                return {
                    "signal": "BUY",
                    "score": score,
                    "zone_low": round(ob["low"], 2),
                    "zone_high": round(ob["high"], 2),
                    "rsi": round(last["rsi"], 2)
                }

    # 🔴 SELL setup
    if ob["type"] == "SELL":

        if ob["low"] <= last["close"] <= ob["high"]:

            score += 40

            if last["ema5"] < last["ema13"]:
                score += 20

            if last["rsi"] < 45:
                score += 20

            if last["close"] < last["open"]:
                score += 20

            if score >= 80:

                return {
                    "signal": "SELL",
                    "score": score,
                    "zone_low": round(ob["low"], 2),
                    "zone_high": round(ob["high"], 2),
                    "rsi": round(last["rsi"], 2)
                }

    return None
