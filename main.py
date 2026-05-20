from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio

TOKEN = "TON_TOKEN"


# 🧠 simulation analyse (remplace par ton strategy.py plus tard)
def run_analysis():

    return {
        "signal": "BUY",
        "rsi": 61,
        "ema": "UP",
        "score": 82
    }


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("📊 Analyse", callback_data="analyse")],
        [InlineKeyboardButton("🤖 START AUTO", callback_data="auto_on")],
        [InlineKeyboardButton("🛑 STOP AUTO", callback_data="auto_off")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚀 BOT READY",
        reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "analyse":

        await query.edit_message_text("📊 Analyse en cours...")

        # ⏳ pause non bloquante
        await asyncio.sleep(2)

        result = run_analysis()

        await query.edit_message_text(
            f"""📊 ANALYSE TERMINÉE

🟢 Signal: {result['signal']}
📈 RSI: {result['rsi']}
⚡ EMA: {result['ema']}
🎯 SCORE: {result['score']}%
"""
        )


# ▶️ BOT
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("BOT STARTED...")
app.run_polling()
