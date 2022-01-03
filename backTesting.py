import pyupbit
import numpy as np

df = pyupbit.get_ohlcv("KRW-BTC", count=15)
df['range(변동폭*k)'] = (df['high'] - df['low']) * 0.7
df['target(매수가)'] = df['open'] + df['range(변동폭*k)'].shift(1)

df['ROR(수익률)'] = np.where(df['high'] > df['target(매수가)'],
                     df['close'] / df['target(매수가)'],
                     1)

df['HPR(누적수익률)'] = df['ROR(수익률)'].cumprod()
df['DD(낙폭)'] = (df['HPR(누적수익률)'].cummax() - df['HPR(누적수익률)']) / df['HPR(누적수익률)'].cummax() * 100
df.to_excel("backTesting_result.xlsx")