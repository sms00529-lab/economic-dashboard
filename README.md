# 📊 투자자를 위한 경제지표 대시보드

실시간 경제지표를 한눈에! 부동산 투자 의사결정을 위한 핵심 지표 대시보드

🔗 **라이브**: https://sms00529-lab.github.io/economic-dashboard/

---

## ⚡ 이원화 자동 업데이트 시스템

### 🔥 실시간 지수 (5분마다)
```
KOSPI, NASDAQ, Bitcoin, Gold, Oil, USD/KRW
→ 평일 장중 5분마다 업데이트
→ 스크립트: auto_update_all_indicators.py
```

### 🏛️ 공식 지표 (하루 1회)
```
한국 기준금리 (한국은행 API)
미국 기준금리 (FRED API)
한국 국채 10년 (한국은행 API)
미국 국채 10년 (FRED API)
→ 매일 오전 9시 업데이트
→ 스크립트: auto_update_official_data.py
```

---

## 📊 대시보드 구조

### 탭 1: 주요 지수 (6개)
24시간 미니 차트 + 실시간 변동률

### 탭 2: 금리 비교
한미 기준금리 18년 비교 (2008~2025)

### 탭 3: 국채 비교
한미 국채 10년물 24개월 추세

### 탭 4: 통화량 비교
한미 M2 10년 비교 (정규화)

### 탭 5: 성장률 & 물가
GDP / CPI 비교

---

## 🔑 API 키 발급

### 한국은행 ECOS (무료)
```
https://ecos.bok.or.kr/
→ 회원가입 → 인증키 신청 → 즉시 발급
```

### FRED (무료)
```
https://fredaccount.stlouisfed.org/apikeys
→ Request API Key → 즉시 발급
```

---

## 🚀 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/sms00529-lab/economic-dashboard.git
cd economic-dashboard
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. API 키 설정
```python
# auto_update_official_data.py
BOK_API_KEY = "여기에_입력"
FRED_API_KEY = "여기에_입력"
```

### 4. GitHub에 배포
```bash
git add .
git commit -m "자동화 설정 완료"
git push
```

### 5. GitHub Pages 활성화
```
Settings → Pages → Source: main 브랜치
```

---

## 📁 파일 구조

```
economic-dashboard/
├── index.html                          # 메인 대시보드
├── auto_update_all_indicators.py       # 실시간 지수 (5분)
├── auto_update_official_data.py        # 공식 지표 (하루)
├── requirements.txt                    # Python 패키지
├── .github/workflows/
│   └── update-dashboard.yml            # GitHub Actions
└── README.md
```

---

## 💰 비용

```
한국은행 API:    무료
FRED API:        무료
GitHub Pages:    무료
GitHub Actions:  무료 (월 2,000분)

총 비용: 0원! 🎉
```

---

## 🎨 기술 스택

- HTML5 / CSS3 / JavaScript
- Chart.js 4.4.0
- Python 3.11
- 한국은행 ECOS API
- FRED API
- yfinance / 업비트 API
- GitHub Pages + Actions

---

## 📞 문의

**Instagram**: [@Chok.sense1](https://www.instagram.com/chok.sense1)

부산 부동산 투자 전문 | 투자센스촉센세

---

**Made with ❤️ by @Chok.sense1**
