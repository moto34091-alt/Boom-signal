from telegram import Bot
import os

bot = Bot(token=os.getenv("TOKEN"))


async def send_signal(chat_id, asset, data):

    msg = f"""
🚀 SIGNAL OTC

📊 {asset}
🟢 {data['signal']}
📈 RSI: {data['rsi']}
🎯 SCORE: {data['score']}%
"""

    await bot.send_message(chat_id=chat_id, text=msg)
