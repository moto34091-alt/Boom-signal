from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio

TOKEN = "TON_TOKEN_ICI"


# 🧠 ANALYSE SIMPLE (tu peux brancher ton strategy.py après)
def run_analysis():

    return {
        "signal": "BUY",
        "rsi": 62,
        "ema": "UP",
        "score": 80
    }


# ▶️ START MENU
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("📊 Analyse", callback_data="analyse")],
        [InlineKeyboardButton("🤖 Start Auto", callback_data="auto_on")],
        [InlineKeyboardButton("🛑 Stop Auto", callback_data="auto_off")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚀 BOT OTC READY",
        reply_markup=reply_markup
    )


# 🔘 BUTTON HANDLER
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    # 📊 ANALYSE
    if data == "analyse":

        await query.edit_message_text("📊 Analyse en cours...")

        await asyncio.sleep(2)

        result = run_analysis()

        await query.edit_message_text(
            f"""📊 ANALYSE TERMINÉE

🟢 Signal: {result['signal']}
📈 RSI: {result['rsi']}
⚡ EMA: {result['ema']}
🎯 Score: {result['score']}%
"""
        )


    # 🤖 AUTO ON
    elif data == "auto_on":
        await query.edit_message_text("🤖 AUTO SCAN ACTIVÉ")

    # 🛑 AUTO OFF
    elif data == "auto_off":
        await query.edit_message_text("🛑 AUTO SCAN STOP")


# ▶️ BOT START
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("BOT STARTED...")
app.run_polling()
