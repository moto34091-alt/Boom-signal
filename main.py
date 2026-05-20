from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("TOKEN")

running = False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("📊 Analyse", callback_data="analyse")],
        [InlineKeyboardButton("🤖 START AUTO", callback_data="auto_on")],
        [InlineKeyboardButton("🛑 STOP AUTO", callback_data="auto_off")],
        [InlineKeyboardButton("📈 Stats", callback_data="stats")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚀 OTC BOT CONTROL PANEL",
        reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global running

    query = update.callback_query
    await query.answer()

    if query.data == "analyse":
        await query.edit_message_text("📊 Analyse en cours...")

    elif query.data == "auto_on":
        running = True
        await query.edit_message_text("🤖 AUTO SCAN ACTIVÉ")

    elif query.data == "auto_off":
        running = False
        await query.edit_message_text("🛑 AUTO SCAN STOP")

    elif query.data == "stats":
        await query.edit_message_text("📈 Stats en cours...")


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("BOT STARTED...")
app.run_polling()
