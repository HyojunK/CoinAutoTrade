import pyupbit
import time
import datetime

def get_target_price(ticker, k):
    data = pyupbit.get_ohlcv(ticker)

    # 전일 가격 데이터
    yesterday = data.iloc[-2]
    # 전일 종가(= 금일 시가)
    today_open = yesterday['close']
    # 변동폭 = 전일 고가 - 전일 저가
    range = yesterday['high'] - yesterday['low']
    # 목표가
    target = today_open + range * k

    return target

# 현재 시간
now = datetime.datetime.now()
# 시작 시간 (=자정)
openTime = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
# 목표가
targetPrice = get_target_price("KRW-BTC", 0.5)

while True:
    now = datetime.datetime.now()
    if openTime < now < openTime + datetime.timedelta(seconds=5) :
        targetPrice = get_target_price("KRW-BTC", 0.5)
        openTime = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        currentPrice = pyupbit.get_current_price("KRW-BTC")
        print(currentPrice)

    time.sleep(1)