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


# ─────────────────────────────
# 🔐 TOKEN
# ─────────────────────────────
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise Exception("TOKEN manquant")


# ─────────────────────────────
# 🌍 GLOBAL STATE
# ─────────────────────────────
AUTO_SIGNAL = False
LAST_SIGNAL = None

TRADE_HISTORY = []

TOTAL_WINS = 0
TOTAL_LOSSES = 0


# ─────────────────────────────
# 🧠 ANALYSE MARCHÉ
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
            "change": round(
                ((last["close"] - prev["close"]) / prev["close"]) * 100,
                2
            ),
            "signal": "NO SIGNAL",
            "rsi": round(last.get("rsi", 0), 2),
            "score": 0,
            "time": datetime.now().strftime("%H:%M:%S")
        }

        # ✅ SIGNAL
        if signal:

            result["signal"] = signal["signal"]
            result["rsi"] = signal["rsi"]
            result["score"] = signal["score"]

            LAST_SIGNAL = result

        return result

    except Exception as e:

        print("ERROR:", e)
        return None


# ─────────────────────────────
# 🏠 DASHBOARD
# ─────────────────────────────
def dashboard():

    status = "🟢 ON" if AUTO_SIGNAL else "🔴 OFF"

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "📊 MARKET ANALYSIS",
                callback_data="PAGE_MARKETS"
            )
        ],

        [
            InlineKeyboardButton(
                "⚡ AUTO SIGNAL",
                callback_data="PAGE_SIGNALS"
            )
        ],

        [
            InlineKeyboardButton(
                "📈 STATS",
                callback_data="STATS"
            )
        ],

        [
            InlineKeyboardButton(
                "⚙️ SETTINGS",
                callback_data="PAGE_SETTINGS"
            )
        ],

        [
            InlineKeyboardButton(
                f"🔥 BOT STATUS: {status}",
                callback_data="STATUS"
            )
        ],

        [
            InlineKeyboardButton(
                "💰 POCKET OPTION",
                url="https://pocketoption.com"
            )
        ],

        [
            InlineKeyboardButton(
                "📞 CONTACT @Mr_dflam",
                url="https://t.me/Mr_dflam"
            )
        ]
    ])


# ─────────────────────────────
# 📊 MARKETS
# ─────────────────────────────
def markets():

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "₿ BTCUSDT",
                callback_data="BTCUSDT"
            )
        ],

        [
            InlineKeyboardButton(
                "Ξ ETHUSDT",
                callback_data="ETHUSDT"
            )
        ],

        [
            InlineKeyboardButton(
                "◎ SOLUSDT",
                callback_data="SOLUSDT"
            )
        ],

        [
            InlineKeyboardButton(
                "🟡 BNBUSDT",
                callback_data="BNBUSDT"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅ BACK",
                callback_data="PAGE_HOME"
            )
        ]
    ])


# ─────────────────────────────
# 📊 SIGNAL MENU
# ─────────────────────────────
def signal_menu():

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "💰 TRADE NOW",
                callback_data="TRADE"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅ BACK",
                callback_data="PAGE_MARKETS"
            )
        ]
    ])


# ─────────────────────────────
# 💰 TRADE MENU
# ─────────────────────────────
def trade_menu():

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "💵 1$",
                callback_data="TRADE_1"
            ),

            InlineKeyboardButton(
                "💵 2$",
                callback_data="TRADE_2"
            ),

            InlineKeyboardButton(
                "💵 3$",
                callback_data="TRADE_3"
            )
        ],

        [
            InlineKeyboardButton(
                "💵 4$",
                callback_data="TRADE_4"
            ),

            InlineKeyboardButton(
                "💵 5$",
                callback_data="TRADE_5"
            )
        ],

        [
            InlineKeyboardButton(
                "💵 10$",
                callback_data="TRADE_10"
            ),

            InlineKeyboardButton(
                "💵 20$",
                callback_data="TRADE_20"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅ BACK",
                callback_data="PAGE_HOME"
            )
        ]
    ])


# ─────────────────────────────
# ⚙️ SETTINGS
# ─────────────────────────────
def settings():

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "📊 STATUS",
                callback_data="STATUS"
            )
        ],

        [
            InlineKeyboardButton(
                "📘 HELP",
                callback_data="HELP"
            )
        ],

        [
            InlineKeyboardButton(
                "💰 POCKET OPTION",
                url="https://pocketoption.com"
            )
        ],

        [
            InlineKeyboardButton(
                "📞 CONTACT @Mr_dflam",
                url="https://t.me/Mr_dflam"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅ BACK",
                callback_data="PAGE_HOME"
            )
        ]
    ])


# ─────────────────────────────
# 📘 HELP
# ─────────────────────────────
HELP_TEXT = """
━━━━━━━━━━━━━━━━━━━━
📘 SMART MONEY BOT
━━━━━━━━━━━━━━━━━━━━

🧠 Analyse :
• RSI
• EMA
• Smart Money
• Volatility

━━━━━━━━━━━━━━━━━━━━
📊 SIGNALS :
🟢 BUY = hausse probable
🔴 SELL = baisse probable
⚪ NO SIGNAL = marché instable

━━━━━━━━━━━━━━━━━━━━
💰 TRADE NOW :
• Choisis le montant
• Le bot prend le dernier signal
• Simulation BUY / SELL

━━━━━━━━━━━━━━━━━━━━
⚡ AUTO SIGNAL :
Analyse automatique du marché

━━━━━━━━━━━━━━━━━━━━
⏳ EXPIRATION :
1 minute

━━━━━━━━━━━━━━━━━━━━
💰 PLATFORM :
Pocket Option

━━━━━━━━━━━━━━━━━━━━
📞 CONTACT :
@Mr_dflam
━━━━━━━━━━━━━━━━━━━━
"""


# ─────────────────────────────
# 🚀 START
# ─────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = """
🚀 SMART MONEY TRADING APP

📊 Analyse marché
⚡ Smart Money Signal
💰 Trade Simulation
📈 Trading Stats
"""

    await update.message.reply_text(
        msg,
        reply_markup=dashboard()
    )


# ─────────────────────────────
# 🔘 HANDLER
# ─────────────────────────────
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global AUTO_SIGNAL
    global LAST_SIGNAL

    global TOTAL_WINS
    global TOTAL_LOSSES
    global TRADE_HISTORY

    query = update.callback_query

    await query.answer()

    data = query.data


    # 🏠 HOME
    if data == "PAGE_HOME":

        await query.edit_message_text(
            "🏠 DASHBOARD",
            reply_markup=dashboard()
        )

        return


    # 📊 MARKETS
    if data == "PAGE_MARKETS":

        await query.edit_message_text(
            "📊 MARKET ANALYSIS",
            reply_markup=markets()
        )

        return


    # ⚙️ SETTINGS
    if data == "PAGE_SETTINGS":

        await query.edit_message_text(
            "⚙️ SETTINGS",
            reply_markup=settings()
        )

        return


    # 📘 HELP
    if data == "HELP":

        await query.edit_message_text(
            HELP_TEXT,
            reply_markup=settings()
        )

        return


    # 📊 STATUS
    if data == "STATUS":

        await query.edit_message_text(
            f"""
📊 BOT STATUS

⚡ Auto Signal:
{"🟢 ACTIVE" if AUTO_SIGNAL else "🔴 OFF"}

⏰ {datetime.now().strftime("%H:%M:%S")}

📞 @Mr_dflam
""",
            reply_markup=settings()
        )

        return


    # ⚡ AUTO SIGNAL
    if data == "PAGE_SIGNALS":

        AUTO_SIGNAL = not AUTO_SIGNAL

        await query.edit_message_text(
            f"""
⚡ AUTO SIGNAL

{"🟢 ACTIVATED" if AUTO_SIGNAL else "🔴 DISABLED"}

📡 Market scanner ready
""",
            reply_markup=dashboard()
        )

        return


    # 📈 STATS
    if data == "STATS":

        total = TOTAL_WINS + TOTAL_LOSSES

        if total > 0:
            winrate = round(
                (TOTAL_WINS / total) * 100,
                2
            )
        else:
            winrate = 0

        msg = f"""
━━━━━━━━━━━━━━━━━━━━
📈 TRADING STATS
━━━━━━━━━━━━━━━━━━━━

🏆 Wins: {TOTAL_WINS}

❌ Losses: {TOTAL_LOSSES}

📊 Total Trades: {total}

🎯 Winrate: {winrate}%

📡 Smart Money Active

📞 @Mr_dflam
"""

        await query.edit_message_text(
            msg,
            reply_markup=dashboard()
        )

        return


    # 💰 OPEN TRADE MENU
    if data == "TRADE":

        await query.edit_message_text(
            "💰 CHOOSE TRADE AMOUNT",
            reply_markup=trade_menu()
        )

        return


    # 💰 EXECUTE TRADE
    if data.startswith("TRADE_"):

        amount = data.replace("TRADE_", "")

        if not LAST_SIGNAL:

            await query.edit_message_text(
                "⚪ No signal available"
            )

            return

        direction = LAST_SIGNAL["signal"]

        signal_emoji = (
            "🟢"
            if direction == "BUY"
            else "🔴"
        )

        # 🔥 SIMULATION RESULT
        if direction == "BUY":

            result_trade = "WIN ✔"

            TOTAL_WINS += 1

        else:

            result_trade = "LOSS ❌"

            TOTAL_LOSSES += 1

        # 📈 SAVE HISTORY
        TRADE_HISTORY.append({

            "symbol": LAST_SIGNAL["symbol"],

            "signal": direction,

            "amount": amount,

            "result": result_trade,

            "time": LAST_SIGNAL["time"]
        })

        total = TOTAL_WINS + TOTAL_LOSSES

        if total > 0:

            winrate = round(
                (TOTAL_WINS / total) * 100,
                2
            )

        else:

            winrate = 0

        msg = f"""
━━━━━━━━━━━━━━━━━━━━
💰 TRADE EXECUTED
━━━━━━━━━━━━━━━━━━━━

🪙 {LAST_SIGNAL['symbol']}

{signal_emoji} {direction}

💵 Amount: {amount}$

💰 Entry: {LAST_SIGNAL['price']}

⏰ {LAST_SIGNAL['time']}

📈 RESULT:
{result_trade}

━━━━━━━━━━━━━━━━━━━━
📈 ACCOUNT STATS
━━━━━━━━━━━━━━━━━━━━

🏆 Wins: {TOTAL_WINS}

❌ Losses: {TOTAL_LOSSES}

🎯 Winrate: {winrate}%

📞 @Mr_dflam
"""

        await query.edit_message_text(
            msg,
            reply_markup=dashboard()
        )

        return


    # ─────────────────────────────
    # 📊 MARKET ANALYSIS
    # ─────────────────────────────
    result = analyze(data)

    if not result:

        await query.edit_message_text(
            "⚪ Market unavailable",
            reply_markup=markets()
        )

        return


    # ❌ NO SIGNAL
    if result["signal"] == "NO SIGNAL":

        msg = f"""
━━━━━━━━━━━━━━━━━━━━
📊 MARKET ANALYSIS
━━━━━━━━━━━━━━━━━━━━

🪙 {result['symbol']}

💰 {result['price']}

📈 {result['change']}%

⚪ NO SIGNAL

📊 RSI: {result['rsi']}

⏰ {result['time']}

📞 @Mr_dflam
"""

        await query.edit_message_text(
            msg,
            reply_markup=markets()
        )

        return


    # ✅ SIGNAL FOUND
    signal_emoji = (
        "🟢"
        if result["signal"] == "BUY"
        else "🔴"
    )

    msg = f"""
━━━━━━━━━━━━━━━━━━━━
📊 SMART MONEY SIGNAL
━━━━━━━━━━━━━━━━━━━━

🪙 {result['symbol']}

💰 Price: {result['price']}

📈 Change: {result['change']}%

━━━━━━━━━━━━━━━━━━━━

{signal_emoji} SIGNAL:
{result['signal']}

📊 RSI: {result['rsi']}

🎯 SCORE: {result['score']}%

━━━━━━━━━━━━━━━━━━━━

⏳ EXPIRATION:
1 MINUTE

💰 READY TO TRADE

⏰ {result['time']}

📞 @Mr_dflam
"""

    await query.edit_message_text(
        msg,
        reply_markup=signal_menu()
    )


# ─────────────────────────────
# ▶ RUN BOT
# ─────────────────────────────
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handler))

print("🚀 SMART MONEY APP READY")

app.run_polling()
