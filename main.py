import os
import asyncio
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


# 🧠 ANALYSE PROPRE (AUTO SIGNAL ONLY)
def run_analysis(symbol: str):

    try:
        df = get_crypto(symbol)

        if df is None or len(df) < 20:
            return None  # ❌ pas de bruit

        df = add_indicators(df)

        signal = smart_money_signal(df)

        if not signal:
            return None  # ❌ ON CACHE NO SIGNAL

        last = df.iloc[-1]
        prev = df.iloc[-2]

        price = round(last["close"], 2)

        change = round(
            ((last["close"] - prev["close"]) / prev["close"]) * 100,
            2
        )

        ema_trend = "UP" if last["ema5"] > last["ema13"] else "DOWN"

        return {
            "asset": symbol,
            "price": price,
            "change": change,
            "signal": signal["signal"],
            "trend": ema_trend,
            "rsi": signal["rsi"],
            "score": signal["score"],
            "confidence": signal["confidence"],
            "time": datetime.now().strftime("%H:%M:%S")
        }

    except:
        return None


# 🚀 /start (UI CLEAN)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("BTC", callback_data="BTCUSDT"),
            InlineKeyboardButton("ETH", callback_data="ETHUSDT")
        ],
        [
            InlineKeyboardButton("SOL", callback_data="SOLUSDT"),
            InlineKeyboardButton("BNB", callback_data="BNBUSDT")
        ],
        [
            InlineKeyboardButton("🔥 AUTO SIGNAL BTC", callback_data="AUTO_BTCUSDT")
        ]
    ]

    await update.message.reply_text(
        "🚀 SMART MONEY BOT\nChoisis un marché :",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# 🔥 AUTO SIGNAL LOOP (NEW)
async def auto_signal_loop(context: ContextTypes.DEFAULT_TYPE):

    job = context.job
    chat_id = job.chat_id
    symbol = job.data["symbol"]

    result = run_analysis(symbol)

    if not result:
        return  # ❌ RIEN A AFFICHER

    msg = f"""
🚀 AUTO SIGNAL

🪙 {result['asset']}
💰 {result['price']} ({result['change']}%)

🟢 {result['signal']}
📊 RSI: {result['rsi']}
🎯 Score: {result['score']}%
🔥 {result['confidence']}

⏰ {result['time']}
"""

    await context.bot.send_message(chat_id=chat_id, text=msg)


# 🔘 BUTTON HANDLER
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    # 🔥 AUTO MODE
    if data.startswith("AUTO_"):

        symbol = data.replace("AUTO_", "")
        chat_id = query.message.chat_id

        # stop ancien job si existe
        for job in context.job_queue.get_jobs_by_name(str(chat_id)):
            job.schedule_removal()

        context.job_queue.run_repeating(
            auto_signal_loop,
            interval=8,
            first=1,
            chat_id=chat_id,
            data={"symbol": symbol},
            name=str(chat_id)
        )

        await query.edit_message_text(f"🔥 AUTO SIGNAL ACTIVÉ: {symbol}")
        return

    # 📊 MANUAL ANALYSIS
    result = run_analysis(data)

    if not result:
        await query.edit_message_text("⚪ Aucun signal pour le moment")
        return

    msg = f"""
🚀 ANALYSE

🪙 {result['asset']}
💰 {result['price']}
📈 {result['change']}%

🟢 {result['signal']}
⚡ {result['trend']}
📊 RSI: {result['rsi']}
🎯 Score: {result['score']}%
🔥 {result['confidence']}

⏰ {result['time']}
"""

    await query.edit_message_text(msg)


# ▶ BOT
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("🚀 BOT CLEAN STARTED")

app.run_polling()
