import pyupbit
import time
import datetime
import math
import requests

class autoTrade :
    def __init__(self, start_cash, ticker) :
        self.fee = 0.05 # 수수료
        self.target_price = 0 # 목표 매수가
        self.bull = False # 상승장 여부
        self.ticker = ticker # 티커
        self.buy_yn = False # 매수 여부

        self.start_cash = start_cash # 시작 자산

        self.get_today_data()

    def start(self) :
        now = datetime.datetime.now() # 현재 시간
        slackBot.message("자동 매매 프로그램이 시작되었습니다\n시작 시간 : " + str(now) + "\n매매 대상 : " + self.ticker + "\n시작 자산 : " + str(self.start_cash))
        openTime = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1) # 자정

        while True :
            try :
                now = datetime.datetime.now()

                if openTime < now < openTime + datetime.timedelta(seconds=5) :
                    openTime = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
                    self.sell_coin() # 매도 시도
                    self.get_today_data() # 데이터 갱신

                current_price = pyupbit.get_current_price(self.ticker)
                if((current_price >= self.target_price) and self.bull and not self.buy_yn) : # 매수 시도
                    self.buy_coin()
            except :
                slackBot.message("!!! 프로그램 오류 발생 !!!")

            time.sleep(1)

    def get_today_data(self) :
        daily_data = pyupbit.get_ohlcv(self.ticker, count=41)
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

        self.target_price = today.targetPrice
        self.bull = today.bull

    def buy_coin(self) :
        balance = upbit.get_balance() # 잔고 조회
        
        if balance > 5000 : # 잔고 5000원 이상일 때
            upbit.buy_market_order(self.ticker, balance * 0.9995)
            self.buy_yn = True

            buy_price = pyupbit.get_orderbook("KRW-BTC")['orderbook_units'][0]['ask_price'] # 최우선 매도 호가
            slackBot.message("#매수 주문\n매수 주문 가격 : " + buy_price + "원")

    def sell_coin(self) :
        balance = upbit.get_balance("KRW_BTC") # 잔고 조회

        upbit.sell_market_order(ticker, balance)
        self.buy_yn = False

        sell_price = pyupbit.get_orderbook("KRW-BTC")['orderbook_units'][0]['bid_price'] # 최우선 매수 호가
        slackBot.message("#매도 주문\n매도 주문 가격 : " + sell_price + "원")

class slack :
    def __init__(self, token, channel) :
        self.token = token
        self.channel = channel

    def message(self, message):
        response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + self.token},
        data={"channel": self.channel,"text": message}
    )

with open("key_info.txt") as f :
    lines = f.readlines()
    acc_key = lines[0].strip()    # Access Key
    sec_key = lines[1].strip()    # Secret Key
    app_token = lines[2].strip()  # App Token
    channel = lines[3].strip()    # Slack Channel Name

upbit = pyupbit.Upbit(acc_key, sec_key)
slackBot = slack(app_token, channel)

start_cash = upbit.get_balance()
ticker = "KRW-BTC"
tradingBot = autoTrade(start_cash, ticker)
tradingBot.start()
