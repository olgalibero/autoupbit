import time
import pyupbit
import datetime

access = ""
secret = ""

# Modify the interval from 'day' to 'minute720' for 12-hour intervals

# Get target price
def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="minute720", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

# Get start time of the current 12-hour interval
def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute720", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# The rest of the functions remain unchanged

# Login
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# Auto-trading start
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        # Calculate end time for the 12-hour interval
        end_time = start_time + datetime.timedelta(hours=12)

        # Trading logic
        if start_time < now < end_time - datetime.timedelta(seconds=30):
            target_price = get_target_price("KRW-BTC", 0.45)
            current_price = get_current_price("KRW-BTC")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
        else:
            btc = get_balance("BTC")
            if btc > 0.00009:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
