#!/bin/bash
# GitHub 업로드 스크립트

echo "=========================================="
echo "GitHub 업로드 준비"
echo "=========================================="
echo ""
echo "Personal Access Token을 입력해주세요."
echo "(입력한 토큰은 이 스크립트 실행에만 사용됩니다)"
echo ""
read -s TOKEN

if [ -z "$TOKEN" ]; then
    echo "❌ 토큰이 입력되지 않았습니다."
    exit 1
fi

echo ""
echo "업로드 중..."

# 원격 저장소 URL에 토큰 포함
git remote set-url origin https://${TOKEN}@github.com/tpdns9370-web/fs-app.git

# 푸시 실행
git push -u origin main

# 보안을 위해 원격 URL에서 토큰 제거
git remote set-url origin https://github.com/tpdns9370-web/fs-app.git

echo ""
echo "✅ 완료!"

