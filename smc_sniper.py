from market_structure import detect_structure
from choch_detector import detect_choch


def smc_signal(df):

    structure = detect_structure(df)
    choch = detect_choch(df)

    last = df.iloc[-1]

    score = 0

    # 📈 BOS continuation
    if structure:

        score += 40

        if structure["direction"] == "BUY":

            if last["ema5"] > last["ema13"]:
                score += 20

            if last["rsi"] > 55:
                score += 20

        if structure["direction"] == "SELL":

            if last["ema5"] < last["ema13"]:
                score += 20

            if last["rsi"] < 45:
                score += 20

        if score >= 80:

            return {
                "signal": structure["direction"],
                "type": "BOS",
                "score": score,
                "rsi": round(last["rsi"], 2)
            }

    # 🔄 CHOCH reversal
    if choch:

        score += 40

        if choch["direction"] == "BUY":

            if last["rsi"] > 50:
                score += 20

        if choch["direction"] == "SELL":

            if last["rsi"] < 50:
                score += 20

        if score >= 60:

            return {
                "signal": choch["direction"],
                "type": "CHOCH",
                "score": score,
                "rsi": round(last["rsi"], 2)
            }

    return None
