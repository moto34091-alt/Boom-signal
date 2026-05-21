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
# 📌 BOT COMMANDS
# ─────────────────────────────
async def set_commands(app):

    commands = [

        BotCommand(
            "start",
            "🚀 Open Smart Money AI"
        ),

        BotCommand(
            "help",
            "📘 Help Manual"
        ),

        BotCommand(
            "stats",
            "📈 Statistics"
        ),

        BotCommand(
            "auto",
            "⚡ Auto Signal"
        ),

        BotCommand(
            "contact",
            "📞 Contact"
        )
    ]

    await app.bot.set_my_commands(commands)


# ─────────────────────────────
# 📱 PERSISTENT MENU
# ─────────────────────────────
def persistent_menu():

    keyboard = [

        ["📊 Analyse Market"],

        ["⚡ Auto Signal", "💰 Trade Now"],

        ["📈 Stats", "📘 Help"],

        ["📞 Contact", "💸 Pocket Option"]
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
        ]
    ])


# ─────────────────────────────
# 📊 ANALYSE
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

            "price": round(
                last["close"],
                2
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
                last.get("rsi", 0),
                2
            ),

            "score": 0,

            "strategy": "NONE",

            "entry": "⚪ WAIT",

            "time": datetime.now().strftime(
                "%H:%M:%S"
            )
        }

        # ✅ SIGNAL
        if signal:

            result["signal"] = signal["signal"]

            result["score"] = signal["score"]

            result["strategy"] = signal["strategy"]

            result["entry"] = signal["entry"]

            LAST_SIGNAL = result

        return result

    except Exception as e:

        print("ERROR:", e)

        return None


# ─────────────────────────────
# 🚀 START
# ─────────────────────────────
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = """
╔════════════════════╗
      🚀 SMART MONEY AI
╚════════════════════╝

🧠 Smart Strategy Engine
📊 Pocket Option Signals
⚡ Auto Trading Simulation
🎯 High Accuracy Scanner

━━━━━━━━━━━━━━━━━━━━

📈 Hammer Strategy
📈 Morning Star
📈 Evening Star
📈 3 Bullish
📈 3 Bearish

━━━━━━━━━━━━━━━━━━━━

📡 STATUS:
🟢 ONLINE

📞 @Mr_dflam
"""

    await update.message.reply_text(
        text,
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
╔════════════════════╗
        📘 HELP
╚════════════════════╝

📊 Analyse market
→ détecte stratégie active

🟢 BUY
→ tendance haussière

🔴 SELL
→ tendance baissière

📍 ENTRÉE POSSIBLE
→ bon moment

⚠️ ENTRÉE EN RETARD
→ mouvement avancé

❌ NE PAS ENTRER
→ signal dangereux

━━━━━━━━━━━━━━━━━━━━

⏳ Expiration:
1 minute

📞 Contact:
@Mr_dflam
"""
    )


# ─────────────────────────────
# 📞 CONTACT
# ─────────────────────────────
async def contact_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        """
📞 SUPPORT

👤 @Mr_dflam
"""
    )


# ─────────────────────────────
# ⚡ AUTO SIGNAL
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
━━━━━━━━━━━━━━━━━━━━
⚡ AUTO SIGNAL
━━━━━━━━━━━━━━━━━━━━

📡 STATUS:
{status}
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
        (TOTAL_WINS / total) * 100,
        2
    ) if total > 0 else 0

    await update.message.reply_text(
        f"""
━━━━━━━━━━━━━━━━━━━━
📈 ACCOUNT STATS
━━━━━━━━━━━━━━━━━━━━

🏆 Wins: {TOTAL_WINS}

❌ Losses: {TOTAL_LOSSES}

🎯 Winrate: {winrate}%

📞 @Mr_dflam
"""
    )


# ─────────────────────────────
# 📱 TEXT MENU HANDLER
# ─────────────────────────────
async def text_menu_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text


    # 📊 ANALYSE
    if text == "📊 Analyse Market":

        await update.message.reply_text(
            """
━━━━━━━━━━━━━━━━━━━━
📊 SELECT MARKET
━━━━━━━━━━━━━━━━━━━━

Choose asset
""",
            reply_markup=markets_menu()
        )


    # ⚡ AUTO
    elif text == "⚡ Auto Signal":

        global AUTO_SIGNAL

        AUTO_SIGNAL = not AUTO_SIGNAL

        status = (
            "🟢 ON"
            if AUTO_SIGNAL
            else "🔴 OFF"
        )

        await update.message.reply_text(
            f"""
━━━━━━━━━━━━━━━━━━━━
⚡ AUTO SIGNAL
━━━━━━━━━━━━━━━━━━━━

📡 STATUS:
{status}
"""
        )


    # 💰 TRADE
    elif text == "💰 Trade Now":

        if not LAST_SIGNAL:

            await update.message.reply_text(
                """
⚠ Aucun signal actif

📊 Analyse d'abord un marché
"""
            )

            return

        symbol = LAST_SIGNAL["symbol"]

        direction = LAST_SIGNAL["signal"]

        entry_price = LAST_SIGNAL["price"]

        strategy = LAST_SIGNAL["strategy"]

        entry_status = LAST_SIGNAL["entry"]

        await update.message.reply_text(
            f"""
╔════════════════════╗
      💰 TRADE OPENED
╚════════════════════╝

🪙 {symbol}

📊 {direction}

━━━━━━━━━━━━━━━━━━━━

💰 Entry:
{entry_price}

📈 Strategy:
{strategy}

📍 {entry_status}

━━━━━━━━━━━━━━━━━━━━

📡 Simulation Active

⏳ Expiration:
1 Minute
"""
        )

        await asyncio.sleep(60)

        df = get_crypto(symbol)

        exit_price = round(
            df.iloc[-1]["close"],
            2
        )

        result_trade = "DRAW ➖"

        global TOTAL_WINS
        global TOTAL_LOSSES

        if direction == "BUY":

            if exit_price > entry_price:
                result_trade = "WIN ✔"

            elif exit_price < entry_price:
                result_trade = "LOSS ❌"

        elif direction == "SELL":

            if exit_price < entry_price:
                result_trade = "WIN ✔"

            elif exit_price > entry_price:
                result_trade = "LOSS ❌"

        if "WIN" in result_trade:

            TOTAL_WINS += 1

        elif "LOSS" in result_trade:

            TOTAL_LOSSES += 1

        total = TOTAL_WINS + TOTAL_LOSSES

        winrate = round(
            (
                TOTAL_WINS / total
            ) * 100,
            2
        ) if total > 0 else 0

        await update.message.reply_text(
            f"""
━━━━━━━━━━━━━━━━━━
💰 TRADE CLOSED
━━━━━━━━━━━━━━━━━━

🪙 {symbol}

📊 {direction}

━━━━━━━━━━━━━━━━━━
📈 RESULT
━━━━━━━━━━━━━━━━━━

💰 Entry:
{entry_price}

💵 Exit:
{exit_price}

📊 {result_trade}

━━━━━━━━━━━━━━━━━━
📈 ACCOUNT STATS
━━━━━━━━━━━━━━━━━━

🏆 Wins:
{TOTAL_WINS}

❌ Losses:
{TOTAL_LOSSES}

🎯 Winrate:
{winrate}%

📞 @Mr_dflam
"""
        )


    # 📈 STATS
    elif text == "📈 Stats":

        await stats_command(
            update,
            context
        )


    # 📘 HELP
    elif text == "📘 Help":

        await help_command(
            update,
            context
        )


    # 📞 CONTACT
    elif text == "📞 Contact":

        await contact_command(
            update,
            context
        )


    # 💸 POCKET OPTION
    elif text == "💸 Pocket Option":

        await update.message.reply_text(
            "🌐 https://pocketoption.com"
        )


# ─────────────────────────────
# 🔘 BUTTON HANDLER
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


    # ❌ NO SIGNAL
    if result["signal"] == "NO SIGNAL":

        await query.edit_message_text(
            f"""
━━━━━━━━━━━━━━━━━━
📊 MARKET ANALYSIS
━━━━━━━━━━━━━━━━━━

🪙 {result['symbol']}

💰 {result['price']}

📈 {result['change']}%

⚪ NO SIGNAL

📊 RSI:
{result['rsi']}

📞 @Mr_dflam
"""
        )

        return


    # ✅ SIGNAL
    emoji = (
        "🟢"
        if result["signal"] == "BUY"
        else "🔴"
    )

    await query.edit_message_text(
        f"""
╔════════════════════╗
      🚀 SIGNAL FOUND
╚════════════════════╝

🪙 {result['symbol']}

{emoji} {result['signal']}

━━━━━━━━━━━━━━━━━━━━

💰 Price:
{result['price']}

📊 RSI:
{result['rsi']}

🎯 Accuracy:
{result['score']}%

━━━━━━━━━━━━━━━━━━━━

📈 Strategy:
{result['strategy']}

📍 {result['entry']}

━━━━━━━━━━━━━━━━━━━━

⏰ {result['time']}

📞 @Mr_dflam
"""
    )


# ─────────────────────────────
# 🚀 STARTUP
# ─────────────────────────────
async def startup(app):

    await set_commands(app)

    print("✅ COMMANDS LOADED")


# ─────────────────────────────
# ▶ RUN BOT
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
    CommandHandler("contact", contact_command)
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

app.run_polling()
