def smart_money_signal(df):

    # ─────────────────────────────
    # ✅ SECURITY
    # ─────────────────────────────
    if df is None or len(df) < 20:
        return None

    try:

        # ─────────────────────────────
        # 📊 LAST CANDLES
        # ─────────────────────────────
        last = df.iloc[-1]
        prev1 = df.iloc[-2]
        prev2 = df.iloc[-3]

        # ─────────────────────────────
        # 📊 INDICATORS
        # ─────────────────────────────
        rsi = round(last.get("rsi", 50), 2)

        ema5 = last.get("ema5", 0)
        ema13 = last.get("ema13", 0)

        volatility = (
            (df["high"] - df["low"])
            .tail(10)
            .mean()
        )

        # ─────────────────────────────
        # 🚫 MARKET TOO FLAT
        # ─────────────────────────────
        if volatility < 0.03:
            return None

        # ─────────────────────────────
        # 📈 TREND
        # ─────────────────────────────
        trend_up = ema5 > ema13
        trend_down = ema5 < ema13

        # ─────────────────────────────
        # 🔨 HAMMER DETECTION
        # ─────────────────────────────
        body = abs(
            last["close"] - last["open"]
        )

        lower_wick = (
            min(last["open"], last["close"])
            - last["low"]
        )

        upper_wick = (
            last["high"]
            - max(last["open"], last["close"])
        )

        # ─────────────────────────────
        # 🔨 HAMMER BUY
        # ─────────────────────────────
        if (
            lower_wick > body * 2
            and upper_wick < body
            and trend_up
            and rsi < 65
        ):

            return {
                "signal": "BUY",
                "score": 92,
                "strategy": "🔨 HAMMER BUY"
            }

        # ─────────────────────────────
        # ☄ SHOOTING STAR
        # ─────────────────────────────
        if (
            upper_wick > body * 2
            and lower_wick < body
            and trend_down
            and rsi > 35
        ):

            return {
                "signal": "SELL",
                "score": 92,
                "strategy": "☄ SHOOTING STAR"
            }

        # ─────────────────────────────
        # ⭐ MORNING STAR
        # ─────────────────────────────
        if (

            prev2["close"] < prev2["open"]

            and

            prev1["close"] < prev1["open"]

            and

            last["close"] > last["open"]

            and trend_up

            and rsi < 65
        ):

            return {
                "signal": "BUY",
                "score": 90,
                "strategy": "⭐ MORNING STAR"
            }

        # ─────────────────────────────
        # 🌙 EVENING STAR
        # ─────────────────────────────
        if (

            prev2["close"] > prev2["open"]

            and

            prev1["close"] > prev1["open"]

            and

            last["close"] < last["open"]

            and trend_down

            and rsi > 35
        ):

            return {
                "signal": "SELL",
                "score": 90,
                "strategy": "🌙 EVENING STAR"
            }

        # ─────────────────────────────
        # 📈 3 BULLISH
        # ─────────────────────────────
        if (

            prev2["close"] > prev2["open"]

            and

            prev1["close"] > prev1["open"]

            and

            last["close"] > last["open"]

            and trend_up

            and rsi < 65
        ):

            return {
                "signal": "BUY",
                "score": 80,
                "strategy": "📈 3 BULLISH"
            }

        # ─────────────────────────────
        # 📉 3 BEARISH
        # ─────────────────────────────
        if (

            prev2["close"] < prev2["open"]

            and

            prev1["close"] < prev1["open"]

            and

            last["close"] < last["open"]

            and trend_down

            and rsi > 35
        ):

            return {
                "signal": "SELL",
                "score": 80,
                "strategy": "📉 3 BEARISH"
            }

        # ─────────────────────────────
        # 🚫 NO SIGNAL
        # ─────────────────────────────
        return None

    except Exception as e:

        print("SMART MONEY ERROR:", e)

        return None
