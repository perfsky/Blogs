#!/bin/bash
set -e

# 生成静态网站
echo "构建中..."
hugo

# 获取提交信息
MSG="${1:-Update blog $(date '+%Y-%m-%d %H:%M')}"

# 发布到 GitHub Pages
cd public
git checkout main 2>/dev/null || true
if [[ -n $(git status -s) ]]; then
    git add .
    git commit -m "$MSG"
    git push origin main
    echo "Pages 已更新"
fi
cd ..

# 提交源码
if [[ -n $(git status -s) ]]; then
    git add .
    git commit -m "$MSG"
    git push origin main
    echo "源码已提交"
fi

echo "完成"
