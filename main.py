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


# 🔥 STATE
AUTO_SIGNAL = False


# 🧠 ANALYSE SIMPLE
def analyze(symbol):

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
        "symbol": symbol,
        "price": round(last["close"], 2),
        "change": round(((last["close"] - prev["close"]) / prev["close"]) * 100, 2),
        "signal": signal["signal"],
        "rsi": signal["rsi"],
        "score": signal["score"],
        "time": datetime.now().strftime("%H:%M:%S")
    }


# 📊 DASHBOARD PAGE
def dashboard_menu():

    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Markets", callback_data="PAGE_MARKETS")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="PAGE_SETTINGS")]
    ])


# 📈 MARKETS PAGE
def markets_menu():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("BTC", callback_data="BTCUSDT"),
            InlineKeyboardButton("ETH", callback_data="ETHUSDT")
        ],
        [
            InlineKeyboardButton("SOL", callback_data="SOLUSDT"),
            InlineKeyboardButton("BNB", callback_data="BNBUSDT")
        ],
        [InlineKeyboardButton("⬅ Back", callback_data="PAGE_HOME")]
    ])


# ⚙️ SETTINGS PAGE
def settings_menu():

    status = "ON 🔥" if AUTO_SIGNAL else "OFF ⚪"

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"Auto Signal {status}", callback_data="TOGGLE_AUTO")],
        [InlineKeyboardButton("📊 Help", callback_data="HELP")],
        [InlineKeyboardButton("⬅ Back", callback_data="PAGE_HOME")]
    ])


# 🚀 /start = HOME PAGE
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🚀 TRADING APP DASHBOARD",
        reply_markup=dashboard_menu()
    )


# 🔘 NAVIGATION SYSTEM
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global AUTO_SIGNAL

    query = update.callback_query
    await query.answer()

    data = query.data


    # 🏠 HOME
    if data == "PAGE_HOME":
        await query.edit_message_text("🏠 DASHBOARD", reply_markup=dashboard_menu())
        return


    # 📊 MARKETS PAGE
    if data == "PAGE_MARKETS":
        await query.edit_message_text("📈 MARKETS", reply_markup=markets_menu())
        return


    # ⚙️ SETTINGS PAGE
    if data == "PAGE_SETTINGS":
        await query.edit_message_text("⚙️ SETTINGS", reply_markup=settings_menu())
        return


    # 🔥 TOGGLE AUTO
    if data == "TOGGLE_AUTO":
        AUTO_SIGNAL = not AUTO_SIGNAL
        await query.edit_message_text(
            f"Auto Signal {'ON 🔥' if AUTO_SIGNAL else 'OFF ⚪'}",
            reply_markup=settings_menu()
        )
        return


    # 📊 MARKET ANALYSIS
    result = analyze(data)

    if not result:
        await query.edit_message_text("⚪ No signal", reply_markup=markets_menu())
        return

    msg = f"""
📊 SMART MONEY

🪙 {result['symbol']}
💰 {result['price']}
📈 {result['change']}%

🟢 {result['signal']}
📊 RSI: {result['rsi']}
🎯 Score: {result['score']}

⏰ {result['time']}
"""

    await query.edit_message_text(msg, reply_markup=markets_menu())


# ▶ BOT
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handler))

print("🚀 TRADING APP BOT READY")

app.run_polling()
