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


# ─────────────────────────────
# 🧠 ANALYSE
# ─────────────────────────────
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


# ─────────────────────────────
# 🏠 DASHBOARD (HOME)
# ─────────────────────────────
def dashboard():

    status = "🟢 ON" if AUTO_SIGNAL else "🔴 OFF"

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📊 Markets", callback_data="PAGE_MARKETS"),
            InlineKeyboardButton("⚡ Signals", callback_data="PAGE_SIGNALS")
        ],
        [
            InlineKeyboardButton("⚙️ Settings", callback_data="PAGE_SETTINGS")
        ],
        [
            InlineKeyboardButton(f"Auto Signal {status}", callback_data="TOGGLE_AUTO")
        ]
    ])


# ─────────────────────────────
# 📊 MARKETS PAGE
# ─────────────────────────────
def markets():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("₿ BTC", callback_data="BTCUSDT"),
            InlineKeyboardButton("Ξ ETH", callback_data="ETHUSDT")
        ],
        [
            InlineKeyboardButton("◎ SOL", callback_data="SOLUSDT"),
            InlineKeyboardButton("🟡 BNB", callback_data="BNBUSDT")
        ],
        [InlineKeyboardButton("⬅ Home", callback_data="PAGE_HOME")]
    ])


# ─────────────────────────────
# ⚙️ SETTINGS PAGE
# ─────────────────────────────
def settings():

    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Status", callback_data="STATUS")],
        [InlineKeyboardButton("📘 Help", callback_data="HELP")],
        [InlineKeyboardButton("⬅ Home", callback_data="PAGE_HOME")]
    ])


# ─────────────────────────────
# 🚀 START
# ─────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = """
🚀 SMART MONEY TRADING APP

📊 Analyse Crypto en temps réel
⚡ Signaux BUY / SELL
🔥 Auto Signal disponible
"""

    await update.message.reply_text(msg, reply_markup=dashboard())


# ─────────────────────────────
# 🔘 HANDLER
# ─────────────────────────────
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global AUTO_SIGNAL

    query = update.callback_query
    await query.answer()

    data = query.data


    # 🏠 HOME
    if data == "PAGE_HOME":
        await query.edit_message_text("🏠 DASHBOARD", reply_markup=dashboard())
        return


    # 📊 MARKETS
    if data == "PAGE_MARKETS":
        await query.edit_message_text("📊 MARKETS", reply_markup=markets())
        return


    # ⚙️ SETTINGS
    if data == "PAGE_SETTINGS":
        await query.edit_message_text("⚙️ SETTINGS", reply_markup=settings())
        return


    # ⚡ SIGNALS (placeholder futur)
    if data == "PAGE_SIGNALS":
        await query.edit_message_text(
            "⚡ SIGNAL CENTER\n(Bientôt auto alerts)",
            reply_markup=dashboard()
        )
        return


    # 🔥 AUTO TOGGLE
    if data == "TOGGLE_AUTO":
        AUTO_SIGNAL = not AUTO_SIGNAL

        await query.edit_message_text(
            f"Auto Signal {'🟢 ACTIVÉ' if AUTO_SIGNAL else '🔴 DÉSACTIVÉ'}",
            reply_markup=dashboard()
        )
        return


    # 📊 STATUS
    if data == "STATUS":

        await query.edit_message_text(
            f"""
📊 BOT STATUS

⚡ Auto Signal: {"ON" if AUTO_SIGNAL else "OFF"}
⏰ Time: {datetime.now().strftime("%H:%M:%S")}

📡 System: Active
""",
            reply_markup=settings()
        )
        return


    # 📊 MARKET ANALYSIS
    result = analyze(data)

    if not result:
        await query.edit_message_text("⚪ No signal", reply_markup=markets())
        return


    msg = f"""
━━━━━━━━━━━━━━
📊 SMART MONEY SIGNAL
━━━━━━━━━━━━━━

🪙 {result['symbol']}
💰 {result['price']}
📈 {result['change']}%

━━━━━━━━━━━━━━
🟢 {result['signal']}
⚡ RSI: {result['rsi']}
🎯 SCORE: {result['score']}
━━━━━━━━━━━━━━

⏰ {result['time']}
"""

    await query.edit_message_text(msg, reply_markup=markets())


# ─────────────────────────────
# ▶ RUN BOT
# ─────────────────────────────
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handler))

print("🚀 PRO TRADING APP READY")

app.run_polling()
