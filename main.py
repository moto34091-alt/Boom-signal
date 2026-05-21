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

TRADE_HISTORY = []

TOTAL_WINS = 0
TOTAL_LOSSES = 0


# ─────────────────────────────
# 🧠 SMART MONEY SIGNAL
# ─────────────────────────────
def smart_money_signal(df):

    last = df.iloc[-1]

    signal = None
    score = 0

    ema_up = last["ema5"] > last["ema13"]
    ema_down = last["ema5"] < last["ema13"]

    bullish = last["close"] > last["open"]
    bearish = last["close"] < last["open"]

    volatility = (
        df["high"] - df["low"]
    ).tail(10).mean()

    rsi = last["rsi"]

    # 🟢 BUY
    if (

        ema_up
        and rsi < 45
        and bullish
        and volatility > 0.05

    ):

        signal = "BUY"
        score = 80

    # 🔴 SELL
    elif (

        ema_down
        and rsi > 55
        and bearish
        and volatility > 0.05

    ):

        signal = "SELL"
        score = 80

    if signal is None:
        return None

    return {

        "signal": signal,

        "rsi": round(rsi, 2),

        "score": score
    }


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
                    (last["close"] - prev["close"])
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

    status = (
        "🟢 ON"
        if AUTO_SIGNAL
        else "🔴 OFF"
    )

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
                callback_data="AUTO_SIGNAL"
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
                f"🔥 STATUS {status}",
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
# 📊 MARKET MENU
# ─────────────────────────────
def market_menu():

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
                "⬅ BACK",
                callback_data="HOME"
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
                "💵 5$",
                callback_data="TRADE_5"
            ),

            InlineKeyboardButton(
                "💵 10$",
                callback_data="TRADE_10"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅ BACK",
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
━━━━━━━━━━━━━━━━━━━━
🚀 SMART MONEY APP
━━━━━━━━━━━━━━━━━━━━

📊 Market Analysis
⚡ Smart Money Signals
💰 Trade Simulation
📈 Live Statistics

📞 @Mr_dflam
"""

    await update.message.reply_text(

        text,

        reply_markup=dashboard()
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


    # 🏠 HOME
    if data == "HOME":

        await query.edit_message_text(

            "🏠 DASHBOARD",

            reply_markup=dashboard()
        )

        return


    # 📊 PAGE MARKETS
    if data == "PAGE_MARKETS":

        await query.edit_message_text(

            """
━━━━━━━━━━━━━━━━━━━━
📊 SELECT MARKET
━━━━━━━━━━━━━━━━━━━━
""",

            reply_markup=market_menu()
        )

        return


    # ⚡ AUTO SIGNAL
    if data == "AUTO_SIGNAL":

        AUTO_SIGNAL = not AUTO_SIGNAL

        status = (
            "🟢 ACTIVATED"
            if AUTO_SIGNAL
            else "🔴 DISABLED"
        )

        await query.edit_message_text(

            f"""
━━━━━━━━━━━━━━━━━━━━
⚡ AUTO SIGNAL
━━━━━━━━━━━━━━━━━━━━

{status}

📡 Scanner Ready
""",

            reply_markup=dashboard()
        )

        return


    # 📈 STATS
    if data == "STATS":

        total = (
            TOTAL_WINS +
            TOTAL_LOSSES
        )

        if total > 0:

            winrate = round(
                (
                    TOTAL_WINS / total
                ) * 100,
                2
            )

        else:

            winrate = 0

        await query.edit_message_text(

            f"""
━━━━━━━━━━━━━━━━━━━━
📈 ACCOUNT STATS
━━━━━━━━━━━━━━━━━━━━

🏆 Wins:
{TOTAL_WINS}

❌ Losses:
{TOTAL_LOSSES}

🎯 Winrate:
{winrate}%

📊 Trades:
{total}

📞 @Mr_dflam
""",

            reply_markup=dashboard()
        )

        return


    # 🔥 STATUS
    if data == "STATUS":

        status = (
            "🟢 ACTIVE"
            if AUTO_SIGNAL
            else "🔴 OFF"
        )

        await query.edit_message_text(

            f"""
━━━━━━━━━━━━━━━━━━━━
🔥 BOT STATUS
━━━━━━━━━━━━━━━━━━━━

⚡ Auto Signal:
{status}

⏰ {datetime.now().strftime('%H:%M:%S')}

📞 @Mr_dflam
""",

            reply_markup=dashboard()
        )

        return


    # 💰 OPEN TRADE MENU
    if data == "TRADE":

        await query.edit_message_text(

            """
━━━━━━━━━━━━━━━━━━━━
💰 SELECT AMOUNT
━━━━━━━━━━━━━━━━━━━━
""",

            reply_markup=trade_menu()
        )

        return


    # 💰 EXECUTE TRADE
    if data.startswith("TRADE_"):

        amount = data.replace(
            "TRADE_",
            ""
        )

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

        entry_price = LAST_SIGNAL["price"]

        # ⏳ WAIT MESSAGE
        await query.edit_message_text(

            f"""
━━━━━━━━━━━━━━━━━━━━
⏳ TRADE STARTED
━━━━━━━━━━━━━━━━━━━━

🪙 {LAST_SIGNAL['symbol']}

{signal_emoji} {direction}

💵 Amount:
{amount}$

💰 Entry:
{entry_price}

⏳ Expiration:
1 Minute

📡 Waiting Result...
"""
        )

        # ⏳ WAIT 1 MINUTE
        await asyncio.sleep(60)

        # 📊 NEW PRICE
        new_df = get_crypto(
            LAST_SIGNAL["symbol"]
        )

        if new_df is None:

            await query.edit_message_text(
                "❌ Market unavailable"
            )

            return

        new_price = round(
            new_df.iloc[-1]["close"],
            2
        )

        # 🟢 BUY
        if direction == "BUY":

            if new_price > entry_price:

                result_trade = "WIN ✔"

                TOTAL_WINS += 1

            else:

                result_trade = "LOSS ❌"

                TOTAL_LOSSES += 1

        # 🔴 SELL
        else:

            if new_price < entry_price:

                result_trade = "WIN ✔"

                TOTAL_WINS += 1

            else:

                result_trade = "LOSS ❌"

                TOTAL_LOSSES += 1

        # 📈 WINRATE
        total = (
            TOTAL_WINS +
            TOTAL_LOSSES
        )

        if total > 0:

            winrate = round(
                (
                    TOTAL_WINS / total
                ) * 100,
                2
            )

        else:

            winrate = 0

        # 📊 FINAL RESULT
        await query.edit_message_text(

            f"""
━━━━━━━━━━━━━━━━━━━━
💰 TRADE CLOSED
━━━━━━━━━━━━━━━━━━━━

🪙 {LAST_SIGNAL['symbol']}

{signal_emoji} {direction}

💵 Amount:
{amount}$

━━━━━━━━━━━━━━━━━━━━
📊 TRADE RESULT
━━━━━━━━━━━━━━━━━━━━

💰 Entry:
{entry_price}

💵 Exit:
{new_price}

📈 RESULT:
{result_trade}

━━━━━━━━━━━━━━━━━━━━
📈 ACCOUNT STATS
━━━━━━━━━━━━━━━━━━━━

🏆 Wins:
{TOTAL_WINS}

❌ Losses:
{TOTAL_LOSSES}

🎯 Winrate:
{winrate}%

⏰ {datetime.now().strftime('%H:%M:%S')}

📞 @Mr_dflam
""",

            reply_markup=dashboard()
        )

        return


    # 📊 ANALYSE MARKET
    result = analyze(data)

    if not result:

        await query.edit_message_text(

            "⚪ Market unavailable",

            reply_markup=market_menu()
        )

        return


    # ❌ NO SIGNAL
    if result["signal"] == "NO SIGNAL":

        await query.edit_message_text(

            f"""
━━━━━━━━━━━━━━━━━━━━
📊 MARKET ANALYSIS
━━━━━━━━━━━━━━━━━━━━

🪙 {result['symbol']}

💰 {result['price']}

📈 {result['change']}%

⚪ NO SIGNAL

📊 RSI:
{result['rsi']}

⏰ {result['time']}

📞 @Mr_dflam
""",

            reply_markup=market_menu()
        )

        return


    # ✅ SIGNAL FOUND
    signal_emoji = (
        "🟢"
        if result["signal"] == "BUY"
        else "🔴"
    )

    await query.edit_message_text(

        f"""
━━━━━━━━━━━━━━━━━━━━
📊 SMART MONEY SIGNAL
━━━━━━━━━━━━━━━━━━━━

🪙 {result['symbol']}

💰 Price:
{result['price']}

📈 Change:
{result['change']}%

━━━━━━━━━━━━━━━━━━━━

{signal_emoji} SIGNAL:
{result['signal']}

📊 RSI:
{result['rsi']}

🎯 SCORE:
{result['score']}%

━━━━━━━━━━━━━━━━━━━━

⏳ EXPIRATION:
1 MINUTE

💰 READY TO TRADE

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
                    "⬅ BACK",
                    callback_data="PAGE_MARKETS"
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

print("🚀 SMART MONEY APP READY")

app.run_polling()
