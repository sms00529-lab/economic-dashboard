#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
6개 주요 지수 자동 업데이트
KOSPI, NASDAQ, Bitcoin, Gold, Oil, USD/KRW
"""

import yfinance as yf
import requests
import re
import os
from datetime import datetime

# ============================================================================
# 6개 주요 지수
# ============================================================================

def get_kospi():
    """KOSPI"""
    try:
        ticker = yf.Ticker("^KS11")
        hist = ticker.history(period="2d")
        if len(hist) >= 2:
            current = hist['Close'][-1]
            previous = hist['Close'][-2]
            change = ((current - previous) / previous) * 100
            print(f"✅ KOSPI: {current:.2f} ({change:+.2f}%)")
            return {"value": round(current, 2), "change": round(change, 2)}
    except Exception as e:
        print(f"❌ KOSPI 에러: {e}")
    return None

def get_nasdaq():
    """NASDAQ"""
    try:
        ticker = yf.Ticker("^IXIC")
        hist = ticker.history(period="2d")
        if len(hist) >= 2:
            current = hist['Close'][-1]
            previous = hist['Close'][-2]
            change = ((current - previous) / previous) * 100
            print(f"✅ NASDAQ: {current:.2f} ({change:+.2f}%)")
            return {"value": round(current, 2), "change": round(change, 2)}
    except Exception as e:
        print(f"❌ NASDAQ 에러: {e}")
    return None

def get_bitcoin():
    """Bitcoin (업비트)"""
    try:
        response = requests.get(
            'https://api.upbit.com/v1/ticker?markets=KRW-BTC',
            timeout=10
        )
        data = response.json()[0]
        price = int(data['trade_price'])
        change = data['signed_change_rate'] * 100
        
        print(f"✅ Bitcoin: {price:,}원 ({change:+.2f}%)")
        return {"value": price, "change": round(change, 2)}
    except Exception as e:
        print(f"❌ Bitcoin 에러: {e}")
    return None

def get_gold():
    """Gold (국제금 현물 - XAU/USD)"""
    try:
        # 금 현물 가격 (온스당 달러)
        ticker = yf.Ticker("XAUUSD=X")
        hist = ticker.history(period="2d")
        if len(hist) >= 2:
            current = hist['Close'][-1]
            previous = hist['Close'][-2]
            change = ((current - previous) / previous) * 100
            print(f"✅ Gold (국제금): ${current:.2f} ({change:+.2f}%)")
            return {"value": round(current, 2), "change": round(change, 2)}
    except Exception as e:
        print(f"❌ Gold 에러: {e}")
        # 백업: GC=F (선물) 시도
        try:
            ticker = yf.Ticker("GC=F")
            hist = ticker.history(period="2d")
            if len(hist) >= 2:
                current = hist['Close'][-1]
                previous = hist['Close'][-2]
                change = ((current - previous) / previous) * 100
                print(f"✅ Gold (선물): ${current:.2f} ({change:+.2f}%)")
                return {"value": round(current, 2), "change": round(change, 2)}
        except:
            pass
    return None

def get_oil():
    """Oil (WTI)"""
    try:
        ticker = yf.Ticker("CL=F")
        hist = ticker.history(period="2d")
        if len(hist) >= 2:
            current = hist['Close'][-1]
            previous = hist['Close'][-2]
            change = ((current - previous) / previous) * 100
            print(f"✅ Oil: ${current:.2f} ({change:+.2f}%)")
            return {"value": round(current, 2), "change": round(change, 2)}
    except Exception as e:
        print(f"❌ Oil 에러: {e}")
    return None

def get_exchange():
    """USD/KRW"""
    try:
        ticker = yf.Ticker("KRW=X")
        hist = ticker.history(period="2d")
        if len(hist) >= 2:
            current = hist['Close'][-1]
            previous = hist['Close'][-2]
            change = ((current - previous) / previous) * 100
            print(f"✅ USD/KRW: ₩{current:.2f} ({change:+.2f}%)")
            return {"value": round(current, 2), "change": round(change, 2)}
    except Exception as e:
        print(f"❌ USD/KRW 에러: {e}")
    return None

# ============================================================================
# HTML 업데이트
# ============================================================================

def update_html():
    """HTML 파일의 MANUAL_DATA 업데이트"""
    
    print("\n" + "="*60)
    print("🚀 6개 주요 지수 업데이트 시작")
    print("="*60 + "\n")
    
    # 데이터 수집
    data = {
        'kospi': get_kospi(),
        'nasdaq': get_nasdaq(),
        'bitcoin': get_bitcoin(),
        'gold': get_gold(),
        'oil': get_oil(),
        'exchange': get_exchange()
    }
    
    # 실패한 항목 체크
    failed = [k for k, v in data.items() if v is None]
    if failed:
        print(f"\n⚠️  실패한 항목: {', '.join(failed)}")
        print("❌ 모든 데이터를 수집하지 못했습니다.")
        return False
    
    # HTML 파일 읽기
    html_path = 'index.html'
    if not os.path.exists(html_path):
        print(f"❌ HTML 파일을 찾을 수 없습니다: {html_path}")
        return False
        
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # MANUAL_DATA 업데이트
    manual_data = f"""const MANUAL_DATA = {{
        kospi: {{ value: {data['kospi']['value']}, change: {data['kospi']['change']} }},
        nasdaq: {{ value: {data['nasdaq']['value']}, change: {data['nasdaq']['change']} }},
        bitcoin: {{ value: {data['bitcoin']['value']}, change: {data['bitcoin']['change']} }},
        gold: {{ value: {data['gold']['value']}, change: {data['gold']['change']} }},
        oil: {{ value: {data['oil']['value']}, change: {data['oil']['change']} }},
        exchange: {{ value: {data['exchange']['value']}, change: {data['exchange']['change']} }}
    }};"""
    
    # 정규식으로 교체
    pattern = r'const MANUAL_DATA = \{[\s\S]*?\};'
    html = re.sub(pattern, manual_data, html)
    
    # HTML 파일 저장
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ index.html 업데이트 완료!")
    print(f"⏰ 업데이트 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    return True

# ============================================================================
# 메인
# ============================================================================

if __name__ == "__main__":
    success = update_html()
    exit(0 if success else 1)
