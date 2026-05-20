import time
from market import get_data
from indicators import add_indicators
from strategy import generate_signal

ASSETS = ["XAU/USD", "XAG/USD", "UKOIL", "USOIL"]

def run():
    while True:
        for asset in ASSETS:

            df = get_data(asset)
            df = add_indicators(df)

            signal = generate_signal(df)

            if signal:
                print(asset, signal)

        time.sleep(2)
