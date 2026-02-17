# GitHub 发布指南

## 📋 发布前检查清单

- [x] 代码已完成
- [x] 测试通过
- [x] 文档完善
- [x] 版本号已更新
- [ ] .gitignore 已配置
- [ ] LICENSE 已添加
- [ ] README.md 已完善

---

## 🚀 发布步骤（完整版）

### 第一步：准备本地仓库

```bash
# 进入项目目录
cd C:\Users\Lenovo\.claude\skills\qixinvip-crawler

# 检查是否已有 Git 仓库
git status

# 如果没有，初始化
git init
```

### 第二步：创建 .gitignore（已完成✅）

项目已包含完整的 .gitignore 文件，会自动忽略：
- 配置文件（config.json, cookie.txt）
- 输出文件（*.xlsx, *.csv）
- Python 缓存（__pycache__/）
- 虚拟环境（venv/）
- 调试截图（*.png）

### 第三步：添加文件到 Git

```bash
# 添加所有文件
git add .

# 查看状态
git status

# 如果需要移除敏感文件
git rm --cached config.json cookie.txt 2>/dev/null || true
```

### 第四步：创建首次提交

```bash
git commit -m "feat: 初始化 v1.0.0 版本

- 实现启信宝企业信息爬取
- 支持 VIP 权限利用
- 成功提取 12/14 字段（85.7%）
- 支持 Excel/CSV 导出
- 完整文档和测试脚本

详情见 v1.0.0_README.md"
```

### 第五步：创建 GitHub 仓库

#### 方式 A：通过网页创建（推荐）

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `qixinvip-crawler`
   - **Description**: `专业的启信宝企业信息爬取工具，基于 Playwright 实现`
   - **Public/Private**: 选择 Public
   - **⚠️ 不要**勾选 "Add a README file"（我们已有）
   - **⚠️ 不要**勾选 "Add .gitignore"（我们已有）
   - **⚠️ 不要**选择 "Choose a license"（我们已有）
3. 点击 "Create repository"

#### 方式 B：通过 GitHub CLI（gh）

```bash
# 如果安装了 gh CLI
gh repo create qixinvip-crawler --public --description "专业的启信宝企业信息爬取工具" --source=. --remote=origin --push
```

### 第六步：连接远程仓库并推送

```bash
# 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/qixinvip-crawler.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 第七步：创建 GitHub Release（可选）

1. 访问你的仓库页面
2. 点击右侧 "Releases"
3. 点击 "Create a new release"
4. 填写信息：
   - **Tag version**: `v1.0.0`
   - **Target**: `main`
   - **Title**: `v1.0.0 - 首个稳定版本`
   - **Description**: 复制 `v1.0.0_README.md` 的内容
5. 勾选 "Set as the latest release"
6. 点击 "Publish release"

---

## 🎯 快速发布命令（一键复制）

```bash
# 完整命令序列（复制粘贴到终端）
cd C:\Users\Lenovo\.claude\skills\qixinvip-crawler
git init
git add .
git commit -m "feat: 初始化 v1.0.0 版本 - 启信宝企业信息爬虫"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/qixinvip-crawler.git
git push -u origin main
```

**⚠️ 重要**: 将 `YOUR_USERNAME` 替换为你的 GitHub 用户名！

---

## 📝 发布后检查清单

### 仓库设置

- [ ] 仓库描述已添加
- [ ] 仓库主页已设置（如果需要）
- [ ] Topics 已添加（web-scraping, crawler, automation）
- [ ] License 已显示（MIT）

### Release 检查

- [ ] Release 已创建
- [ ] 说明文档完整
- [ ] 版本号正确
- [ ] 附件（如果有）

### 文档检查

- [ ] README.md 显示正常
- [ ] 所有文档链接有效
- [ ] 代码示例可以运行

---

## 🔧 常见问题

### Q1: 推送失败，提示 "Permission denied"

**原因**: 用户名或密码错误

**解决**:
1. 检查用户名是否正确
2. 使用 Personal Access Token 而非密码
3. 生成 Token: Settings → Developer settings → Personal access tokens

### Q2: .gitignore 不生效

**原因**: 文件已被 git 跟踪

**解决**:
```bash
# 先清除缓存
git rm -r --cached .
git add .
git commit -m "fix: 应用 .gitignore"
git push
```

### Q3: 文件太大，推送失败

**原因**: GitHub 限制单文件 < 100MB

**解决**:
- 检查是否有大文件在 .gitignore 中
- 使用 Git LFS（如果需要）

---

## 📊 发布统计

发布后可以在 GitHub 查看：

- **Stars**: 收藏数
- **Forks**: 分叉数
- **Issues**: 问题反馈
- **Clones**: 访问统计（Settings → Insights）

---

## 🎉 发布完成！

发布成功后，你的项目地址是：

```
https://github.com/YOUR_USERNAME/qixinvip-crawler
```

**下一步**:
1. 分享到社交媒体
2. 添加到作品集
3. 邀请他人 Star
4. 开始 v1.1.0 开发

---

**需要帮助？**
- GitHub 文档: https://docs.github.com
- Git 文档: https://git-scm.com/docs
