# ─────────────────────────────
# 🚀 SMART MONEY SIGNAL
# ─────────────────────────────
def smart_money_signal(df):

    try:

        if len(df) < 5:
            return None

        # ─────────────────────
        # 📊 CANDLES
        # ─────────────────────
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

        lower_wick = min(
            c1["open"],
            c1["close"]
        ) - c1["low"]

        hammer = (

            lower_wick > body * 2
        )

        # ─────────────────────
        # ⭐ MORNING STAR
        # ─────────────────────
        morning_star = (

            c3["close"] < c3["open"]
            and
            c2["close"] > c2["open"]
            and
            c1["close"] > c1["open"]
        )

        # ─────────────────────
        # 🌙 EVENING STAR
        # ─────────────────────
        evening_star = (

            c3["close"] > c3["open"]
            and
            c2["close"] < c2["open"]
            and
            c1["close"] < c1["open"]
        )

        # ─────────────────────
        # 📊 RSI
        # ─────────────────────
        rsi = c1.get("rsi", 50)

        # ─────────────────────
        # 🟢 BUY SIGNALS
        # ─────────────────────
        if bullish_3 and rsi >= 48:

            signal = "BUY"
            strategy = "📈 3 BULLISH"
            score = 85

        elif hammer and rsi <= 45:

            signal = "BUY"
            strategy = "🔨 HAMMER"
            score = 88

        elif morning_star:

            signal = "BUY"
            strategy = "⭐ MORNING STAR"
            score = 90

        # ─────────────────────
        # 🔴 SELL SIGNALS
        # ─────────────────────
        elif bearish_3 and rsi <= 52:

            signal = "SELL"
            strategy = "📉 3 BEARISH"
            score = 85

        elif evening_star:

            signal = "SELL"
            strategy = "🌙 EVENING STAR"
            score = 90

        # ❌ NO SIGNAL
        if not signal:

            return None

        # ─────────────────────
        # 📍 ENTRY FILTER
        # ─────────────────────
        entry = "✅ ENTRE POSSIBLE"

        candle_size = abs(
            c1["close"] - c1["open"]
        )

        full_size = (
            c1["high"] - c1["low"]
        )

        # ⚠ TOO LATE
        if candle_size > full_size * 0.8:

            entry = "⚠ ENTRE EN RETARD"

        # ❌ FLAT MARKET
        if full_size < 0.02:

            entry = "❌ NE PAS ENTRER"

        # ─────────────────────
        # ✅ RESULT
        # ─────────────────────
        return {

            "signal": signal,

            "score": score,

            "strategy": strategy,

            "entry": entry
        }

    except Exception as e:

        print(
            "SMART MONEY ERROR:",
            e
        )

        return None
