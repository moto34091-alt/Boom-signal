import time
from market import get_forex, get_crypto
from indicators import add_indicators
from strategy import generate_signal

FOREX = ["EUR/USD", "GBP/USD"]
CRYPTO = ["BTCUSDT", "ETHUSDT"]


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
                print("FOREX:", pair, signal)


        # ₿ CRYPTO
        for coin in CRYPTO:

            df = get_crypto(coin)

            df = add_indicators(df)
            signal = generate_signal(df)

            if signal:
                print("CRYPTO:", coin, signal)

        time.sleep(5)
