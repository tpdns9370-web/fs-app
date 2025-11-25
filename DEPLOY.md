# 배포 가이드

오픈다트 재무데이터 시각화 분석 서비스를 배포하는 방법입니다.

## 배포 옵션

### 1. Render (추천) - 무료 플랜 제공

1. [Render](https://render.com)에 가입
2. "New +" → "Web Service" 선택
3. GitHub 저장소 연결 또는 직접 배포
4. 설정:
   - **Name**: 원하는 서비스 이름
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. 환경 변수 설정:
   - `OPENDART_API_KEY`: 오픈다트 API 키
   - `GEMINI_API_KEY`: Gemini API 키
6. "Create Web Service" 클릭

**장점**: 무료 플랜, 자동 HTTPS, 쉬운 설정

---

### 2. Railway - 간편한 배포

1. [Railway](https://railway.app)에 가입
2. "New Project" → "Deploy from GitHub repo" 선택
3. 저장소 선택 및 배포
4. 환경 변수 추가:
   - `OPENDART_API_KEY`
   - `GEMINI_API_KEY`
5. 자동 배포 완료

**장점**: 매우 간단한 배포, 자동 HTTPS

---

### 3. Heroku

1. [Heroku](https://www.heroku.com)에 가입
2. Heroku CLI 설치
3. 로그인:
   ```bash
   heroku login
   ```
4. 앱 생성:
   ```bash
   heroku create your-app-name
   ```
5. 환경 변수 설정:
   ```bash
   heroku config:set OPENDART_API_KEY=your_key
   heroku config:set GEMINI_API_KEY=your_key
   ```
6. 배포:
   ```bash
   git push heroku main
   ```

**참고**: Heroku는 무료 플랜이 종료되었습니다.

---

### 4. PythonAnywhere

1. [PythonAnywhere](https://www.pythonanywhere.com)에 가입 (무료 플랜)
2. Files 탭에서 파일 업로드
3. Web 탭에서 새 웹앱 생성
4. WSGI 설정 파일 수정:
   ```python
   import sys
   path = '/home/yourusername/yourproject'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```
5. 환경 변수는 Files 탭에서 `.env` 파일 생성

**장점**: 무료 플랜, Python 전용

---

### 5. Fly.io

1. [Fly.io](https://fly.io)에 가입
2. Fly CLI 설치:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```
3. 로그인:
   ```bash
   fly auth login
   ```
4. 앱 초기화:
   ```bash
   fly launch
   ```
5. 환경 변수 설정:
   ```bash
   fly secrets set OPENDART_API_KEY=your_key
   fly secrets set GEMINI_API_KEY=your_key
   ```

---

## 로컬 테스트

배포 전 로컬에서 테스트:

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정 (선택사항)
export OPENDART_API_KEY=your_key
export GEMINI_API_KEY=your_key

# 개발 서버 실행
python app.py

# 또는 gunicorn으로 실행 (프로덕션 모드)
gunicorn app:app --bind 0.0.0.0:5001
```

---

## 환경 변수

다음 환경 변수를 설정해야 합니다:

- `OPENDART_API_KEY`: 오픈다트 API 키
- `GEMINI_API_KEY`: Gemini API 키
- `PORT`: 포트 번호 (대부분의 플랫폼에서 자동 설정)
- `FLASK_DEBUG`: 디버그 모드 (프로덕션에서는 False)

---

## 주의사항

1. **API 키 보안**: 절대 코드에 API 키를 하드코딩하지 마세요. 환경 변수를 사용하세요.
2. **corp.xml 파일**: 이 파일은 약 27,000줄이므로 Git에 포함해도 되지만, 대용량 파일일 수 있습니다.
3. **포트**: 대부분의 플랫폼에서 `PORT` 환경 변수를 자동으로 설정합니다.
4. **타임아웃**: AI 분석은 시간이 걸릴 수 있으므로, 플랫폼의 타임아웃 설정을 확인하세요.

---

## 문제 해결

### 모듈을 찾을 수 없음
- `requirements.txt`에 모든 의존성이 포함되어 있는지 확인
- 가상 환경이 활성화되어 있는지 확인

### 포트 오류
- 플랫폼에서 제공하는 `PORT` 환경 변수 사용
- `app.py`에서 `os.getenv('PORT')` 사용 확인

### API 키 오류
- 환경 변수가 올바르게 설정되었는지 확인
- 플랫폼의 환경 변수 설정 페이지에서 확인

---

## 추천 배포 플랫폼

**초보자**: Render 또는 Railway (가장 쉬움)
**무료 플랜**: PythonAnywhere 또는 Fly.io
**프로덕션**: Render, Railway, 또는 AWS/GCP

