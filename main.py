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


# 🔥 STATE
AUTO_SIGNAL = False


# ─────────────────────────────
# 🧠 ANALYSE
# ─────────────────────────────
def analyze(symbol):

    try:
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

    except:
        return None


# ─────────────────────────────
# 📘 HELP COMPLET
# ─────────────────────────────
HELP_TEXT = """
━━━━━━━━━━━━━━━━━━━━
📘 SMART MONEY BOT
━━━━━━━━━━━━━━━━━━━━

🧠 ANALYSE :
Le bot utilise :
• RSI (force marché)
• EMA (trend)
• Volatility
• Smart Money logic

━━━━━━━━━━━━━━━━━━━━
📊 SIGNALS :
🟢 BUY → pression acheteuse
🔴 SELL → pression vendeuse
⚪ Aucun signal = marché instable

━━━━━━━━━━━━━━━━━━━━
⚡ AUTO SIGNAL :
• analyse automatique
• envoi uniquement signaux forts
• filtre bruit marché

━━━━━━━━━━━━━━━━━━━━
📈 STRATEGY :
• confirmation trend obligatoire
• RSI zones extrêmes
• Smart Money validation

━━━━━━━━━━━━━━━━━━━━
📞 CONTACT :
@Mr_dflam
━━━━━━━━━━━━━━━━━━━━
"""


# ─────────────────────────────
# 🏠 DASHBOARD
# ─────────────────────────────
def dashboard():

    status = "🟢 ON" if AUTO_SIGNAL else "🔴 OFF"

    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 MARKET ANALYSIS", callback_data="PAGE_MARKETS")],
        [InlineKeyboardButton("⚡ AUTO SIGNAL", callback_data="PAGE_SIGNALS")],
        [InlineKeyboardButton("⚙️ SETTINGS", callback_data="PAGE_SETTINGS")],
        [InlineKeyboardButton(f"🔥 STATUS: {status}", callback_data="STATUS")],
        [InlineKeyboardButton("📞 CONTACT", url="https://t.me/Mr_dflam")]
    ])


# ─────────────────────────────
# 📊 MARKETS
# ─────────────────────────────
def markets():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("₿ BTCUSDT", callback_data="BTCUSDT"),
            InlineKeyboardButton("Ξ ETHUSDT", callback_data="ETHUSDT")
        ],
        [
            InlineKeyboardButton("◎ SOLUSDT", callback_data="SOLUSDT"),
            InlineKeyboardButton("🟡 BNBUSDT", callback_data="BNBUSDT")
        ],
        [InlineKeyboardButton("⬅ BACK", callback_data="PAGE_HOME")]
    ])


# ─────────────────────────────
# ⚙️ SETTINGS
# ─────────────────────────────
def settings():

    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 BOT STATUS", callback_data="STATUS")],
        [InlineKeyboardButton("📘 HELP", callback_data="HELP")],
        [InlineKeyboardButton("📞 CONTACT @Mr_dflam", url="https://t.me/Mr_dflam")],
        [InlineKeyboardButton("⬅ BACK", callback_data="PAGE_HOME")]
    ])


# ─────────────────────────────
# 🚀 START
# ─────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🚀 SMART MONEY TRADING APP\nBienvenue sur le dashboard",
        reply_markup=dashboard()
    )


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


    # 📘 HELP
    if data == "HELP":
        await query.edit_message_text(HELP_TEXT, reply_markup=settings())
        return


    # 📊 STATUS
    if data == "STATUS":
        await query.edit_message_text(
            f"""
📊 BOT STATUS

⚡ Auto Signal: {"ON" if AUTO_SIGNAL else "OFF"}
⏰ Time: {datetime.now().strftime("%H:%M:%S")}

📞 @Mr_dflam
""",
            reply_markup=settings()
        )
        return


    # ⚡ PAGE SIGNALS (placeholder)
    if data == "PAGE_SIGNALS":
        await query.edit_message_text(
            "⚡ SIGNAL CENTER (LIVE COMING SOON)",
            reply_markup=dashboard()
        )
        return


    # 📊 ANALYSE MARKET
    result = analyze(data)

    if not result:
        await query.edit_message_text("⚪ No strong signal", reply_markup=markets())
        return

    msg = f"""
━━━━━━━━━━━━━━━━━━━━
📊 SMART MONEY SIGNAL
━━━━━━━━━━━━━━━━━━━━

🪙 {result['symbol']}
💰 {result['price']}
📈 {result['change']}%

🟢 {result['signal']}
📊 RSI: {result['rsi']}
🎯 SCORE: {result['score']}

⏰ {result['time']}

📞 @Mr_dflam
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
