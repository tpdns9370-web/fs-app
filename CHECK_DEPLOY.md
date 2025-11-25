# 배포 상태 확인 가이드

## Render 자동 배포 확인 방법

### 1단계: Render 대시보드 확인

1. [render.com](https://render.com) 접속 및 로그인
2. 대시보드에서 `fs-app` 또는 배포한 서비스 이름 클릭
3. 확인할 항목들:

#### ✅ 자동 배포 활성화 확인
- "Settings" 탭 클릭
- "Auto-Deploy" 섹션 확인
- "Yes"로 설정되어 있으면 자동 배포 활성화됨

#### ✅ 최근 배포 확인
- "Events" 또는 "Logs" 탭 확인
- 최근 배포 시간 확인
- GitHub 푸시 시간과 비교

#### ✅ 배포 상태 확인
- 상단에 "Live" 또는 "Building" 표시 확인
- "Live" = 정상 작동 중
- "Building" = 배포 진행 중

---

## 자동 배포가 안 되는 경우

### 문제 1: Auto-Deploy가 비활성화됨
**해결 방법:**
1. Render 대시보드 → 서비스 선택
2. "Settings" 탭
3. "Auto-Deploy" → "Yes"로 변경
4. "Save Changes" 클릭

### 문제 2: GitHub 연결이 끊어짐
**해결 방법:**
1. Render 대시보드 → 서비스 선택
2. "Settings" 탭
3. "Repository" 섹션 확인
4. 필요시 "Disconnect" 후 다시 연결

### 문제 3: 수동 배포 필요
**해결 방법:**
1. Render 대시보드 → 서비스 선택
2. "Manual Deploy" 클릭
3. "Deploy latest commit" 선택

---

## 배포 확인 체크리스트

- [ ] Render에 서비스가 생성되어 있는가?
- [ ] GitHub 저장소가 연결되어 있는가?
- [ ] Auto-Deploy가 활성화되어 있는가?
- [ ] 최근 배포 시간이 GitHub 푸시 시간 이후인가?
- [ ] 서비스 상태가 "Live"인가?

---

## 수동으로 재배포하기

자동 배포가 안 되면 수동으로 재배포할 수 있습니다:

1. Render 대시보드 접속
2. 서비스 선택
3. "Manual Deploy" → "Deploy latest commit" 클릭
4. 배포 완료 대기 (2-5분)

---

## 최신 코드 확인

GitHub에 최신 코드가 있는지 확인:
- https://github.com/tpdns9370-web/fs-app

최근 커밋에 다음이 포함되어 있는지 확인:
- 재무상태표 박스 시각화 추가
- 배포 가이드 파일들

