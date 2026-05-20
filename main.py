import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "TON_TOKEN"


def run_analysis():
    return {
        "signal": "BUY",
        "rsi": 60,
        "ema": "UP",
        "score": 80
    }


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("📊 Analyse", callback_data="analyse")],
        [InlineKeyboardButton("🤖 Start", callback_data="auto_on")],
        [InlineKeyboardButton("🛑 Stop", callback_data="auto_off")]
    ]

    await update.message.reply_text(
        "🚀 BOT READY",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "analyse":

        await query.edit_message_text("📊 Analyse en cours...")

        await asyncio.sleep(2)

        result = run_analysis()

        await query.edit_message_text(
            f"""📊 RESULT

🟢 {result['signal']}
📈 RSI: {result['rsi']}
⚡ EMA: {result['ema']}
🎯 SCORE: {result['score']}%
"""
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("BOT STARTED...")
app.run_polling()
