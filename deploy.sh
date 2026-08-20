#!/bin/bash
set -e

MSG="${1:-Update blog $(date '+%Y-%m-%d %H:%M')}"
ROOT_DIR="$(git rev-parse --show-toplevel)"
cd "$ROOT_DIR"

if [[ -n $(git -C public status --porcelain) ]]; then
    echo "public 子模块存在未提交更改，请先处理后再部署。"
    exit 1
fi
git -C public checkout main 2>/dev/null

git add -A -- . ':(exclude)public'
if ! git diff --cached --quiet; then
    git commit -m "$MSG"
    echo "源码已提交"
fi

echo "构建中..."
hugo

if [[ -n $(git -C public status --porcelain) ]]; then
    git -C public add -A
    git -C public commit -m "$MSG"
    git -C public push origin main
    echo "Pages 已更新"
fi

git add public
if ! git diff --cached --quiet; then
    git commit -m "chore: 同步发布产物"
fi
git push origin main

echo "完成"
