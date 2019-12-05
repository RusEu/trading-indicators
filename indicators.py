def vwma(x, volume, period):
    import talib as ta
    return ta.SMA(x * volume, period) / ta.SMA(volume, period)

def trend(high, low, close, factor=3, pd=14):
    import numpy as np
    import talib as ta
    
    hl2 = (high + low) / 2
    atr = np.nan_to_num(ta.ATR(high, low, close, timeperiod=14), 0)
    Close = close
    Up = (hl2 - (factor * atr))
    Dn = (hl2 + (factor * atr))

    TrendUp = Up
    TrendDown = Dn
    Trend = np.array([1])

    for index, _ in enumerate(Close):
        if index == 0:
            continue

        if Close[index - 1] > TrendUp[index - 1]:
            TrendUp[index] = max(Up[index], TrendUp[index - 1])
        else:
            TrendUp[index] = Up[index]

        if Close[index - 1] < TrendDown[index - 1]:
            TrendDown[index] = min(Dn[index], TrendDown[index - 1])
        else:
            TrendDown[index] = Dn[index]

        if Close[index] > TrendDown[index - 1]:
            Trend = np.append(Trend,1)
        elif Close[index] < TrendUp[index - 1]:
            Trend = np.append(Trend, -1)
        elif Trend[index - 1]:
            Trend = np.append(Trend, Trend[index - 1])
        else:
            Trend = np.append(Trend, 1)
    
    return Trend

def mmar(close):
    import numpy as np
    import pandas as pd
    import talib as ta

    df = pd.DataFrame.from_dict(dict(
        ma05 = ta.EMA(close, 5),
        ma10 = ta.EMA(close, 10),
        ma20 = ta.EMA(close, 20),
        ma30 = ta.EMA(close, 30),
        ma40 = ta.EMA(close, 40),
        ma50 = ta.EMA(close, 50),
        ma60 = ta.EMA(close, 60),
        ma70 = ta.EMA(close, 70),
        ma80 = ta.EMA(close, 80),
        ma90 = ta.EMA(close, 90),
        ma100 = ta.EMA(close, 100)
    ))

    leadMAColor = pd.Series(np.full(len(close), 'gray'))
    leadMAColor = np.where(((df['ma05'] - df['ma05'].shift(1)) >= 0) & (df['ma05'] < df['ma100']), 'green', leadMAColor)
    leadMAColor = np.where(((df['ma05'] - df['ma05'].shift(1)) <= 0) & (df['ma05'] < df['ma100']), 'red', leadMAColor)
    leadMAColor = np.where(((df['ma05'] - df['ma05'].shift(1)) < 0) & (df['ma05'] > df['ma100']), 'maroon', leadMAColor)
    leadMAColor = np.where(((df['ma05'] - df['ma05'].shift(1)) >= 0) & (df['ma05'] > df['ma100']), 'lime', leadMAColor)

    def maColor(ma, mal):
        color = pd.Series(np.full(len(ma), 'gray'))
        color = np.where(((ma - mal) >= 0) & (ma < df['ma100']), 'green', color)
        color = np.where(((ma - mal) <= 0) & (ma < df['ma100']), 'red', color)
        color = np.where(((ma - mal) < 0) & (ma > df['ma100']), 'maroon', color)
        color = np.where(((ma - mal) >= 0) & (ma > df['ma100']), 'lime', color)
        return color

    return pd.DataFrame.from_dict(
        dict(
            leadMA_c=leadMAColor,
            ma05_c = maColor(df['ma05'], df['ma05'].shift(1)),
            ma10_c = maColor(df['ma10'], df['ma10'].shift(1)),
            ma20_c = maColor(df['ma20'], df['ma20'].shift(1)),
            ma30_c = maColor(df['ma30'], df['ma30'].shift(1)),
            ma40_c = maColor(df['ma40'], df['ma40'].shift(1)),
            ma50_c = maColor(df['ma50'], df['ma50'].shift(1)),
            ma60_c = maColor(df['ma60'], df['ma60'].shift(1)),
            ma70_c = maColor(df['ma70'], df['ma70'].shift(1)),
            ma80_c = maColor(df['ma80'], df['ma80'].shift(1)),
            ma90_c = maColor(df['ma90'], df['ma90'].shift(1))  
        )
    )
    
def fibonacci_bands(high, low, close, volume, mult=3.0, period=200):
    hlc3 = (high + low + close) / 3
    dev = mult * hlc3.rolling(period).std()
    basis = vwma(hlc3, volume, period)
    
    upper_1 = basis + (0.236 * dev)
    upper_2 = basis + (0.382 * dev)
    upper_3 = basis + (0.5 * dev)
    upper_4 = basis + (0.618 * dev)
    upper_5 = basis + (0.764 * dev)
    upper_6 = basis + (1 * dev)
    lower_1 = basis - (0.236 * dev)
    lower_2 = basis - (0.382 * dev)
    lower_3 = basis - (0.5 * dev)
    lower_4 = basis - (0.618 * dev)
    lower_5 = basis - (0.764 * dev)
    lower_6 = basis - (1 * dev)
    upper_basis = upper_6 - basis
    
    return dict(
        upper_1=upper_1,
        upper_2=upper_2,
        upper_3=upper_3,
        upper_4=upper_4,
        upper_5=upper_5,
        upper_6=upper_6,
        lower_1=lower_1,
        lower_2=lower_2,
        lower_3=lower_3,
        lower_4=lower_4,
        lower_5=lower_5,
        lower_6=lower_6,
        upper_basis=upper_basis
    )