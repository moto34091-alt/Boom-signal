from filters import fake_spike
from smart_money import liquidity_sweep, consolidation

def generate_signal(df):
    last = df.iloc[-1]

    score = 0
    direction = None

    # trend
    if last["ema5"] > last["ema13"]:
        score += 25
        direction = "BUY"

    if last["ema5"] < last["ema13"]:
        score += 25
        direction = "SELL"

    # RSI
    if 50 < last["rsi"] < 70:
        score += 20
    elif 30 < last["rsi"] < 50:
        score += 20

    # filters
    if fake_spike(df):
        return None

    if liquidity_sweep(df):
        score -= 20

    if consolidation(df):
        score -= 15

    if score >= 80:
        return {
            "signal": direction,
            "score": score,
            "rsi": round(last["rsi"], 2)
        }

    return None
