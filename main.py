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


TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise Exception("TOKEN manquant")


# 🔥 AUTO STATE GLOBAL
AUTO_SIGNAL = False
CURRENT_SYMBOL = "BTCUSDT"


# 🧠 ANALYSE
def run_analysis(symbol):

    df = get_crypto(symbol)
    if df is None or len(df) < 20:
        return None

    df = add_indicators(df)
    signal = smart_money_signal(df)

    if not signal:
        return None

    last = df.iloc[-1]
    prev = df.iloc[-2]

    return {
        "asset": symbol,
        "price": round(last["close"], 2),
        "change": round(((last["close"] - prev["close"]) / prev["close"]) * 100, 2),
        "signal": signal["signal"],
        "rsi": signal["rsi"],
        "score": signal["score"],
        "time": datetime.now().strftime("%H:%M:%S")
    }


# 📊 MENU BOUTONS
def main_keyboard():

    status = "ON 🔥" if AUTO_SIGNAL else "OFF ⚪"

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("BTC", callback_data="BTCUSDT"),
            InlineKeyboardButton("ETH", callback_data="ETHUSDT")
        ],
        [
            InlineKeyboardButton("SOL", callback_data="SOLUSDT"),
            InlineKeyboardButton("BNB", callback_data="BNBUSDT")
        ],
        [
            InlineKeyboardButton(f"Auto Signal {status}", callback_data="TOGGLE_AUTO")
        ]
    ])


# 🚀 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🚀 SMART MONEY BOT\nChoisis un marché :",
        reply_markup=main_keyboard()
    )


# 📊 /help
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("""
📌 HELP

✔ Clique sur un marché pour analyser
✔ Active Auto Signal pour recevoir BUY/SELL
✔ Bot basé sur Smart Money + RSI

@Mr_dflam
""")


# 📊 /status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global AUTO_SIGNAL, CURRENT_SYMBOL

    await update.message.reply_text(f"""
📊 STATUS BOT

🔥 Auto Signal: {"ON" if AUTO_SIGNAL else "OFF"}
🪙 Symbol: {CURRENT_SYMBOL}
⏰ Time: {datetime.now().strftime("%H:%M:%S")}

@Mr_dflam
""")


# 🔘 BUTTONS
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global AUTO_SIGNAL, CURRENT_SYMBOL

    query = update.callback_query
    await query.answer()

    data = query.data

    # 🔥 TOGGLE AUTO
    if data == "TOGGLE_AUTO":

        AUTO_SIGNAL = not AUTO_SIGNAL

        await query.edit_message_text(
            f"Auto Signal {'ACTIVÉ 🔥' if AUTO_SIGNAL else 'DÉSACTIVÉ ⚪'}",
            reply_markup=main_keyboard()
        )
        return

    # 📊 SELECT SYMBOL
    CURRENT_SYMBOL = data

    result = run_analysis(data)

    if not result:
        await query.edit_message_text("⚪ Aucun signal")
        return

    msg = f"""
📊 ANALYSE TERMINÉE

🪙 {result['asset']}
💰 {result['price']}
📈 {result['change']}%

🟢 {result['signal']}
📊 RSI: {result['rsi']}
🎯 Score: {result['score']}%

⏰ {result['time']}

@Mr_dflam
"""

    await query.edit_message_text(msg, reply_markup=main_keyboard())


# ▶ BOT
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("status", status))
app.add_handler(CallbackQueryHandler(button_handler))

print("🚀 BOT READY")

app.run_polling()
