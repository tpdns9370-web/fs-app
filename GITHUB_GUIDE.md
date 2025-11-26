# GitHub 사용 가이드 (비개발자용)

이 가이드는 GitHub를 처음 사용하는 분들을 위한 단계별 설명입니다.

## 1단계: GitHub 계정 만들기

1. 웹 브라우저에서 [github.com](https://github.com) 접속
2. 오른쪽 위 "Sign up" 클릭
3. 이메일 주소, 비밀번호 입력
4. 사용자 이름 선택 (예: sewoonkim)
5. 이메일 인증 완료

✅ **완료!** 이제 GitHub 계정이 있습니다.

---

## 2단계: GitHub Desktop 설치 (가장 쉬운 방법)

### Windows/Mac용 GitHub Desktop

1. [desktop.github.com](https://desktop.github.com) 접속
2. "Download for Windows" 또는 "Download for Mac" 클릭
3. 다운로드한 파일 실행하여 설치
4. 설치 후 GitHub Desktop 실행
5. GitHub 계정으로 로그인

**왜 GitHub Desktop을 사용하나요?**
- 명령어를 몰라도 사용 가능
- 버튼 클릭만으로 업로드 가능
- 시각적으로 이해하기 쉬움

---

## 3단계: 프로젝트를 GitHub에 올리기

### 방법 A: GitHub Desktop 사용 (추천)

#### 3-1. 저장소 만들기

1. GitHub Desktop 실행
2. 왼쪽 위 "File" → "New Repository" 클릭
3. 설정 입력:
   - **Name**: `fs-project2` (또는 원하는 이름)
   - **Description**: "오픈다트 재무데이터 분석 서비스" (선택사항)
   - **Local Path**: 현재 프로젝트 폴더 경로 선택
     - 예: `/Users/sewoonkim/Desktop/Vibe Coding/fs-project2`
   - **Initialize this repository with a README**: ✅ 체크 해제 (이미 파일이 있으므로)
4. "Create Repository" 클릭

#### 3-2. 파일 추가 및 업로드

1. GitHub Desktop에서 변경된 파일들이 보입니다
2. 왼쪽 하단 "Summary"에 메시지 입력:
   - 예: "첫 번째 업로드" 또는 "Initial commit"
3. 왼쪽 하단 "Commit to main" 버튼 클릭
4. 오른쪽 위 "Publish repository" 버튼 클릭
5. 설정:
   - **Keep this code private**: 원하면 체크 (비공개)
   - **Organization**: 그대로 두기
6. "Publish repository" 클릭

✅ **완료!** 이제 GitHub에 코드가 올라갔습니다!

---

### 방법 B: 웹사이트에서 직접 만들기 (GitHub Desktop 없이)

#### 3-1. GitHub 웹사이트에서 저장소 만들기

1. [github.com](https://github.com) 로그인
2. 오른쪽 위 "+" 아이콘 → "New repository" 클릭
3. 설정 입력:
   - **Repository name**: `fs-project2`
   - **Description**: "오픈다트 재무데이터 분석 서비스"
   - **Public** 또는 **Private** 선택
   - **Initialize this repository with a README**: ✅ 체크 해제
4. "Create repository" 클릭

#### 3-2. 파일 업로드

1. 생성된 저장소 페이지에서 "uploading an existing file" 클릭
2. 프로젝트 폴더의 모든 파일을 드래그 앤 드롭:
   - `app.py`
   - `corp_parser.py`
   - `opendart_api.py`
   - `gemini_analyzer.py`
   - `corp.xml`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `templates` 폴더 (안에 파일들 포함)
   - 기타 모든 파일
3. 아래로 스크롤하여 "Commit changes" 클릭

✅ **완료!** 파일이 업로드되었습니다!

---

## 4단계: 배포하기 (Render 사용)

### 4-1. Render 계정 만들기

1. [render.com](https://render.com) 접속
2. "Get Started for Free" 클릭
3. "Sign up with GitHub" 클릭 (GitHub 계정으로 가입)
4. GitHub 계정 권한 허용

### 4-2. 웹 서비스 만들기

1. Render 대시보드에서 "New +" 버튼 클릭
2. "Web Service" 선택
3. "Connect account" 또는 "Connect GitHub" 클릭
4. 방금 만든 저장소(`fs-project2`) 선택
5. 설정 입력:
   - **Name**: `opendart-financial` (원하는 이름)
   - **Region**: `Singapore` (한국과 가까움) 또는 `Oregon`
   - **Branch**: `main`
   - **Root Directory**: (비워두기)
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```
     gunicorn app:app
     ```
6. "Advanced" 클릭하여 환경 변수 추가:
   - **Key**: `OPENDART_API_KEY`
     **Value**: (오픈다트에서 발급받은 API 키 입력)
   - **Key**: `GEMINI_API_KEY`
     **Value**: (Google AI Studio에서 발급받은 API 키 입력)
7. "Create Web Service" 클릭

### 4-3. 배포 대기

1. 배포가 시작됩니다 (약 2-5분 소요)
2. "Logs" 탭에서 진행 상황 확인 가능
3. "Events" 탭에서 배포 상태 확인
4. 배포 완료되면 초록색 "Live" 표시가 나타남

✅ **완료!** 이제 웹사이트가 인터넷에 공개되었습니다!

---

## 5단계: 웹사이트 확인하기

1. Render 대시보드에서 서비스 이름 클릭
2. 상단에 URL이 표시됩니다 (예: `https://opendart-financial.onrender.com`)
3. 이 URL을 클릭하거나 복사하여 브라우저에서 열기
4. 웹사이트가 정상 작동하는지 확인!

---

## 문제 해결

### Q: GitHub Desktop에서 파일이 안 보여요
**A**: 프로젝트 폴더를 올바르게 선택했는지 확인하세요.

### Q: Render에서 배포가 실패해요
**A**: 
1. "Logs" 탭에서 오류 메시지 확인
2. 환경 변수가 올바르게 설정되었는지 확인
3. `requirements.txt`에 모든 패키지가 있는지 확인

### Q: 웹사이트가 열리지 않아요
**A**:
1. Render에서 서비스가 "Live" 상태인지 확인
2. 배포가 완료될 때까지 기다리기 (처음 배포는 5-10분 걸릴 수 있음)
3. 브라우저 캐시 삭제 후 다시 시도

### Q: 코드를 수정했어요. 어떻게 업데이트하나요?
**A** (GitHub Desktop 사용 시):
1. GitHub Desktop에서 변경된 파일 확인
2. "Summary"에 변경 내용 입력 (예: "버그 수정")
3. "Commit to main" 클릭
4. "Push origin" 클릭
5. Render에서 자동으로 재배포됩니다!

---

## 용어 설명

- **Repository (저장소)**: 프로젝트 폴더를 GitHub에 올린 것
- **Commit (커밋)**: 변경사항을 저장하는 것
- **Push (푸시)**: 로컬 변경사항을 GitHub에 업로드하는 것
- **Deploy (배포)**: 코드를 웹사이트로 만드는 것

---

## 다음 단계

배포가 완료되면:
1. 친구들에게 URL 공유하기
2. 모바일에서도 접속해보기
3. 필요하면 코드 수정 후 다시 업로드하기

---

## 도움이 필요하신가요?

- GitHub 공식 문서: [docs.github.com](https://docs.github.com)
- Render 문서: [render.com/docs](https://render.com/docs)
- 문제가 있으면 GitHub에 이슈를 등록하세요!

