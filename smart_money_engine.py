import time

from market import get_crypto
from indicators import add_indicators
from smart_money_killer import smart_money_signal

CRYPTOS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT"
]


def run_smart_money():

    while True:

        for coin in CRYPTOS:

            try:

                df = get_crypto(coin)

                df = add_indicators(df)

                signal = smart_money_signal(df)

                if signal:

                    print(f"""
🚨 SMART MONEY TRAP

🪙 {coin}
⚠️ {signal['type']}

🟢 SIGNAL: {signal['signal']}

📈 RSI: {signal['rsi']}
🎯 SCORE: {signal['score']}%
""")

            except Exception as e:
                print("ERROR:", e)

        time.sleep(2)
