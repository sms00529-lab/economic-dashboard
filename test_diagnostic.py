#!/usr/bin/env python3
"""
디버깅용 테스트 스크립트
각 단계별로 어디서 실패하는지 확인
"""

import sys
import os

print("=" * 60)
print("🔍 진단 시작")
print("=" * 60)

# 1. Python 버전
print(f"\n1️⃣ Python 버전: {sys.version}")

# 2. 필수 패키지 확인
print("\n2️⃣ 패키지 확인:")
packages = ['requests', 'yfinance']
for pkg in packages:
    try:
        __import__(pkg)
        print(f"   ✅ {pkg}")
    except ImportError:
        print(f"   ❌ {pkg} - 설치 안됨!")

# 3. 현재 디렉토리
print(f"\n3️⃣ 현재 디렉토리: {os.getcwd()}")

# 4. 파일 확인
print("\n4️⃣ 파일 확인:")
files = ['index.html', 'auto_update_all_indicators.py', 'auto_update_official_data.py']
for f in files:
    if os.path.exists(f):
        print(f"   ✅ {f}")
    else:
        print(f"   ❌ {f} - 없음!")

# 5. yfinance 테스트
print("\n5️⃣ yfinance 테스트:")
try:
    import yfinance as yf
    ticker = yf.Ticker("^KS11")
    hist = ticker.history(period="1d")
    if len(hist) > 0:
        print(f"   ✅ KOSPI: {hist['Close'][-1]:.2f}")
    else:
        print("   ⚠️  데이터 없음")
except Exception as e:
    print(f"   ❌ 에러: {e}")

# 6. 업비트 API 테스트
print("\n6️⃣ 업비트 API 테스트:")
try:
    import requests
    response = requests.get('https://api.upbit.com/v1/ticker?markets=KRW-BTC', timeout=5)
    data = response.json()[0]
    print(f"   ✅ Bitcoin: {data['trade_price']:,}원")
except Exception as e:
    print(f"   ❌ 에러: {e}")

# 7. index.html 읽기 테스트
print("\n7️⃣ index.html 읽기 테스트:")
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"   ✅ 파일 크기: {len(content):,} bytes")
        
        # MANUAL_DATA 찾기
        if 'const MANUAL_DATA' in content:
            print("   ✅ MANUAL_DATA 섹션 있음")
        else:
            print("   ❌ MANUAL_DATA 섹션 없음!")
except Exception as e:
    print(f"   ❌ 에러: {e}")

print("\n" + "=" * 60)
print("✅ 진단 완료")
print("=" * 60)
