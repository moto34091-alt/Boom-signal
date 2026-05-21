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

            "price": round(last["close"], 2),

            "change": round(
                (
                    (
                        last["close"]
                        - prev["close"]
                    ) / prev["close"]
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

            rsi = result["rsi"]

            # ─────────────────────
            # 📍 ENTRY STATUS
            # ─────────────────────
            entry_status = "✅ ENTRÉE POSSIBLE"

            if result["signal"] == "BUY":

                if rsi >= 60 and rsi < 70:
                    entry_status = "⚠️ ENTRÉE EN RETARD"

                elif rsi >= 70:
                    entry_status = "❌ NE PAS ENTRER"

            elif result["signal"] == "SELL":

                if rsi <= 40 and rsi > 30:
                    entry_status = "⚠️ ENTRÉE EN RETARD"

                elif rsi <= 30:
                    entry_status = "❌ NE PAS ENTRER"

            result["entry"] = entry_status

            LAST_SIGNAL = result

        return result

    except Exception as e:

        print("ERROR:", e)

        return None


# ─────────────────────────────
# 🏠 MENU
# ─────────────────────────────
def menu():

    auto = "🟢 ON" if AUTO_SIGNAL else "🔴 OFF"

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "📊 MARKETS",
                callback_data="MARKETS"
            ),

            InlineKeyboardButton(
                f"⚡ AUTO {auto}",
                callback_data="AUTO"
            )
        ],

        [
            InlineKeyboardButton(
                "📈 STATS",
                callback_data="STATS"
            ),

            InlineKeyboardButton(
                "💰 TRADE NOW",
                callback_data="TRADE"
            )
        ],

        [
            InlineKeyboardButton(
                "💸 POCKET OPTION",
                url="https://pocketoption.com"
            )
        ],

        [
            InlineKeyboardButton(
                "📞 CONTACT",
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
                "₿ BTC",
                callback_data="BTCUSDT"
            ),

            InlineKeyboardButton(
                "Ξ ETH",
                callback_data="ETHUSDT"
            )
        ],

        [
            InlineKeyboardButton(
                "◎ SOL",
                callback_data="SOLUSDT"
            ),

            InlineKeyboardButton(
                "🟡 BNB",
                callback_data="BNBUSDT"
            )
        ],

        [
            InlineKeyboardButton(
                "🏠 HOME",
                callback_data="HOME"
            )
        ]
    ])


# ─────────────────────────────
# 🚀 START
# ─────────────────────────────
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = """
╔══════════════════╗
     🚀 SMART MONEY
╚══════════════════╝

📊 Market Scanner
🧠 Strategy Engine V2
⚡ Auto Signals
💰 Pocket Simulation

━━━━━━━━━━━━━━━━━━

📈 Hammer
📈 Morning Star
📈 Evening Star
📈 3 Bullish
📈 3 Bearish

━━━━━━━━━━━━━━━━━━

📞 @Mr_dflam
"""

    await update.message.reply_text(
        text,
        reply_markup=menu()
    )


# ─────────────────────────────
# 🔘 HANDLER
# ─────────────────────────────
async def handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    global AUTO_SIGNAL
    global LAST_SIGNAL
    global TOTAL_WINS
    global TOTAL_LOSSES

    query = update.callback_query

    await query.answer()

    data = query.data


    # ─────────────────────
    # 🏠 HOME
    # ─────────────────────
    if data == "HOME":

        await query.edit_message_text(
            """
╔══════════════════╗
     🚀 SMART MONEY
╚══════════════════╝
""",
            reply_markup=menu()
        )

        return


    # ─────────────────────
    # 📊 MARKETS
    # ─────────────────────
    if data == "MARKETS":

        await query.edit_message_text(
            """
━━━━━━━━━━━━━━━━━━
📊 SELECT MARKET
━━━━━━━━━━━━━━━━━━
""",
            reply_markup=markets()
        )

        return


    # ─────────────────────
    # ⚡ AUTO SIGNAL
    # ─────────────────────
    if data == "AUTO":

        AUTO_SIGNAL = not AUTO_SIGNAL

        status = (
            "🟢 ACTIVATED"
            if AUTO_SIGNAL
            else "🔴 DISABLED"
        )

        await query.edit_message_text(
            f"""
━━━━━━━━━━━━━━━━━━
⚡ AUTO SIGNAL
━━━━━━━━━━━━━━━━━━

{status}

📡 Smart Scanner Active
""",
            reply_markup=menu()
        )

        return


    # ─────────────────────
    # 📈 STATS
    # ─────────────────────
    if data == "STATS":

        total = (
            TOTAL_WINS +
            TOTAL_LOSSES
        )

        winrate = round(
            (
                TOTAL_WINS / total
            ) * 100,
            2
        ) if total > 0 else 0

        await query.edit_message_text(
            f"""
━━━━━━━━━━━━━━━━━━
📈 ACCOUNT STATS
━━━━━━━━━━━━━━━━━━

🏆 Wins:
{TOTAL_WINS}

❌ Losses:
{TOTAL_LOSSES}

🎯 Winrate:
{winrate}%

━━━━━━━━━━━━━━━━━━

📞 @Mr_dflam
""",
            reply_markup=menu()
        )

        return


    # ─────────────────────
    # 💰 TRADE NOW
    # ─────────────────────
    if data == "TRADE":

        if not LAST_SIGNAL:

            await query.edit_message_text(
                "⚠ Aucun signal actif",
                reply_markup=menu()
            )

            return

        symbol = LAST_SIGNAL["symbol"]

        direction = LAST_SIGNAL["signal"]

        entry_price = LAST_SIGNAL["price"]

        strategy = LAST_SIGNAL["strategy"]

        # 🚫 mauvais entry
        if "NE PAS ENTRER" in LAST_SIGNAL["entry"]:

            await query.edit_message_text(
                f"""
━━━━━━━━━━━━━━━━━━
🚫 TRADE BLOCKED
━━━━━━━━━━━━━━━━━━

🪙 {symbol}

📊 {direction}

📍 {LAST_SIGNAL['entry']}

⚠ Signal trop tardif

📞 @Mr_dflam
""",
                reply_markup=menu()
            )

            return

        # 🚀 START TRADE
        await query.edit_message_text(
            f"""
━━━━━━━━━━━━━━━━━━
💰 TRADE STARTED
━━━━━━━━━━━━━━━━━━

🪙 {symbol}

📊 {direction}

💰 Entry:
{entry_price}

📊 Strategy:
{strategy}

📍 {LAST_SIGNAL['entry']}

⏳ Expiration:
1 Minute

📡 Simulation Running...
"""
        )

        # ⏳ wait
        await asyncio.sleep(60)

        # 📊 exit price
        df = get_crypto(symbol)

        if df is None:

            await query.edit_message_text(
                "❌ Market unavailable"
            )

            return

        exit_price = round(
            df.iloc[-1]["close"],
            2
        )

        # 📈 RESULT
        result_trade = "LOSS ❌"

        if direction == "BUY":

            if exit_price > entry_price:
                result_trade = "WIN ✔"

        elif direction == "SELL":

            if exit_price < entry_price:
                result_trade = "WIN ✔"

        # 📊 STATS
        if "WIN" in result_trade:
            TOTAL_WINS += 1
        else:
            TOTAL_LOSSES += 1

        total = (
            TOTAL_WINS +
            TOTAL_LOSSES
        )

        winrate = round(
            (
                TOTAL_WINS / total
            ) * 100,
            2
        ) if total > 0 else 0

        # ✅ RESULT SCREEN
        await query.edit_message_text(
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
""",
            reply_markup=menu()
        )

        return


    # ─────────────────────
    # 📊 MARKET ANALYSIS
    # ─────────────────────
    result = analyze(data)

    if not result:

        await query.edit_message_text(
            "⚪ Market unavailable",
            reply_markup=markets()
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

⏰ {result['time']}

📞 @Mr_dflam
""",
            reply_markup=markets()
        )

        return


    # ✅ SIGNAL DETECTED
    emoji = (
        "🟢"
        if result["signal"] == "BUY"
        else "🔴"
    )

    await query.edit_message_text(
        f"""
╔══════════════════╗
    🚀 SIGNAL DETECTED
╚══════════════════╝

🪙 {result['symbol']}

{emoji} {result['signal']}

━━━━━━━━━━━━━━━━━━

💰 {result['price']}

📊 RSI:
{result['rsi']}

🎯 SCORE:
{result['score']}%

━━━━━━━━━━━━━━━━━━

📊 STRATEGY:
{result['strategy']}

📍 {result['entry']}

⏰ {result['time']}

📞 @Mr_dflam
""",
        reply_markup=InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "💰 TRADE NOW",
                    callback_data="TRADE"
                )
            ],

            [
                InlineKeyboardButton(
                    "📊 MARKETS",
                    callback_data="MARKETS"
                ),

                InlineKeyboardButton(
                    "🏠 HOME",
                    callback_data="HOME"
                )
            ]
        ])
    )


# ─────────────────────────────
# ▶ RUN BOT
# ─────────────────────────────
app = Application.builder().token(TOKEN).build()

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CallbackQueryHandler(handler)
)

print("🚀 SMART MONEY BOT READY")

app.run_polling()
