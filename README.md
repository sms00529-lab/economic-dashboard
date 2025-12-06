# 📊 진짜 자동 경제지표 대시보드

**실시간 API 자동 수집** - 기본값 없음, 진짜 데이터만!

---

## 🚨 중요한 변경사항

### 이전 버전 (잘못된 방식):
- ❌ API 실패 시 기본값 사용
- ❌ 실패해도 성공한 것처럼 보임
- ❌ 가짜 자동화

### 현재 버전 (올바른 방식):
- ✅ API 실패 시 명확한 에러
- ✅ 진짜 실시간 데이터만 사용
- ✅ 진짜 자동화

---

## 🔍 진단 시스템

### 1. 문제 파악하기

**test_diagnostic.py** 실행:
```bash
python test_diagnostic.py
```

확인 항목:
- Python 버전
- 패키지 설치 (requests, yfinance)
- 파일 존재 여부 (index.html)
- API 연결 테스트
- 데이터 수집 테스트

### 2. GitHub Actions에서 진단

워크플로우에 **"시스템 진단"** 단계 추가됨:
```yaml
- name: 시스템 진단
  run: python test_diagnostic.py
```

실행 후 로그에서:
- ✅ 표시: 정상
- ❌ 표시: 문제 발견

---

## 📋 파일 구조

```
경제대시보드/
├── .github/
│   └── workflows/
│       └── update-dashboard.yml     # GitHub Actions (진단 포함)
├── index.html                       # 대시보드 HTML
├── auto_update_all_indicators.py    # 실시간 지수 (기본값 없음)
├── auto_update_official_data.py     # 공식 지표 (yfinance 우선)
├── test_diagnostic.py               # 진단 스크립트 ⭐ NEW
├── requirements.txt
└── README.md
```

---

## 🚀 설치 방법

### 1. 파일 업로드

**모든 파일을 GitHub 저장소에 업로드:**
- `update-dashboard.yml` → `.github/workflows/` 폴더에
- 나머지 파일들 → 루트 폴더에

### 2. Actions 권한 설정

```
Settings > Actions > General
→ Workflow permissions
→ ✅ Read and write permissions
→ Save
```

### 3. 테스트 실행

```
Actions 탭 > Run workflow
```

---

## 🔧 문제 해결

### exit code 2가 나온다면?

**1단계: 진단 로그 확인**
```
Actions 탭 > 실패한 워크플로우 클릭
→ "시스템 진단" 단계 확인
```

**2단계: 구체적인 에러 확인**
```
"실시간 지수 업데이트" 단계 클릭
→ 어느 API가 실패했는지 확인
```

**3단계: 로그 복사해서 문의**

---

## 📊 데이터 소스

### 실시간 지수 (yfinance):
- KOSPI (^KS11)
- NASDAQ (^IXIC)
- Bitcoin (업비트 API)
- Gold (GC=F)
- Oil (CL=F)
- USD/KRW (KRW=X)

### 공식 지표:
- 미국 국채 10년 (yfinance ^TNX 우선, FRED 백업)
- 한국 기준금리 (한국은행 ECOS API)
- 한국 국채 10년 (한국은행 ECOS API)
- 미국 기준금리 (FRED API)

---

## ⏰ 자동 실행

- **실시간 지수**: 5분마다 (평일 09:00-17:00)
- **공식 지표**: 매일 오전 9시

---

## 💡 API 키 (선택사항)

### GitHub Secrets 추가:
```
Settings > Secrets and variables > Actions

1. BOK_API_KEY: 한국은행 API 키
2. FRED_API_KEY: FRED API 키
```

**참고**: 
- yfinance는 API 키 불필요
- ECOS/FRED는 API 키 없으면 스크립트에 기본값 사용
- 기본값도 작동하지만, 본인 키 사용 권장

---

## 🎯 성공 기준

### ✅ 정상 작동:
```
🚀 실시간 지수 업데이트 시작
✅ KOSPI: 2500.00 (+1.23%)
✅ NASDAQ: 20000.00 (+0.50%)
✅ Bitcoin: 95,000,000원 (+2.15%)
✅ Gold: $2650.00 (-0.35%)
✅ Oil (WTI): $72.50 (+1.15%)
✅ USD/KRW: ₩1400.00 (+0.25%)
✅ HTML 업데이트 완료
✅ 모든 작업 완료!
```

### ❌ 실패 예시:
```
❌ 오류 발생: KOSPI 데이터 없음
exit code 1
```

→ **명확한 에러 메시지**로 문제 파악 가능!

---

## 📞 문의

**문제가 계속되면:**
1. `test_diagnostic.py` 실행 결과 캡처
2. GitHub Actions 실패 로그 캡처
3. 에러 메시지와 함께 이슈 생성

---

**Made with ❤️ by @Chok.sense1**

**진짜 자동화 = 진짜 데이터!** 🚀
