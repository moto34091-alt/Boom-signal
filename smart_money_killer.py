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
        rsi = round(
            last.get("rsi", 50),
            2
        )

        ema5 = last.get("ema5", 0)
        ema13 = last.get("ema13", 0)

        # ─────────────────────────────
        # 🌊 VOLATILITY
        # ─────────────────────────────
        volatility = (
            (df["high"] - df["low"])
            .tail(10)
            .mean()
        )

        # 🚫 market trop lent
        if volatility < 0.05:
            return None

        # ─────────────────────────────
        # 📈 TREND
        # ─────────────────────────────
        trend_up = ema5 > ema13
        trend_down = ema5 < ema13

        # ─────────────────────────────
        # 🔨 CANDLE STRUCTURE
        # ─────────────────────────────
        body = abs(
            last["close"] - last["open"]
        )

        lower_wick = (
            min(
                last["open"],
                last["close"]
            ) - last["low"]
        )

        upper_wick = (
            last["high"] - max(
                last["open"],
                last["close"]
            )
        )

        # ─────────────────────────────
        # ⚡ STRONG CANDLE FILTER
        # ─────────────────────────────
        candle_power = abs(
            last["close"] - last["open"]
        )

        avg_power = abs(
            (
                df["close"] - df["open"]
            ).tail(10).mean()
        )

        # 🚫 bougie faible
        if candle_power < avg_power:
            return None

        # ─────────────────────────────
        # 📍 ENTRY STATUS
        # ─────────────────────────────
        def entry_status(signal_type):

            # 🟢 BUY
            if signal_type == "BUY":

                if rsi < 60:
                    return "✅ ENTRÉE POSSIBLE"

                elif rsi >= 60 and rsi < 70:
                    return "⚠️ ENTRÉE EN RETARD"

                else:
                    return "❌ NE PAS ENTRER"

            # 🔴 SELL
            elif signal_type == "SELL":

                if rsi > 40:
                    return "✅ ENTRÉE POSSIBLE"

                elif rsi <= 40 and rsi > 30:
                    return "⚠️ ENTRÉE EN RETARD"

                else:
                    return "❌ NE PAS ENTRER"

            return "⚪ WAIT"

        # ─────────────────────────────
        # 🔨 HAMMER BUY
        # ─────────────────────────────
        if (

            lower_wick > body * 2

            and

            upper_wick < body

            and

            trend_up

            and

            rsi < 65
        ):

            return {

                "signal": "BUY",

                "score": 92,

                "strategy": "🔨 HAMMER BUY",

                "entry": entry_status("BUY")
            }

        # ─────────────────────────────
        # ☄ SHOOTING STAR SELL
        # ─────────────────────────────
        if (

            upper_wick > body * 2

            and

            lower_wick < body

            and

            trend_down

            and

            rsi > 35
        ):

            return {

                "signal": "SELL",

                "score": 92,

                "strategy": "☄ SHOOTING STAR",

                "entry": entry_status("SELL")
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

            and

            trend_up

            and

            rsi < 65
        ):

            return {

                "signal": "BUY",

                "score": 90,

                "strategy": "⭐ MORNING STAR",

                "entry": entry_status("BUY")
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

            and

            trend_down

            and

            rsi > 35
        ):

            return {

                "signal": "SELL",

                "score": 90,

                "strategy": "🌙 EVENING STAR",

                "entry": entry_status("SELL")
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

            and

            trend_up

            and

            rsi < 65
        ):

            return {

                "signal": "BUY",

                "score": 80,

                "strategy": "📈 3 BULLISH",

                "entry": entry_status("BUY")
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

            and

            trend_down

            and

            rsi > 35
        ):

            return {

                "signal": "SELL",

                "score": 80,

                "strategy": "📉 3 BEARISH",

                "entry": entry_status("SELL")
            }

        # ─────────────────────────────
        # 🚫 NO SIGNAL
        # ─────────────────────────────
        return None

    except Exception as e:

        print(
            "SMART MONEY ERROR:",
            e
        )

        return None
