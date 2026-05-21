import os
import asyncio
from datetime import datetime

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    BotCommand
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from market import get_crypto
from indicators import add_indicators
from smart_money_killer import smart_money_signal


# ─────────────────────────────
# 🔐 TOKEN
# ─────────────────────────────
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise Exception("TOKEN manquant")


# ─────────────────────────────
# 🌍 GLOBALS
# ─────────────────────────────
AUTO_SIGNAL = False
LAST_SIGNAL = None

TOTAL_WINS = 0
TOTAL_LOSSES = 0


# ─────────────────────────────
# 📌 COMMANDS
# ─────────────────────────────
async def set_commands(app):
    commands = [
        BotCommand("start", "🚀 Open Smart Money AI"),
        BotCommand("help", "📘 Help Manual"),
        BotCommand("stats", "📈 Statistics"),
        BotCommand("auto", "⚡ Auto Signal"),
        BotCommand("contact", "📞 Contact")
    ]
    await app.bot.set_my_commands(commands)


# ─────────────────────────────
# 📱 MENU
# ─────────────────────────────
def persistent_menu():
    return ReplyKeyboardMarkup(
        [
            ["📊 Analyse Market"],
            ["⚡ Auto Signal", "💰 Trade Now"],
            ["📈 Stats", "📘 Help"],
            ["📞 Contact", "💸 Pocket Option"]
        ],
        resize_keyboard=True
    )


# ─────────────────────────────
# 📊 MARKET MENU
# ─────────────────────────────
def markets_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("₿ BTCUSDT", callback_data="BTCUSDT"),
            InlineKeyboardButton("Ξ ETHUSDT", callback_data="ETHUSDT")
        ],
        [
            InlineKeyboardButton("◎ SOLUSDT", callback_data="SOLUSDT"),
            InlineKeyboardButton("🟡 BNBUSDT", callback_data="BNBUSDT")
        ]
    ])


# ─────────────────────────────
# 📊 ANALYSE (SMART MONEY CORE)
# ─────────────────────────────
def analyze(symbol):
    global LAST_SIGNAL

    try:
        df = get_crypto(symbol)

        if df is None or len(df) < 20:
            return None

        df = add_indicators(df)

        signal = smart_money_signal(df)

        last = df.iloc[-1]
        prev = df.iloc[-2]

        result = {
            "symbol": symbol,
            "price": round(last["close"], 2),
            "change": round(((last["close"] - prev["close"]) / prev["close"]) * 100, 2),
            "signal": "NO SIGNAL",
            "rsi": round(last.get("rsi", 0), 2),
            "score": 0,
            "strategy": "NONE",
            "entry": "⚪ WAIT",
            "time": datetime.now().strftime("%H:%M:%S")
        }

        # ───── SIGNAL FOUND ─────
        if signal:
            result["signal"] = signal.get("signal", "NO SIGNAL")
            result["score"] = signal.get("score", 0)
            result["strategy"] = signal.get("strategy", "NONE")
            result["entry"] = signal.get("entry", "WAIT")

            LAST_SIGNAL = result

        return result

    except Exception as e:
        print("ERROR ANALYSE:", e)
        return None


# ─────────────────────────────
# 🚀 START
# ─────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    await update.message.reply_text(
        """
╔════════════════════╗
🚀 SMART MONEY AI
╚════════════════════╝

🧠 Smart Strategy Engine
📊 Pocket Option Signals
⚡ Auto Trading Simulation
🎯 High Accuracy Scanner

📡 STATUS: ONLINE
""",
        reply_markup=persistent_menu()
    )


# ─────────────────────────────
# 📘 HELP
# ─────────────────────────────
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
📘 HELP

📊 Analyse Market → signal detection
🟢 BUY → bullish trend
🔴 SELL → bearish trend

📍 ENTRY → good moment
⚠️ LATE ENTRY → risky
❌ NO TRADE → dangerous

⏳ Expiration: 1 minute
"""
    )


# ─────────────────────────────
# 📞 CONTACT
# ─────────────────────────────
async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📞 @Mr_dflam")


# ─────────────────────────────
# ⚡ AUTO SIGNAL
# ─────────────────────────────
async def auto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global AUTO_SIGNAL
    AUTO_SIGNAL = not AUTO_SIGNAL

    await update.message.reply_text(
        f"""
⚡ AUTO SIGNAL

STATUS:
{'🟢 ACTIVATED' if AUTO_SIGNAL else '🔴 DISABLED'}
"""
    )


# ─────────────────────────────
# 📈 STATS
# ─────────────────────────────
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total = TOTAL_WINS + TOTAL_LOSSES
    winrate = round((TOTAL_WINS / total) * 100, 2) if total > 0 else 0

    await update.message.reply_text(
        f"""
📈 ACCOUNT STATS

🏆 Wins: {TOTAL_WINS}
❌ Losses: {TOTAL_LOSSES}
🎯 Winrate: {winrate}%
"""
    )


# ─────────────────────────────
# 📱 MENU HANDLER
# ─────────────────────────────
async def text_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global AUTO_SIGNAL, LAST_SIGNAL, TOTAL_WINS, TOTAL_LOSSES

    text = update.message.text

    # 📊 ANALYSE
    if text == "📊 Analyse Market":
        await update.message.reply_text(
            "Select market",
            reply_markup=markets_menu()
        )

    # ⚡ AUTO
    elif text == "⚡ Auto Signal":
        AUTO_SIGNAL = not AUTO_SIGNAL
        await update.message.reply_text(f"AUTO: {'ON' if AUTO_SIGNAL else 'OFF'}")

    # 💰 TRADE
    elif text == "💰 Trade Now":

        if not LAST_SIGNAL:
            await update.message.reply_text("⚠ No active signal")
            return

        symbol = LAST_SIGNAL["symbol"]
        direction = LAST_SIGNAL["signal"]
        entry_price = LAST_SIGNAL["price"]

        await update.message.reply_text(
            f"""
💰 TRADE OPENED

{symbol}
{direction}

ENTRY: {entry_price}
"""
        )

        await asyncio.sleep(60)

        df = get_crypto(symbol)
        exit_price = round(df.iloc[-1]["close"], 2)

        result_trade = "DRAW"

        if direction == "BUY":
            result_trade = "WIN ✔" if exit_price > entry_price else "LOSS ❌"
        elif direction == "SELL":
            result_trade = "WIN ✔" if exit_price < entry_price else "LOSS ❌"

        if "WIN" in result_trade:
            TOTAL_WINS += 1
        elif "LOSS" in result_trade:
            TOTAL_LOSSES += 1

        total = TOTAL_WINS + TOTAL_LOSSES
        winrate = round((TOTAL_WINS / total) * 100, 2) if total else 0

        await update.message.reply_text(
            f"""
💰 TRADE CLOSED

{symbol}
{direction}

ENTRY: {entry_price}
EXIT: {exit_price}

RESULT: {result_trade}

🏆 Wins: {TOTAL_WINS}
❌ Losses: {TOTAL_LOSSES}
🎯 Winrate: {winrate}%
"""
        )

    elif text == "📈 Stats":
        await stats_command(update, context)

    elif text == "📘 Help":
        await help_command(update, context)

    elif text == "📞 Contact":
        await contact_command(update, context)

    elif text == "💸 Pocket Option":
        await update.message.reply_text("https://pocketoption.com")


# ─────────────────────────────
# 🔘 CALLBACK
# ─────────────────────────────
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    symbol = query.data
    result = analyze(symbol)

    if not result:
        await query.edit_message_text("❌ No data")
        return

    if result["signal"] == "NO SIGNAL":
        await query.edit_message_text(
            f"""
📊 MARKET ANALYSIS

{symbol}
NO SIGNAL
RSI: {result['rsi']}
"""
        )
        return

    emoji = "🟢" if result["signal"] == "BUY" else "🔴"

    await query.edit_message_text(
        f"""
🚀 SIGNAL FOUND

{symbol}
{emoji} {result["signal"]}

PRICE: {result["price"]}
RSI: {result["rsi"]}
SCORE: {result["score"]}%

STRATEGY: {result["strategy"]}
ENTRY: {result["entry"]}

⏰ {result["time"]}
"""
    )


# ─────────────────────────────
# 🚀 STARTUP
# ─────────────────────────────
async def startup(app):
    await set_commands(app)
    print("✅ BOT READY")


# ─────────────────────────────
# ▶ RUN BOT
# ─────────────────────────────
app = Application.builder().token(TOKEN).build()

app.post_init = startup

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("stats", stats_command))
app.add_handler(CommandHandler("auto", auto_command))
app.add_handler(CommandHandler("contact", contact_command))

app.add_handler(CallbackQueryHandler(handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_menu_handler))

print("🚀 SMART MONEY AI STARTED")

app.run_polling(drop_pending_updates=True)
