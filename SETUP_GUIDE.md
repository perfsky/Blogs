# Mac 环境配置指南

本指南帮助你在 Mac 上配置和使用 Sakuya's Blog。

## 前置要求

- macOS 系统
- Homebrew 包管理器
- Git

## 一、环境配置

### 1. 安装 Hugo（如果未安装）

```bash
# 使用 Homebrew 安装 Hugo Extended 版本
brew install hugo
```

### 2. 克隆仓库并初始化子模块

如果是第一次克隆仓库：

```bash
# 方式一：克隆时直接包含子模块
git clone --recurse-submodules https://github.com/perfsky/Blogs.git

# 方式二：先克隆再初始化子模块
git clone https://github.com/perfsky/Blogs.git
cd Blogs
git submodule init
git submodule update
```

### 3. 验证安装

```bash
hugo version  # 应该显示 extended 版本
git submodule status  # 检查子模块状态
```

## 二、日常工作流程

### 创建新文章

```bash
# 博客类文章
hugo new content/myblog/文章标题.md

# CTF writeup
hugo new content/matches/比赛名称-题目.md

# 技术杂项
hugo new content/misc/文章标题.md
```

### 本地预览

```bash
# 启动开发服务器（包含草稿）
hugo server -D

# 或者不包含草稿
hugo server

# 访问 http://localhost:1313
# 支持热重载，保存文件后自动刷新
```

### 发布文章

1. **编辑文章 Front Matter**，将 `draft: true` 改为 `draft: false`

2. **生成静态网站**：
```bash
hugo
```

3. **发布到 GitHub Pages**：
```bash
# 进入 public 目录（这是一个独立的 git 仓库）
cd public

# 提交更改
git add .
git commit -m "Update: 新文章标题"
git push origin main

# 返回主目录
cd ..
```

4. **提交源码**：
```bash
# 在主仓库提交源文件
git add .
git commit -m "Add post: 新文章标题"
git push origin main
```

## 三、子模块管理

### 更新主题

```bash
# 更新 hextra 主题到最新版本
cd themes/hextra
git pull origin main
cd ../..

# 提交子模块更新
git add themes/hextra
git commit -m "Update hextra theme"
git push
```

### 查看子模块状态

```bash
git submodule status
```

### 重新初始化子模块（如果遇到问题）

```bash
git submodule deinit -f .
git submodule update --init --recursive
```

## 四、常见问题

### 1. 子模块未初始化

**症状**：`themes/hextra` 目录为空

**解决**：
```bash
git submodule update --init --recursive
```

### 2. Hugo 命令找不到

**症状**：`command not found: hugo`

**解决**：
```bash
# 安装 Hugo
brew install hugo

# 或者重新安装
brew reinstall hugo
```

### 3. public 目录冲突

**症状**：无法推送到 perfsky.github.io

**解决**：
```bash
cd public
git status
git pull --rebase origin main
git push origin main
```

### 4. 主题样式不生效

**症状**：网站样式异常

**解决**：
```bash
# 清除缓存
hugo mod clean
rm -rf public resources

# 重新生成
hugo
```

## 五、快速命令参考

```bash
# 本地预览
hugo server -D

# 生成网站
hugo

# 查看帮助
hugo help

# 创建新内容
hugo new content/<section>/<filename>.md

# 检查配置
hugo config

# 更新依赖
git submodule update --remote --merge
```

## 六、目录结构说明

```
Blogs/
├── archetypes/          # 内容模板
├── assets/             # 资源文件（CSS、JS等）
├── content/            # 文章内容
│   ├── myblog/        # 个人博客
│   ├── matches/       # CTF writeups
│   └── misc/          # 技术杂项
├── layouts/           # 自定义布局
├── public/            # 生成的静态网站（独立仓库）
├── resources/         # Hugo 生成的资源缓存
├── themes/hextra/     # Hextra 主题（子模块）
└── hugo.yaml          # Hugo 配置文件
```

## 七、推荐的开发流程

1. 启动开发服务器：`hugo server -D`
2. 在 VS Code 中编辑 Markdown 文件
3. 浏览器自动刷新预览效果
4. 满意后设置 `draft: false`
5. 运行 `hugo` 生成静态文件
6. 分别提交 public 和主仓库

## 八、一键发布脚本（可选）

创建 `deploy.sh`：

```bash
#!/bin/bash

echo "生成静态网站..."
hugo

echo "发布到 GitHub Pages..."
cd public
git add .
git commit -m "Rebuild site $(date)"
git push origin main
cd ..

echo "提交源码..."
git add .
read -p "输入提交信息: " msg
git commit -m "$msg"
git push origin main

echo "✅ 发布完成！"
```

使用方法：
```bash
chmod +x deploy.sh
./deploy.sh
```

---

**提示**：编辑文章时，VS Code 可以安装 Markdown 相关扩展以获得更好的编辑体验。
