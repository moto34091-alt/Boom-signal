from market import get_crypto
from indicators import add_indicators
from smart_money_killer import smart_money_signal
from datetime import datetime


def run_analysis(symbol="BTCUSDT"):

    try:

        # 📊 récupération marché réel
        df = get_crypto(symbol)

        if df is None or len(df) < 20:
            return {
                "error": "Market data unavailable"
            }

        # 📈 indicateurs
        df = add_indicators(df)

        # 🧠 stratégie smart money
        signal = smart_money_signal(df)

        # 📌 dernière bougie
        last = df.iloc[-1]
        prev = df.iloc[-2]

        # 💰 prix live
        current_price = round(last["close"], 2)

        # 📊 variation %
        change_percent = round(
            ((last["close"] - prev["close"]) / prev["close"]) * 100,
            2
        )

        # ⚡ EMA trend
        ema_trend = (
            "BULLISH"
            if last["ema5"] > last["ema13"]
            else "BEARISH"
        )

        # 🌊 volatilité
        volatility = round(
            (df["high"] - df["low"]).tail(10).mean(),
            2
        )

        # 📈 volume
        volume = (
            round(last["volume"], 2)
            if "volume" in df.columns
            else 0
        )

        # ⏰ heure analyse
        analysis_time = datetime.now().strftime("%H:%M:%S")

        # ❌ aucun signal
        if not signal:

            return {
                "asset": symbol,
                "price": current_price,
                "change": change_percent,
                "signal": "NO SIGNAL",
                "trend": ema_trend,
                "rsi": round(last["rsi"], 2),
                "score": 0,
                "volatility": volatility,
                "volume": volume,
                "time": analysis_time
            }

        # ✅ signal réel
        return {
            "asset": symbol,
            "price": current_price,
            "change": change_percent,
            "signal": signal["signal"],
            "trend": ema_trend,
            "rsi": signal["rsi"],
            "score": signal["score"],
            "volatility": volatility,
            "volume": volume,
            "time": analysis_time
        }

    except Exception as e:

        return {
            "error": str(e)
        }
