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


# 🔐 TOKEN
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise Exception("TOKEN manquant")


# 🧠 ANALYSE MARCHÉ
def run_analysis(symbol: str):

    try:

        df = get_crypto(symbol)

        # ❌ marché indisponible
        if df is None:
            return {"error": "Market unavailable"}

        if len(df) < 20:
            return {"error": "Not enough data"}

        df = add_indicators(df)

        signal = smart_money_signal(df)

        last = df.iloc[-1]
        prev = df.iloc[-2]

        price = round(last["close"], 2)

        change = round(
            ((last["close"] - prev["close"]) / prev["close"]) * 100,
            2
        )

        ema_trend = "UP" if last["ema5"] > last["ema13"] else "DOWN"

        volatility = round(
            (df["high"] - df["low"]).tail(10).mean(),
            2
        )

        volume = round(last["volume"], 2)

        time_now = datetime.now().strftime("%H:%M:%S")

        # ❌ aucun signal
        if not signal:

            return {
                "asset": symbol,
                "price": price,
                "change": change,
                "signal": "NO SIGNAL",
                "trend": ema_trend,
                "rsi": round(last["rsi"], 2),
                "score": 0,
                "volatility": volatility,
                "volume": volume,
                "time": time_now
            }

        # ✅ signal réel
        return {
            "asset": symbol,
            "price": price,
            "change": change,
            "signal": signal["signal"],
            "trend": ema_trend,
            "rsi": signal["rsi"],
            "score": signal["score"],
            "volatility": volatility,
            "volume": volume,
            "time": time_now
        }

    except Exception as e:

        return {"error": str(e)}


# 🚀 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        [
            InlineKeyboardButton("₿ BTC", callback_data="BTCUSDT"),
            InlineKeyboardButton("Ξ ETH", callback_data="ETHUSDT")
        ],

        [
            InlineKeyboardButton("◎ SOL", callback_data="SOLUSDT"),
            InlineKeyboardButton("🟡 BNB", callback_data="BNBUSDT")
        ]
    ]

    await update.message.reply_text(
        "🚀 SMART MONEY BOT\nChoisis un marché :",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# 🔘 bouton handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    symbol = query.data

    await query.edit_message_text(f"📊 Analyse {symbol}...")

    result = run_analysis(symbol)

    # ❌ erreurs
    if "error" in result:

        await query.edit_message_text(f"❌ {result['error']}")
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

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("🚀 BOT STARTED")

app.run_polling()
