#!/usr/bin/env python3
"""
실시간 경제지표 대시보드 - 진짜 자동 업데이트
기본값 없음 - API 실패 시 에러 발생
"""

import yfinance as yf
import requests
import re
from datetime import datetime
import os
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================================================================
# 주요 지수 (6개) - 기본값 없음
# ============================================================================

def get_kospi():
    """KOSPI 실시간 - 실패 시 None"""
    ticker = yf.Ticker("^KS11")
    ticker.session.verify = False
    hist = ticker.history(period="2d")
    if len(hist) >= 2:
        current = hist['Close'][-1]
        previous = hist['Close'][-2]
        change = ((current - previous) / previous) * 100
        print(f"✅ KOSPI: {current:.2f} ({change:+.2f}%)")
        return {"value": round(current, 2), "change": round(change, 2)}
    raise Exception("KOSPI 데이터 없음")

def get_nasdaq():
    """NASDAQ 실시간 - 실패 시 None"""
    ticker = yf.Ticker("^IXIC")
    ticker.session.verify = False
    hist = ticker.history(period="2d")
    if len(hist) >= 2:
        current = hist['Close'][-1]
        previous = hist['Close'][-2]
        change = ((current - previous) / previous) * 100
        print(f"✅ NASDAQ: {current:.2f} ({change:+.2f}%)")
        return {"value": round(current, 2), "change": round(change, 2)}
    raise Exception("NASDAQ 데이터 없음")

def get_bitcoin():
    """비트코인 실시간 (업비트 KRW) - 실패 시 None"""
    response = requests.get(
        'https://api.upbit.com/v1/ticker?markets=KRW-BTC',
        timeout=10, verify=False
    )
    data = response.json()[0]
    price = int(data['trade_price'])
    change = data['signed_change_rate'] * 100
    
    print(f"✅ Bitcoin: {price:,}원 ({change:+.2f}%)")
    return {"value": price, "change": round(change, 2)}

def get_gold():
    """금 실시간 - 실패 시 None"""
    ticker = yf.Ticker("GC=F")
    ticker.session.verify = False
    hist = ticker.history(period="2d")
    if len(hist) >= 2:
        current = hist['Close'][-1]
        previous = hist['Close'][-2]
        change = ((current - previous) / previous) * 100
        print(f"✅ Gold: ${current:.2f} ({change:+.2f}%)")
        return {"value": round(current, 2), "change": round(change, 2)}
    raise Exception("Gold 데이터 없음")

def get_oil():
    """원유 실시간 (WTI 선물) - 실패 시 None"""
    ticker = yf.Ticker("CL=F")
    ticker.session.verify = False
    hist = ticker.history(period="2d")
    if len(hist) >= 2:
        current = hist['Close'][-1]
        previous = hist['Close'][-2]
        change = ((current - previous) / previous) * 100
        print(f"✅ Oil (WTI): ${current:.2f} ({change:+.2f}%)")
        return {"value": round(current, 2), "change": round(change, 2)}
    raise Exception("Oil 데이터 없음")

def get_exchange():
    """USD/KRW 실시간 - 실패 시 None"""
    ticker = yf.Ticker("KRW=X")
    ticker.session.verify = False
    hist = ticker.history(period="2d")
    if len(hist) >= 2:
        current = hist['Close'][-1]
        previous = hist['Close'][-2]
        change = ((current - previous) / previous) * 100
        print(f"✅ USD/KRW: ₩{current:.2f} ({change:+.2f}%)")
        return {"value": round(current, 2), "change": round(change, 2)}
    raise Exception("USD/KRW 데이터 없음")

# ============================================================================
# HTML 업데이트
# ============================================================================

def update_html(main_data, html_path='index.html'):
    """HTML 파일 업데이트 - 실패 시 예외 발생"""
    
    # 파일 존재 확인
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"index.html 파일이 없습니다: {html_path}")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # MANUAL_DATA 섹션 확인
    if 'const MANUAL_DATA' not in content:
        raise ValueError("index.html에 MANUAL_DATA 섹션이 없습니다!")
    
    # MANUAL_DATA 업데이트
    manual_data_str = f"""const MANUAL_DATA = {{
            kospi: {{ value: {main_data['kospi']['value']}, change: {main_data['kospi']['change']} }},
            nasdaq: {{ value: {main_data['nasdaq']['value']}, change: {main_data['nasdaq']['change']} }},
            bitcoin: {{ value: {main_data['bitcoin']['value']}, change: {main_data['bitcoin']['change']} }},
            gold: {{ value: {main_data['gold']['value']}, change: {main_data['gold']['change']} }},
            oil: {{ value: {main_data['oil']['value']}, change: {main_data['oil']['change']} }},
            exchange: {{ value: {main_data['exchange']['value']}, change: {main_data['exchange']['change']} }}
        }};"""
    
    # 중첩 중괄호를 처리하는 정규식 (non-greedy 방식)
    pattern = r'const MANUAL_DATA = \{[\s\S]*?\};'
    content = re.sub(pattern, manual_data_str, content)
    
    # 파일 저장
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ HTML 업데이트 완료: {html_path}")
    print(f"   시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================================================
# 메인 함수
# ============================================================================

def main():
    """전체 데이터 수집 및 업데이트 - 실패 시 exit code 1"""
    print("=" * 80)
    print(f"🚀 실시간 지수 업데이트 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    try:
        print("\n📊 주요 지수 수집 중...")
        
        main_data = {
            'kospi': get_kospi(),
            'nasdaq': get_nasdaq(),
            'bitcoin': get_bitcoin(),
            'gold': get_gold(),
            'oil': get_oil(),
            'exchange': get_exchange()
        }
        
        # HTML 업데이트
        update_html(main_data)
        
        print("\n✅ 모든 작업 완료!")
        print("=" * 80)
        return 0  # 성공
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()
        return 1  # 실패
    
if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
