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
# 🏠 HOME MENU
# ─────────────────────────────
def home_menu():

    auto = (
        "🟢 ON"
        if AUTO_SIGNAL
        else "🔴 OFF"
    )

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "📊 ANALYSE MARKET",
                callback_data="MARKETS"
            )
        ],

        [
            InlineKeyboardButton(
                f"⚡ AUTO SIGNAL {auto}",
                callback_data="AUTO"
            )
        ],

        [
            InlineKeyboardButton(
                "💰 TRADE NOW SIMULATION",
                callback_data="TRADE"
            )
        ],

        [
            InlineKeyboardButton(
                "📈 ACCOUNT STATS",
                callback_data="STATS"
            )
        ],

        [
            InlineKeyboardButton(
                "📘 HELP & MANUAL",
                callback_data="HELP"
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
                "📞 CONTACT @Mr_dflam",
                url="https://t.me/Mr_dflam"
            )
        ]
    ])


# ─────────────────────────────
# 📊 MARKETS
# ─────────────────────────────
def markets_menu():

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
        reply_markup=home_menu()
    )


# ─────────────────────────────
# 🔘 BUTTON HANDLER
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
╔════════════════════╗
      🚀 SMART MONEY AI
╚════════════════════╝

📡 STATUS:
🟢 ONLINE

📞 @Mr_dflam
""",
            reply_markup=home_menu()
        )

        return


    # ─────────────────────
    # 📊 MARKETS
    # ─────────────────────
    if data == "MARKETS":

        await query.edit_message_text(
            """
━━━━━━━━━━━━━━━━━━━━
📊 SELECT MARKET
━━━━━━━━━━━━━━━━━━━━

Choose asset for analysis
""",
            reply_markup=markets_menu()
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
╔════════════════════╗
       ⚡ AUTO SIGNAL
╚════════════════════╝

📡 STATUS:
{status}

🧠 AI Scanner Running...
""",
            reply_markup=home_menu()
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
╔════════════════════╗
      📈 ACCOUNT STATS
╚════════════════════╝

🏆 Wins:
{TOTAL_WINS}

❌ Losses:
{TOTAL_LOSSES}

🎯 Winrate:
{winrate}%

━━━━━━━━━━━━━━━━━━━━

📞 @Mr_dflam
""",
            reply_markup=home_menu()
        )

        return


    # ─────────────────────
    # 📘 HELP
    # ─────────────────────
    if data == "HELP":

        await query.edit_message_text(
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
→ trade sécurisé

⚠️ ENTRÉE EN RETARD
→ mouvement déjà avancé

❌ NE PAS ENTRER
→ signal dangereux

━━━━━━━━━━━━━━━━━━━━

⏳ Expiration conseillée:
1 minute

📈 Marchés:
BTC / ETH / SOL / BNB

━━━━━━━━━━━━━━━━━━━━

📞 Plus d'infos:
@Mr_dflam
""",
            reply_markup=home_menu()
        )

        return


    # ─────────────────────
    # 💰 TRADE
    # ─────────────────────
    if data == "TRADE":

        if not LAST_SIGNAL:

            await query.edit_message_text(
                """
⚠ Aucun signal actif

📊 Analyse d'abord un marché
""",
                reply_markup=home_menu()
            )

            return

        symbol = LAST_SIGNAL["symbol"]

        direction = LAST_SIGNAL["signal"]

        entry_price = LAST_SIGNAL["price"]

        strategy = LAST_SIGNAL["strategy"]

        entry_status = LAST_SIGNAL["entry"]

        # 🚫 BLOCKED
        if "NE PAS ENTRER" in entry_status:

            await query.edit_message_text(
                f"""
╔════════════════════╗
      🚫 TRADE BLOCKED
╚════════════════════╝

🪙 {symbol}

📊 {direction}

📍 {entry_status}

⚠ Signal trop tardif
""",
                reply_markup=home_menu()
            )

            return

        # 🚀 TRADE START
        await query.edit_message_text(
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

        # ⏳ WAIT
        await asyncio.sleep(60)

        # 📊 EXIT PRICE
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
        result_trade = "DRAW ➖"

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

        # 📊 STATS
        if "WIN" in result_trade:

            TOTAL_WINS += 1

        elif "LOSS" in result_trade:

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

        # 📈 FINAL RESULT
        await query.edit_message_text(
            f"""
╔════════════════════╗
      📈 TRADE RESULT
╚════════════════════╝

🪙 {symbol}

━━━━━━━━━━━━━━━━━━━━

💰 Entry:
{entry_price}

💵 Exit:
{exit_price}

🏆 RESULT:
{result_trade}

━━━━━━━━━━━━━━━━━━━━

📊 ACCOUNT

🏆 Wins:
{TOTAL_WINS}

❌ Losses:
{TOTAL_LOSSES}

🎯 Winrate:
{winrate}%

━━━━━━━━━━━━━━━━━━━━

📞 @Mr_dflam
""",
            reply_markup=home_menu()
        )

        return


    # ─────────────────────
    # 📊 MARKET ANALYSIS
    # ─────────────────────
    result = analyze(data)

    if not result:

        await query.edit_message_text(
            """
⚪ Market unavailable
""",
            reply_markup=markets_menu()
        )

        return


    # ❌ NO SIGNAL
    if result["signal"] == "NO SIGNAL":

        await query.edit_message_text(
            f"""
╔════════════════════╗
      📊 MARKET STATUS
╚════════════════════╝

🪙 {result['symbol']}

━━━━━━━━━━━━━━━━━━━━

💰 Price:
{result['price']}

📈 Change:
{result['change']}%

⚪ NO SIGNAL

📊 RSI:
{result['rsi']}

━━━━━━━━━━━━━━━━━━━━

⏰ {result['time']}

📞 @Mr_dflam
""",
            reply_markup=markets_menu()
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
                )
            ],

            [
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

print("🚀 SMART MONEY AI STARTED")

app.run_polling()
