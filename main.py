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

print("TOKEN =", TOKEN)

if not TOKEN:
    raise Exception("TOKEN manquant")


# ─────────────────────────────
# 🌍 GLOBALS
# ─────────────────────────────
AUTO_SIGNAL = False

LAST_SIGNAL = None

TOTAL_WINS = 0
TOTAL_LOSSES = 0

USERS = set()

MARKETS = [

    # 🪙 CRYPTO
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "BNBUSDT",

    # 💱 FOREX
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "AUDUSD",
    "USDCAD",
    "NZDUSD"
]

LAST_AUTO_SIGNALS = {}


# ─────────────────────────────
# 📌 COMMANDS
# ─────────────────────────────
async def set_commands(app):

    commands = [

        BotCommand(
            "start",
            "🚀 Open Bot"
        ),

        BotCommand(
            "help",
            "📘 Help"
        ),

        BotCommand(
            "stats",
            "📈 Statistics"
        ),

        BotCommand(
            "auto",
            "⚡ Auto Signal"
        )
    ]

    await app.bot.set_my_commands(commands)


# ─────────────────────────────
# 📱 MENU
# ─────────────────────────────
def persistent_menu():

    keyboard = [

        ["📊 Analyse Market"],

        ["⚡ Auto Signal", "💰 Trade Now"],

        ["📈 Stats", "📘 Help"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        persistent=True
    )


# ─────────────────────────────
# 📊 MARKET MENU
# ─────────────────────────────
def markets_menu():

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "₿ BTCUSDT",
                callback_data="BTCUSDT"
            ),

            InlineKeyboardButton(
                "Ξ ETHUSDT",
                callback_data="ETHUSDT"
            )
        ],

        [
            InlineKeyboardButton(
                "◎ SOLUSDT",
                callback_data="SOLUSDT"
            ),

            InlineKeyboardButton(
                "🟡 BNBUSDT",
                callback_data="BNBUSDT"
            )
        ],

        [
            InlineKeyboardButton(
                "💶 EURUSD",
                callback_data="EURUSD"
            ),

            InlineKeyboardButton(
                "💷 GBPUSD",
                callback_data="GBPUSD"
            )
        ],

        [
            InlineKeyboardButton(
                "💴 USDJPY",
                callback_data="USDJPY"
            ),

            InlineKeyboardButton(
                "🇦🇺 AUDUSD",
                callback_data="AUDUSD"
            )
        ],

        [
            InlineKeyboardButton(
                "🇺🇸 USDCAD",
                callback_data="USDCAD"
            ),

            InlineKeyboardButton(
                "🇳🇿 NZDUSD",
                callback_data="NZDUSD"
            )
        ]
    ])


# ─────────────────────────────
# 📊 ANALYSE
# ─────────────────────────────
def analyze(symbol):

    global LAST_SIGNAL

    try:

        df = get_crypto(symbol)

        if df is None:
            return None

        if len(df) < 5:
            return None

        df = add_indicators(df)

        signal = smart_money_signal(df)

        last = df.iloc[-1]
        prev = df.iloc[-2]

        result = {

            "symbol": symbol,

            "price": round(
                last["close"],
                5
            ),

            "change": round(
                (
                    (
                        last["close"]
                        - prev["close"]
                    )
                    / prev["close"]
                ) * 100,
                2
            ),

            "signal": "NO SIGNAL",

            "rsi": round(
                last.get("rsi", 50),
                2
            ),

            "score": 0,

            "strategy": "NONE",

            "entry": "⚪ WAIT",

            "time": datetime.now().strftime(
                "%H:%M:%S"
            )
        }

        if signal:

            result["signal"] = signal["signal"]

            result["score"] = signal["score"]

            result["strategy"] = signal["strategy"]

            result["entry"] = signal["entry"]

            LAST_SIGNAL = result

        return result

    except Exception as e:

        print("ANALYSE ERROR:", e)

        return None


# ─────────────────────────────
# ⚡ AUTO SIGNAL
# ─────────────────────────────
async def auto_signal_loop(app):

    global AUTO_SIGNAL

    while True:

        try:

            if not AUTO_SIGNAL:

                await asyncio.sleep(2)

                continue

            for symbol in MARKETS:

                result = analyze(symbol)

                if not result:
                    continue

                if result["signal"] == "NO SIGNAL":
                    continue

                signal_key = (

                    f"{result['symbol']}_"
                    f"{result['signal']}_"
                    f"{result['strategy']}"
                )

                if LAST_AUTO_SIGNALS.get(symbol) == signal_key:
                    continue

                LAST_AUTO_SIGNALS[symbol] = signal_key

                emoji = (
                    "🟢"
                    if result["signal"] == "BUY"
                    else "🔴"
                )

                msg = f"""
🚀 AUTO SIGNAL

🪙 {result['symbol']}

{emoji} {result['signal']}

💰 {result['price']}

📊 RSI:
{result['rsi']}

🎯 Accuracy:
{result['score']}%

📈 {result['strategy']}

📍 {result['entry']}

⏰ {result['time']}

📞 @Mr_dflam
"""

                for user_id in USERS:

                    try:

                        await app.bot.send_message(
                            chat_id=user_id,
                            text=msg
                        )

                    except Exception as e:

                        print(e)

            await asyncio.sleep(10)

        except Exception as e:

            print("AUTO ERROR:", e)

            await asyncio.sleep(5)


# ─────────────────────────────
# 🚀 START
# ─────────────────────────────
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    USERS.add(
        update.effective_chat.id
    )

    await update.message.reply_text(
        """
🚀 SMART MONEY AI

🧠 Smart Trading Bot
📊 Auto Signal
💱 Forex + Crypto

📞 @Mr_dflam
""",
        reply_markup=persistent_menu()
    )


# ─────────────────────────────
# 📘 HELP
# ─────────────────────────────
async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        """
📘 HELP

📊 Analyse Market
⚡ Auto Signal
💰 Trade Simulation

⏳ Expiration:
60 seconds
"""
    )


# ─────────────────────────────
# 📈 STATS
# ─────────────────────────────
async def stats_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    total = TOTAL_WINS + TOTAL_LOSSES

    winrate = round(
        (
            TOTAL_WINS / total
        ) * 100,
        2
    ) if total > 0 else 0

    await update.message.reply_text(
        f"""
📈 ACCOUNT STATS

🏆 Wins:
{TOTAL_WINS}

❌ Losses:
{TOTAL_LOSSES}

🎯 Winrate:
{winrate}%
"""
    )


# ─────────────────────────────
# ⚡ AUTO COMMAND
# ─────────────────────────────
async def auto_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    global AUTO_SIGNAL

    AUTO_SIGNAL = not AUTO_SIGNAL

    status = (
        "🟢 ACTIVATED"
        if AUTO_SIGNAL
        else "🔴 DISABLED"
    )

    await update.message.reply_text(
        f"""
⚡ AUTO SIGNAL

📡 STATUS:
{status}
"""
    )


# ─────────────────────────────
# 📱 MENU HANDLER
# ─────────────────────────────
async def text_menu_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    if text == "📊 Analyse Market":

        await update.message.reply_text(
            "📊 SELECT MARKET",
            reply_markup=markets_menu()
        )

    elif text == "⚡ Auto Signal":

        await auto_command(update, context)

    elif text == "📈 Stats":

        await stats_command(update, context)

    elif text == "📘 Help":

        await help_command(update, context)


# ─────────────────────────────
# 🔘 BUTTONS
# ─────────────────────────────
async def handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    symbol = query.data

    result = analyze(symbol)

    if not result:

        await query.edit_message_text(
            "❌ Market unavailable"
        )

        return

    if result["signal"] == "NO SIGNAL":

        await query.edit_message_text(
            f"""
📊 MARKET ANALYSIS

🪙 {result['symbol']}

💰 {result['price']}

⚪ NO SIGNAL

📊 RSI:
{result['rsi']}
"""
        )

        return

    emoji = (
        "🟢"
        if result["signal"] == "BUY"
        else "🔴"
    )

    await query.edit_message_text(
        f"""
🚀 SIGNAL FOUND

🪙 {result['symbol']}

{emoji} {result['signal']}

💰 {result['price']}

📊 RSI:
{result['rsi']}

🎯 Accuracy:
{result['score']}%

📈 {result['strategy']}

📍 {result['entry']}

⏰ {result['time']}
"""
    )


# ─────────────────────────────
# 🚀 STARTUP
# ─────────────────────────────
async def startup(app):

    await set_commands(app)

    asyncio.create_task(
        auto_signal_loop(app)
    )

    print("✅ BOT READY")


# ─────────────────────────────
# ▶ RUN
# ─────────────────────────────
app = Application.builder().token(TOKEN).build()

app.post_init = startup

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("help", help_command)
)

app.add_handler(
    CommandHandler("stats", stats_command)
)

app.add_handler(
    CommandHandler("auto", auto_command)
)

app.add_handler(
    CallbackQueryHandler(handler)
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        text_menu_handler
    )
)

print("🚀 SMART MONEY AI STARTED")

app.run_polling(
    drop_pending_updates=True
    )
