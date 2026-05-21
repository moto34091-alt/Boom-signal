import time

from market import get_crypto
from indicators import add_indicators
from order_block_sniper import order_block_sniper

CRYPTOS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT"
]


def run_order_block():

    while True:

        for coin in CRYPTOS:

            try:

                df = get_crypto(coin)

                df = add_indicators(df)

                signal = order_block_sniper(df)

                if signal:

                    print(f"""
🎯 ORDER BLOCK SNIPER

🪙 {coin}
🟢 {signal['signal']}

📦 ZONE:
{signal['zone_low']} - {signal['zone_high']}

📈 RSI: {signal['rsi']}
🎯 SCORE: {signal['score']}%
""")

            except Exception as e:
                print("ERROR:", e)

        time.sleep(3)
