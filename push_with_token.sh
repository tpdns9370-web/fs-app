#!/bin/bash

echo "=========================================="
echo "GitHub 업로드 시작"
echo "=========================================="
echo ""
echo "생성하신 Personal Access Token을 입력해주세요:"
read -s TOKEN

if [ -z "$TOKEN" ]; then
    echo "❌ 토큰이 입력되지 않았습니다."
    exit 1
fi

echo ""
echo "📤 업로드 중..."

# 원격 저장소 URL에 토큰 포함하여 설정
git remote set-url origin https://${TOKEN}@github.com/tpdns9370-web/fs-app.git

# 푸시 실행
if git push -u origin main; then
    echo ""
    echo "✅ 업로드 완료!"
    echo ""
    echo "저장소 주소: https://github.com/tpdns9370-web/fs-app"
else
    echo ""
    echo "❌ 업로드 실패. 오류를 확인해주세요."
fi

# 보안을 위해 원격 URL에서 토큰 제거
git remote set-url origin https://github.com/tpdns9370-web/fs-app.git

echo ""
echo "완료되었습니다!"

