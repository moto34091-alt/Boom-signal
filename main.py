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
# 🏠 DASHBOARD (APP STYLE)
# ─────────────────────────────
def dashboard():

    status = "🟢 ON" if AUTO_SIGNAL else "🔴 OFF"

    return InlineKeyboardMarkup([
        # 📊 MAIN ACTIONS
        [InlineKeyboardButton("📊 MARKET ANALYSIS", callback_data="PAGE_MARKETS")],
        [InlineKeyboardButton("⚡ AUTO SIGNAL", callback_data="PAGE_SIGNALS")],

        # ⚙️ SETTINGS
        [InlineKeyboardButton("⚙️ SETTINGS", callback_data="PAGE_SETTINGS")],

        # 🔥 STATUS
        [InlineKeyboardButton(f"🔥 BOT STATUS: {status}", callback_data="STATUS")],

        # 💰 TRADE NOW (SIMULATION)
        [InlineKeyboardButton("💰 TRADE NOW (SIMULATION)", callback_data="TRADE")],

        # 💰 POCKET OPTION
        [InlineKeyboardButton("💰 POCKET OPTION", url="https://pocketoption.com")],

        # 📞 CONTACT
        [InlineKeyboardButton("📞 CONTACT @Mr_dflam", url="https://t.me/Mr_dflam")]
    ])


# ─────────────────────────────
# 📊 MARKETS
# ─────────────────────────────
def markets():

    return InlineKeyboardMarkup([
        [InlineKeyboardButton("₿ BTCUSDT", callback_data="BTCUSDT")],
        [InlineKeyboardButton("Ξ ETHUSDT", callback_data="ETHUSDT")],
        [InlineKeyboardButton("◎ SOLUSDT", callback_data="SOLUSDT")],
        [InlineKeyboardButton("🟡 BNBUSDT", callback_data="BNBUSDT")],
        [InlineKeyboardButton("⬅ BACK", callback_data="PAGE_HOME")]
    ])


# ─────────────────────────────
# ⚙️ SETTINGS
# ─────────────────────────────
def settings():

    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 BOT STATUS", callback_data="STATUS")],
        [InlineKeyboardButton("📘 HOW IT WORKS", callback_data="HELP")],
        [InlineKeyboardButton("💰 POCKET OPTION", url="https://pocketoption.com")],
        [InlineKeyboardButton("📞 CONTACT @Mr_dflam", url="https://t.me/Mr_dflam")],
        [InlineKeyboardButton("⬅ BACK", callback_data="PAGE_HOME")]
    ])


# ─────────────────────────────
# 📘 HELP FULL LOGIC
# ─────────────────────────────
HELP_TEXT = """
━━━━━━━━━━━━━━━━━━━━
📘 SMART MONEY BOT
━━━━━━━━━━━━━━━━━━━━

🧠 HOW IT WORKS:
• RSI = momentum
• EMA = trend direction
• Volume = strength
• Smart Money = liquidity traps

━━━━━━━━━━━━━━━━━━━━
📊 SIGNALS:
🟢 BUY = bullish pressure
🔴 SELL = bearish pressure
⚪ NO SIGNAL = market unstable

━━━━━━━━━━━━━━━━━━━━
⚡ AUTO SIGNAL:
• scans market automatically
• sends ONLY strong signals
• filters fake moves

━━━━━━━━━━━━━━━━━━━━
💰 TRADING:
• signals = entry confirmation
• use Pocket Option for execution

━━━━━━━━━━━━━━━━━━━━
📞 CONTACT:
@Mr_dflam
━━━━━━━━━━━━━━━━━━━━
"""


# ─────────────────────────────
# 🚀 START
# ─────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = """
🚀 SMART MONEY TRADING APP

📊 Analyse crypto en temps réel
⚡ Signaux BUY / SELL
🔥 Auto Signal intégré
💰 Simulation trading disponible
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

💰 System Active
""",
            reply_markup=settings()
        )
        return


    # 💰 TRADE NOW SIMULATION
    if data == "TRADE":

        await query.edit_message_text(
            """
💰 TRADE NOW (SIMULATION)

📊 Analysis in progress...
⚡ Waiting for best entry...

🟢 This is a demo trade button
💡 Use signals for confirmation

@Mr_dflam
""",
            reply_markup=dashboard()
        )
        return


    # 📊 MARKET ANALYSIS
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

💰 POCKET OPTION READY
📞 @Mr_dflam
"""

    await query.edit_message_text(msg, reply_markup=markets())


# ─────────────────────────────
# ▶ RUN BOT
# ─────────────────────────────
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handler))

print("🚀 PRO TRADING APP FINAL READY")

app.run_polling()
