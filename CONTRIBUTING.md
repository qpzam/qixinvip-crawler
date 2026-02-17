# 贡献指南

感谢你考虑为启信宝 VIP 爬虫项目做贡献！

## 如何贡献

### 报告问题

如果你发现了 bug 或者有功能建议：

1. 检查 [Issues](../../issues) 是否已有类似问题
2. 如果没有，创建新的 Issue
3. 提供详细的信息：
   - 问题描述
   - 复现步骤
   - 期望行为
   - 实际行为
   - 环境信息（Python 版本、操作系统等）
   - 日志或截图

### 提交代码

1. **Fork 本仓库**
2. **创建你的特性分支** (`git checkout -b feature/AmazingFeature`)
3. **提交你的修改** (`git commit -m 'Add some AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **开启 Pull Request**

### 代码规范

- 遵循 PEP 8 规范
- 添加必要的注释
- 更新相关文档
- 测试你的修改

### 提交信息格式

使用清晰的提交信息：

```
<type>: <subject>

<body>

<footer>
```

**类型 (type)**:
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具链相关

**示例**:
```
feat: 添加股东信息提取功能

- 实现点击"股东信息"标签
- 提取股东列表数据
- 处理分页情况

Closes #123
```

## 开发设置

### 环境准备

```bash
# 克隆仓库
git clone https://github.com/your-username/qixinvip-crawler.git
cd qixinvip-crawler

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
playwright install chromium
```

### 运行测试

```bash
# 运行诊断测试
python test.py

# 运行单公司测试
python test_single.py
```

### 代码风格

- 使用 4 空格缩进
- 每行最大长度 120
- 函数之间空 2 行
- 类之间空 3 行

## 文档贡献

文档同样重要！你可以：

- 修正错别字
- 改进说明清晰度
- 添加使用示例
- 翻译文档

## 版本发布

版本遵循 [语义化版本](https://semver.org/lang/zh-CN/)：

- **主版本号**: 重大功能变更或不兼容修改
- **次版本号**: 新功能向后兼容
- **修订号**: 向后兼容的问题修复

## 行为准则

- 尊重他人
- 欢迎新手
- 建设性反馈
- 专注于项目

## 获取帮助

- 查看 [README.md](README.md)
- 查看 [QUICKSTART.md](QUICKSTART.md)
- 提交 [Issue](../../issues)

---

**感谢你的贡献！** 🙏
