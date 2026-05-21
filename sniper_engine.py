import time

from market import get_crypto
from indicators import add_indicators
from sniper_strategy import sniper_breakout

CRYPTOS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT"
]

last_signal = {}


def run_sniper():

    while True:

        for coin in CRYPTOS:

            try:

                df = get_crypto(coin)

                df = add_indicators(df)

                signal = sniper_breakout(df)

                if not signal:
                    continue

                key = f"{coin}_{signal['signal']}"

                if last_signal.get(key) == signal:
                    continue

                last_signal[key] = signal

                print(f"""
🚀 SNIPER BREAKOUT

🪙 {coin}
🟢 {signal['signal']}

⚡ BREAKOUT DETECTED
📈 RSI: {signal['rsi']}
🎯 SCORE: {signal['score']}%
""")

            except Exception as e:
                print("ERROR:", coin, e)

        # ⚡ ultra rapide
        time.sleep(1)
