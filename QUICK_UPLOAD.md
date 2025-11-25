# 빠른 업로드 가이드

## ✅ 이미 완료된 작업
- Git 저장소 초기화 완료
- GitHub 저장소 연결 완료 (https://github.com/tpdns9370-web/fs-app.git)
- 파일 커밋 완료

## 이제 해야 할 일: GitHub에 업로드하기

### 방법 1: GitHub Desktop 사용 (가장 쉬움) ⭐

1. **GitHub Desktop 다운로드** (아직 안 했다면)
   - https://desktop.github.com 접속
   - 다운로드 및 설치

2. **GitHub Desktop에서 저장소 열기**
   - GitHub Desktop 실행
   - File → Add Local Repository 클릭
   - 다음 경로 선택:
     ```
     /Users/sewoonkim/Desktop/Vibe Coding/fs-project2
     ```
   - "Add Repository" 클릭

3. **업로드하기**
   - GitHub Desktop에서 변경사항이 보입니다
   - 오른쪽 위 "Publish branch" 또는 "Push origin" 버튼 클릭
   - GitHub 계정 로그인 (처음만)
   - 완료!

---

### 방법 2: Personal Access Token 사용 (명령어)

1. **Personal Access Token 만들기**
   - GitHub.com 로그인
   - 오른쪽 위 프로필 → Settings 클릭
   - 왼쪽 메뉴에서 "Developer settings" 클릭
   - "Personal access tokens" → "Tokens (classic)" 클릭
   - "Generate new token" → "Generate new token (classic)" 클릭
   - Note: `fs-app-upload` 입력
   - Expiration: 원하는 기간 선택 (예: 90 days)
   - Scopes: `repo` 체크
   - "Generate token" 클릭
   - **토큰 복사** (한 번만 보여줌!)

2. **터미널에서 실행**
   ```bash
   cd "/Users/sewoonkim/Desktop/Vibe Coding/fs-project2"
   git push -u origin main
   ```
   - Username: `tpdns9370-web` 입력
   - Password: 방금 복사한 토큰 붙여넣기

---

### 방법 3: 웹사이트에서 직접 업로드

1. https://github.com/tpdns9370-web/fs-app 접속
2. "uploading an existing file" 클릭
3. 프로젝트 폴더의 모든 파일 드래그 앤 드롭
4. "Commit changes" 클릭

---

## 추천: 방법 1 (GitHub Desktop)

가장 쉽고 안전합니다!

