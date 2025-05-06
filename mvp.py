import ccxt
import pandas as pd
from datetime import datetime
import time

def get_binance_futures_klines(symbol='BTC/USDT', timeframe='15m', limit=96):
    """
    Binance 선물 거래소에서 캔들 데이터를 가져오는 함수
    
    Parameters:
    - symbol: 거래쌍 (예: 'BTC/USDT')
    - timeframe: 시간프레임 (예: '15m')
    - limit: 가져올 캔들 개수
    
    Returns:
    - pandas DataFrame with OHLCV data
    """
    try:
        # Binance 선물 거래소 객체 생성
        exchange = ccxt.binance({
            'enableRateLimit': True,  # API 호출 제한 준수
            'options': {
                'defaultType': 'future'  # 선물 거래소 사용
            }
        })
        
        # 캔들 데이터 가져오기
        ohlcv = exchange.fetch_ohlcv(
            symbol=symbol,
            timeframe=timeframe,
            limit=limit
        )
        
        # DataFrame으로 변환
        df = pd.DataFrame(
            ohlcv,
            columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
        )
        
        # timestamp를 datetime으로 변환
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # 인덱스를 timestamp로 설정
        df.set_index('timestamp', inplace=True)
        
        return df
    
    except Exception as e:
        print(f"에러 발생: {str(e)}")
        return None

if __name__ == "__main__":
    # BTC/USDT 15분봉 96개 가져오기
    df = get_binance_futures_klines()
    
    if df is not None:
        print("\n=== BTC/USDT 15분봉 데이터 ===")
        print(f"데이터 개수: {len(df)}")
        print("\n모든 캔들 데이터:")
        pd.set_option('display.max_rows', None)  # 모든 행 표시
        pd.set_option('display.max_columns', None)  # 모든 열 표시
        pd.set_option('display.width', None)  # 출력 너비 제한 해제
        print(df)
        
        # 데이터 저장
        df.to_csv('btc_15m_klines.csv')
        print("\n데이터가 'btc_15m_klines.csv' 파일로 저장되었습니다.") 