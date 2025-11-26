# 오픈다트 재무데이터 시각화 분석 서비스

한국 기업의 재무 데이터를 검색하고 시각화하며 AI로 분석하는 웹 서비스입니다.

## 주요 기능

1. **회사 검색**: 회사명으로 검색하여 고유번호(corp_code) 조회
2. **재무 데이터 시각화**: 오픈다트 API를 통한 재무 정보 차트 시각화
3. **AI 분석**: Gemini AI를 활용한 재무 데이터 자동 분석

## 기술 스택

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **APIs**: 
  - 오픈다트 API (재무 데이터)
  - Google Gemini API (AI 분석)

## 설치 및 실행

### 1. 저장소 클론
```bash
git clone <repository-url>
cd fs-project2
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env` 파일을 생성하거나 환경 변수를 설정하세요:

```bash
export OPENDART_API_KEY=your_opendart_api_key
export GEMINI_API_KEY=your_gemini_api_key
```

또는 `env.example` 파일을 참고하여 `.env` 파일을 생성하세요.

### 4. 서버 실행

개발 모드:
```bash
python app.py
```

프로덕션 모드:
```bash
gunicorn app:app --bind 0.0.0.0:5001
```

서버는 `http://localhost:5001`에서 실행됩니다.

## 배포

자세한 배포 가이드는 [DEPLOY.md](DEPLOY.md)를 참고하세요.

### 빠른 배포 (Render 추천)

1. GitHub에 저장소 푸시
2. [Render](https://render.com)에서 새 Web Service 생성
3. 환경 변수 설정:
   - `OPENDART_API_KEY`
   - `GEMINI_API_KEY`
4. 배포 완료!

### 배포된 웹사이트

배포된 웹사이트는 [Render 대시보드](https://dashboard.render.com)에서 확인하거나, GitHub 저장소 페이지의 "About" 섹션에서 확인할 수 있습니다.

## 프로젝트 구조

```
fs-project2/
├── app.py                 # Flask 메인 애플리케이션
├── corp_parser.py         # XML 파서 및 데이터베이스
├── opendart_api.py        # 오픈다트 API 클라이언트
├── gemini_analyzer.py     # Gemini AI 분석 모듈
├── corp.xml              # 회사 정보 데이터베이스
├── requirements.txt       # Python 의존성
├── Procfile              # 배포 설정 (Heroku/Render)
├── runtime.txt           # Python 버전
├── templates/            # HTML 템플릿
│   ├── index.html        # 검색 페이지
│   └── financial.html    # 재무 정보 페이지
└── DEPLOY.md             # 배포 가이드
```

## API 엔드포인트

- `GET /`: 메인 검색 페이지
- `GET /api/search?q=<query>`: 회사명 검색
- `GET /api/stats`: 통계 정보
- `GET /api/financial?corp_code=<code>&bsns_year=<year>&reprt_code=<code>`: 재무 데이터 조회
- `POST /api/analyze`: AI 재무 분석
- `GET /financial/<corp_code>`: 재무 정보 시각화 페이지

## 라이선스

이 프로젝트는 개인/교육 목적으로 사용할 수 있습니다.

## 문의

문제가 발생하거나 질문이 있으시면 이슈를 등록해주세요.

