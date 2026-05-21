def detect_order_block(df):

    # 🔍 recherche dernières bougies
    for i in range(len(df) - 5, len(df) - 2):

        candle = df.iloc[i]
        next_candle = df.iloc[i + 1]

        # 🟢 BUY ORDER BLOCK
        if candle["close"] < candle["open"]:

            impulsive_move = (
                next_candle["close"] - next_candle["open"]
            )

            if impulsive_move > (
                abs(candle["close"] - candle["open"]) * 1.5
            ):

                return {
                    "type": "BUY",
                    "high": candle["high"],
                    "low": candle["low"]
                }

        # 🔴 SELL ORDER BLOCK
        if candle["close"] > candle["open"]:

            impulsive_move = (
                next_candle["open"] - next_candle["close"]
            )

            if impulsive_move > (
                abs(candle["close"] - candle["open"]) * 1.5
            ):

                return {
                    "type": "SELL",
                    "high": candle["high"],
                    "low": candle["low"]
                }

    return None
