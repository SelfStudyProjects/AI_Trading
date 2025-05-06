import ccxt
import os
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
from openai import OpenAI
import math
import time

# API 키 확인
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY가 .env 파일에 설정되어 있지 않습니다.")

# 바이낸스 세팅
binance_api_key = os.getenv("BINANCE_API_KEY")
binance_secret = os.getenv("BINANCE_SECRET_KEY")
if not binance_api_key or not binance_secret:
    raise ValueError("BINANCE_API_KEY 또는 BINANCE_SECRET_KEY가 .env 파일에 설정되어 있지 않습니다.")

exchange = ccxt.binance({
    'apiKey': binance_api_key,
    'secret': binance_secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',
        'adjustForTimeDifference': True
    }
})

def get_ai_prediction(df):
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # gpt-4에서 gpt-3.5-turbo로 변경
            messages=[
                {
                    "role": "system",
                    "content": "You are a crypto trading expert. Analyze the market data and respond with only 'long' or 'short'."
                },
                {
                    "role": "user",
                    "content": df.to_json()
                }
            ]
        )
        return response.choices[0].message.content.lower()
    except Exception as e:
        print(f"OpenAI API 에러: {str(e)}")
        return None

def execute_trade(action, amount):
    try:
        # 레버리지 설정
        exchange.set_leverage(5, "BTC/USDT")
        
        # 포지션 진입
        if action == "long":
            order = exchange.create_market_buy_order("BTC/USDT", amount)
        elif action == "short":
            order = exchange.create_market_sell_order("BTC/USDT", amount)
        else:
            print("잘못된 액션입니다.")
            return None
            
        print(f"주문 실행 완료: {order}")
        return order
    except Exception as e:
        print(f"거래 실행 에러: {str(e)}")
        return None

# 메인 로직
try:
    # 차트 데이터 가져오기
    ohlcv = exchange.fetch_ohlcv("BTC/USDT", timeframe="15m", limit=96)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    # AI 투자 판단 받기
    action = get_ai_prediction(df)
    if action is None:
        print("AI 예측을 받지 못했습니다. 거래를 중단합니다.")
        exit()
    
    print(f"AI 예측: {action}")
    
    # 100 USDT 가치의 비트코인 수량 계산
    current_price = exchange.fetch_ticker("BTC/USDT")['last']
    amount = math.ceil((100 / current_price) * 1000) / 1000
    print(f"거래 수량: {amount} BTC")
    
    # 거래 실행
    execute_trade(action, amount)
    
except Exception as e:
    print(f"전체 프로세스 에러: {str(e)}")