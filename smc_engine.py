import time

from market import get_crypto
from indicators import add_indicators
from smc_sniper import smc_signal

CRYPTOS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT"
]


def run_smc():

    while True:

        for coin in CRYPTOS:

            try:

                df = get_crypto(coin)

                df = add_indicators(df)

                signal = smc_signal(df)

                if signal:

                    print(f"""
🚀 SMC SIGNAL

🪙 {coin}
📊 TYPE: {signal['type']}
🟢 {signal['signal']}

📈 RSI: {signal['rsi']}
🎯 SCORE: {signal['score']}%
""")

            except Exception as e:
                print("ERROR:", e)

        time.sleep(3)
