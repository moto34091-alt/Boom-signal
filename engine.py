import time
from market import get_forex, get_crypto
from indicators import add_indicators
from strategy import generate_signal

FOREX = ["EUR/USD", "GBP/USD"]
CRYPTO = ["BTCUSDT", "ETHUSDT"]

last_signal_cache = {}


def run():

    while True:

        # 🌍 FOREX
        for pair in FOREX:

            df = get_forex(pair)
            if df is None:
                continue

            df = add_indicators(df)

            signal = generate_signal(df)

            if signal:

                key = f"{pair}_{signal['signal']}"

                # 🔴 évite spam même signal
                if last_signal_cache.get(key) == signal:
                    continue

                last_signal_cache[key] = signal

                print("FOREX:", pair, signal)


        # ₿ CRYPTO
        for coin in CRYPTO:

            df = get_crypto(coin)

            df = add_indicators(df)

            signal = generate_signal(df)

            if signal:

                key = f"{coin}_{signal['signal']}"

                if last_signal_cache.get(key) == signal:
                    continue

                last_signal_cache[key] = signal

                print("CRYPTO:", coin, signal)

        time.sleep(5)
