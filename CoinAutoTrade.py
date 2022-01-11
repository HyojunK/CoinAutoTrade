import pyupbit
import time
import datetime

class autoTrade :
    def __init__(self, start_cash) :
        self.fee = 0.05 # 수수료
        self.target_price = 0 # 목표 매수가
        self.bull = False # 상승장 여부
        
        self.start_cash = start_cash # 시작 자산
        self.current_cash = start_cash # 현재 자산
        self.highest_cash = start_cash # 자산 최고점
        self.lowest_cash = start_cash # 자산 최저점

        self.ror = 1 # 수익률

        self.trade_count = 0 # 거래횟수
        self.win_count = 0 # 승리횟수

    def start(self) :
        while True :
            current_price = pyupbit.get_current_price("KRW-BTC")
            print(current_price)
            time.sleep(1)

    def get_today_data(self) :
        daily_data = pyupbit.get_ohlcv("KRW-BTC", count=41)
        # 노이즈 계산 ( 1- 절대값(시가 - 종가) / (고가 - 저가) )
        daily_data['noise'] = 1 - abs(daily_data['open'] - daily_data['close']) / (daily_data['high'] - daily_data['low'])
        # 노이즈 20일 평균
        daily_data['noise_ma20'] = daily_data['noise'].rolling(window=20).mean().shift(1)
       
        # 변동폭 ( 고가 - 저가 )
        daily_data['range'] = daily_data['high'] - daily_data['low']
        # 목표매수가 ( 시가 + 변동폭 * K )
        daily_data['targetPrice'] = daily_data['open'] + daily_data['range'].shift(1) * daily_data['noise_ma20']

        # 5일 이동평균선
        daily_data['ma5'] = daily_data['close'].rolling(window=5, min_periods=1).mean().shift(1)
        # 상승장 여부
        daily_data['bull'] = daily_data['open'] > daily_data['ma5']

        today = daily_data.iloc[-1]

        return today

tradingBot = autoTrade(1000000)
today_data = tradingBot.start()