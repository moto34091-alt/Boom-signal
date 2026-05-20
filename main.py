import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 🔐 TOKEN depuis Railway Environment
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise Exception("❌ TOKEN manquant dans les variables d'environnement Railway")


# 🧠 Analyse simple (à remplacer par ton strategy.py)
def run_analysis():
    return {
        "signal": "BUY",
        "rsi": 60,
        "ema": "UP",
        "score": 82
    }


# ▶️ MENU START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("📊 Analyse", callback_data="analyse")],
        [InlineKeyboardButton("🤖 Start Auto", callback_data="auto_on")],
        [InlineKeyboardButton("🛑 Stop Auto", callback_data="auto_off")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚀 BOT OTC READY",
        reply_markup=reply_markup
    )


# 🔘 BUTTONS
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "analyse":

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

    elif query.data == "auto_on":
        await query.edit_message_text("🤖 AUTO SCAN ACTIVÉ")

    elif query.data == "auto_off":
        await query.edit_message_text("🛑 AUTO SCAN STOP")


# ▶️ APP
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("BOT STARTED...")
app.run_polling()
