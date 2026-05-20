import time
import asyncio

from market import get_data
from indicators import add_indicators
from strategy import generate_signal
from telegram_bot import send_signal
from main import running

ASSETS = ["XAU/USD", "XAG/USD", "UKOIL", "USOIL"]

CHAT_ID = "TON_CHAT_ID"


def run():

    while True:

        if running:

            for asset in ASSETS:

                df = get_data(asset)
                df = add_indicators(df)

                signal = generate_signal(df)

                if signal:
                    print(asset, signal)

                    asyncio.run(
                        send_signal(CHAT_ID, asset, signal)
                    )

        time.sleep(2)
