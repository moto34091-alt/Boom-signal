def fake_spike(df):
    last = df.iloc[-1]

    body = abs(last["close"] - last["open"])
    range_ = last["high"] - last["low"]

    if range_ == 0:
        return True

    ratio = body / range_

    # spike suspect
    if ratio < 0.3:
        return True

    return False
