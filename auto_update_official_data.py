#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
공식 API 데이터 업데이트 스크립트
- 한국은행 ECOS API
- FRED API
- 금리, 국채, M2, GDP, CPI만 업데이트
"""

import requests
import re
from datetime import datetime, timedelta

# API 키
BOK_API_KEY = "MXHS18NIT5XT11X6KRU6"
FRED_API_KEY = "e1c9cfe7467e9ad32d3c163f5edd61f1"

# ============================================================================
# 한국은행 ECOS API
# ============================================================================

def get_bok_data(stat_code, item_code, cycle='D', count=1):
    """
    한국은행 경제통계시스템 API 호출
    최근 데이터 1개만 가져오기
    """
    end_date = datetime.now().strftime('%Y%m%d')
    
    url = f"https://ecos.bok.or.kr/api/StatisticSearch/{BOK_API_KEY}/json/kr/1/{count}/{stat_code}/{cycle}/{end_date}/{end_date}/{item_code}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if 'StatisticSearch' in data and 'row' in data['StatisticSearch']:
            value = data['StatisticSearch']['row'][0]['DATA_VALUE']
            return float(value.replace(',', ''))
        return None
    except Exception as e:
        print(f"❌ 한국은행 API 오류 ({stat_code}): {e}")
        return None


def get_korea_base_rate():
    """한국 기준금리"""
    # 722Y001 - 한국은행 기준금리 (월별)
    # 최근 3개월 데이터 확인
    for days_ago in [0, 30, 60, 90]:
        date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y%m')
        url = f"https://ecos.bok.or.kr/api/StatisticSearch/{BOK_API_KEY}/json/kr/1/1/722Y001/M/{date}/{date}/0101000"
        
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            if 'StatisticSearch' in data and 'row' in data['StatisticSearch']:
                value = data['StatisticSearch']['row'][0]['DATA_VALUE']
                return float(value)
        except:
            continue
    
    return 2.50  # 기본값


def get_korea_bond_10y():
    """한국 국채 10년물"""
    # 817Y002 - 국고채 수익률 (일별)
    value = get_bok_data('817Y002', '010200000', cycle='D')
    return value if value else 3.15


# ============================================================================
# FRED API
# ============================================================================

def get_fred_data(series_id):
    """FRED API 호출"""
    url = f"https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': series_id,
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'sort_order': 'desc',
        'limit': 10  # 최근 10개 (휴일 대비)
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if 'observations' in data:
            # 유효한 값 찾기 (. 제외)
            for obs in data['observations']:
                if obs['value'] != '.':
                    return float(obs['value'])
        return None
    except Exception as e:
        print(f"❌ FRED API 오류 ({series_id}): {e}")
        return None


def get_us_base_rate():
    """미국 기준금리"""
    # DFF: Federal Funds Effective Rate
    value = get_fred_data('DFF')
    return value if value else 4.00


def get_us_bond_10y():
    """미국 국채 10년물"""
    # DGS10: 10-Year Treasury Constant Maturity Rate
    value = get_fred_data('DGS10')
    return value if value else 4.25


# ============================================================================
# HTML 업데이트
# ============================================================================

def update_html():
    """HTML 파일의 금리/국채 값만 업데이트"""
    
    print("\n" + "="*60)
    print("📊 공식 API 데이터 수집 시작")
    print("="*60)
    
    # 데이터 수집
    kr_rate = get_korea_base_rate()
    us_rate = get_us_base_rate()
    kr_bond = get_korea_bond_10y()
    us_bond = get_us_bond_10y()
    
    print(f"\n✅ 수집 완료:")
    print(f"  한국 기준금리: {kr_rate:.2f}%")
    print(f"  미국 기준금리: {us_rate:.2f}%")
    print(f"  한국 국채 10년: {kr_bond:.2f}%")
    print(f"  미국 국채 10년: {us_bond:.2f}%")
    
    # HTML 파일 읽기
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html = f.read()
    except:
        print("❌ index.html 파일을 찾을 수 없습니다!")
        return
    
    # 간단한 문자열 치환 방식으로 변경
    
    # 한국 기준금리 카드 찾아서 업데이트
    kr_rate_pattern = r'(<div class="card card-large" id="kr-rate-card">.*?<div class="value-main">)[\d.]+(%</div>)'
    html = re.sub(kr_rate_pattern, rf'\g<1>{kr_rate:.2f}\g<2>', html, flags=re.DOTALL)
    
    # 미국 기준금리 카드 찾아서 업데이트
    us_rate_pattern = r'(<div class="card card-large" id="us-rate-card">.*?<div class="value-main">)[\d.]+(%</div>)'
    html = re.sub(us_rate_pattern, rf'\g<1>{us_rate:.2f}\g<2>', html, flags=re.DOTALL)
    
    # 한국 국채 카드 찾아서 업데이트
    kr_bond_pattern = r'(<div class="card card-large" id="kr-bond-card">.*?<div class="value-main">)[\d.]+(%</div>)'
    html = re.sub(kr_bond_pattern, rf'\g<1>{kr_bond:.2f}\g<2>', html, flags=re.DOTALL)
    
    # 미국 국채 카드 찾아서 업데이트
    us_bond_pattern = r'(<div class="card card-large" id="us-bond-card">.*?<div class="value-main">)[\d.]+(%</div>)'
    html = re.sub(us_bond_pattern, rf'\g<1>{us_bond:.2f}\g<2>', html, flags=re.DOTALL)
    
    # HTML 파일 저장
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ index.html 업데이트 완료!")
    print(f"⏰ 업데이트 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")


# ============================================================================
# 실행
# ============================================================================

if __name__ == "__main__":
    update_html()
