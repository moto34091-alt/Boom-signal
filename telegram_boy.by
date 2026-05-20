from telegram import Bot
from config import TOKEN

bot = Bot(token=TOKEN)


async def send_signal(chat_id, asset, data):
    message = f"""
🚀 SIGNAL READY

📊 ASSET: {asset}
⏱ TF: 10s
⌛ EXP: 30s

🟢 {data['signal']}

📈 RSI(7): {data['rsi']}
🎯 CONFIDENCE: {data['confidence']}%
"""

    await bot.send_message(chat_id=chat_id, text=message)
