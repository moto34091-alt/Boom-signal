from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "TON_TOKEN_ICI"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Scalping Bot Active"
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("BOT STARTED...")

app.run_polling()
