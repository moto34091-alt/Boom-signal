import pandas as pd


# ─────────────────────────────
# 📊 SMART MONEY SIGNAL
# ─────────────────────────────
def smart_money_signal(df):

    try:

        if len(df) < 10:
            return None

        last = df.iloc[-1]
        c1 = df.iloc[-1]
        c2 = df.iloc[-2]
        c3 = df.iloc[-3]

        signal = None
        strategy = None
        score = 0

        # ─────────────────────
        # 📈 3 BULLISH
        # ─────────────────────
        bullish_3 = (

            c1["close"] > c1["open"]
            and
            c2["close"] > c2["open"]
            and
            c3["close"] > c3["open"]
        )

        # ─────────────────────
        # 📉 3 BEARISH
        # ─────────────────────
        bearish_3 = (

            c1["close"] < c1["open"]
            and
            c2["close"] < c2["open"]
            and
            c3["close"] < c3["open"]
        )

        # ─────────────────────
        # 🔨 HAMMER
        # ─────────────────────
        body = abs(
            c1["close"] - c1["open"]
        )

        candle = (
            c1["high"] - c1["low"]
        )

        lower_wick = min(
            c1["open"],
            c1["close"]
        ) - c1["low"]

        hammer = (

            lower_wick > body * 2
            and
            body < candle * 0.4
        )

        # ─────────────────────
        # ⭐ MORNING STAR
        # ─────────────────────
        morning_star = (

            c3["close"] < c3["open"]
            and
            abs(c2["close"] - c2["open"]) <
            abs(c3["close"] - c3["open"]) * 0.5
            and
            c1["close"] > c1["open"]
        )

        # ─────────────────────
        # 🌙 EVENING STAR
        # ─────────────────────
        evening_star = (

            c3["close"] > c3["open"]
            and
            abs(c2["close"] - c2["open"]) <
            abs(c3["close"] - c3["open"]) * 0.5
            and
            c1["close"] < c1["open"]
        )

        # ─────────────────────
        # 📊 RSI
        # ─────────────────────
        rsi = last.get("rsi", 50)

        # ─────────────────────
        # 🟢 BUY
        # ─────────────────────
        if bullish_3 and rsi > 50:

            signal = "BUY"
            strategy = "📈 3 BULLISH"
            score = 82

        elif hammer and rsi < 40:

            signal = "BUY"
            strategy = "🔨 HAMMER"
            score = 84

        elif morning_star and rsi < 45:

            signal = "BUY"
            strategy = "⭐ MORNING STAR"
            score = 86

        # ─────────────────────
        # 🔴 SELL
        # ─────────────────────
        elif bearish_3 and rsi < 50:

            signal = "SELL"
            strategy = "📉 3 BEARISH"
            score = 82

        elif evening_star and rsi > 55:

            signal = "SELL"
            strategy = "🌙 EVENING STAR"
            score = 86

        # ❌ NO SIGNAL
        if not signal:
            return None

        # ─────────────────────
        # 📍 ENTRY FILTER
        # ─────────────────────
        entry = "✅ ENTRE POSSIBLE"

        candle_power = abs(
            c1["close"] - c1["open"]
        )

        if candle_power > (
            (c1["high"] - c1["low"]) * 0.8
        ):

            entry = "⚠ ENTRE EN RETARD"

        return {

            "signal": signal,

            "score": score,

            "strategy": strategy,

            "entry": entry
        }

    except Exception as e:

        print("SIGNAL ERROR:", e)

        return None
