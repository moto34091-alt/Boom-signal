import time
from market import get_forex, get_crypto
from indicators import add_indicators
from strategy import generate_signal

FOREX = ["EUR/USD", "GBP/USD"]
CRYPTO = ["BTCUSDT", "ETHUSDT"]

last_signal_cache = {}


# 📊 calcul volatilité
def get_volatility(df):

    avg_range = (df["high"] - df["low"]).tail(10).mean()

    return avg_range


# ⚡ vitesse dynamique
def dynamic_sleep(volatility):

    # 🔥 marché très actif
    if volatility > 0.005:
        return 1

    # ⚡ actif moyen
    elif volatility > 0.002:
        return 3

    # 💤 marché calme
    else:
        return 5


def run():

    while True:

        max_volatility = 0

        # 🌍 FOREX
        for pair in FOREX:

            df = get_forex(pair)

            if df is None:
                continue

            df = add_indicators(df)

            # 📊 volatilité
            volatility = get_volatility(df)

            if volatility > max_volatility:
                max_volatility = volatility

            signal = generate_signal(df)

            if signal:

                key = f"{pair}_{signal['signal']}"

                if last_signal_cache.get(key) == signal:
                    continue

                last_signal_cache[key] = signal

                print("FOREX:", pair, signal)


        # ₿ CRYPTO
        for coin in CRYPTO:

            df = get_crypto(coin)

            df = add_indicators(df)

            volatility = get_volatility(df)

            if volatility > max_volatility:
                max_volatility = volatility

            signal = generate_signal(df)

            if signal:

                key = f"{coin}_{signal['signal']}"

                if last_signal_cache.get(key) == signal:
                    continue

                last_signal_cache[key] = signal

                print("CRYPTO:", coin, signal)


        # ⚡ vitesse dynamique
        sleep_time = dynamic_sleep(max_volatility)

        print(f"⚡ NEXT SCAN IN {sleep_time}s")

        time.sleep(sleep_time)
