import os
from datetime import datetime

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from market import get_crypto
from indicators import add_indicators
from smart_money_killer import smart_money_signal


# 🔐 TOKEN Railway
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise Exception("❌ TOKEN manquant")


# 🧠 Analyse réelle
def run_analysis(symbol="BTCUSDT"):

    try:

        # 📊 data réel
        df = get_crypto(symbol)

        if df is None or len(df) < 20:
            return None

        # 📈 indicateurs
        df = add_indicators(df)

        # 🚨 stratégie smart money
        signal = smart_money_signal(df)

        last = df.iloc[-1]
        prev = df.iloc[-2]

        # 💰 prix live
        current_price = round(last["close"], 2)

        # 📈 variation %
        change_percent = round(
            ((last["close"] - prev["close"]) / prev["close"]) * 100,
            2
        )

        # ⚡ trend EMA
        ema_trend = (
            "BULLISH"
            if last["ema5"] > last["ema13"]
            else "BEARISH"
        )

        # 📊 volatilité
        volatility = round(
            (df["high"] - df["low"]).tail(10).mean(),
            2
        )

        # 📦 volume
        volume = (
            round(last["volume"], 2)
            if "volume" in df.columns
            else 0
        )

        # ⏰ heure
        now = datetime.now().strftime("%H:%M:%S")

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
                "time": now
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
            "time": now
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [
            InlineKeyboardButton(
                "₿ BTC",
                callback_data="BTCUSDT"
            ),

            InlineKeyboardButton(
                "Ξ ETH",
                callback_data="ETHUSDT"
            )
        ],

        [
            InlineKeyboardButton(
                "◎ SOL",
                callback_data="SOLUSDT"
            ),

            InlineKeyboardButton(
                "🟡 BNB",
                callback_data="BNBUSDT"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚀 SMART MONEY BOT\n\nChoisis une crypto :",
        reply_markup=reply_markup
    )


# 🔘 boutons crypto
async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    symbol = query.data

    await query.edit_message_text(
        f"📊 Analyse de {symbol}..."
    )

    result = run_analysis(symbol)

    # ❌ erreur
    if result is None:

        await query.edit_message_text(
            "❌ Impossible de récupérer le marché"
        )

        return

    if "error" in result:

        await query.edit_message_text(
            f"❌ ERROR:\n{result['error']}"
        )

        return

    # 📊 message final
    msg = f"""
📊 ANALYSE TERMINÉE

🪙 {result['asset']}

💰 Prix: {result['price']}
📈 Variation: {result['change']}%

🟢 Signal: {result['signal']}
⚡ Trend: {result['trend']}
📊 RSI: {result['rsi']}
🎯 Score: {result['score']}%

🌊 Volatility: {result['volatility']}
📦 Volume: {result['volume']}

⏰ Time: {result['time']}
"""

    await query.edit_message_text(msg)


# 🚀 APP
app = Application.builder().token(TOKEN).build()

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CallbackQueryHandler(button_handler)
)

print("🚀 BOT STARTED")

app.run_polling()
