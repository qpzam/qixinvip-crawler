# 快速开始指南

## 📦 5 分钟快速上手

### 第 1 步：安装依赖（首次使用）

**Windows:**
```bash
# 双击运行 start.bat
# 或在命令行执行：
pip install -r requirements.txt
playwright install chromium
```

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

### 第 2 步：配置 Cookie

#### 2.1 获取 Cookie

1. 在浏览器中打开 [启信宝](https://www.qixin.com/) 并登录 VIP 账号
2. 按 `F12` 打开开发者工具
3. 切换到 `Network` 标签
4. 刷新页面（`F5`）
5. 点击第一个请求（通常是文档请求）
6. 在右侧找到 `Request Headers`
7. 找到 `Cookie:` 这一栏
8. 复制 `Cookie:` 后面的所有内容

#### 2.2 配置到项目中

编辑 `config.json`，将 Cookie 粘贴进去：

```json
{
  "cookie": "你复制的Cookie字符串"
}
```

### 第 3 步：运行测试

```bash
python test.py
```

选择测试项目，验证配置是否正确。

### 第 4 步：开始爬取

```bash
python main.py
```

选择模式：
- **模式 1**：单公司测试（推荐首次使用）
- **模式 2**：批量爬取
- **模式 3**：交互式模式

## 🎯 示例用法

### 示例 1：爬取单个公司

```bash
python main.py
# 选择 1
# 输入公司名：腾讯科技（深圳）有限公司
# 等待完成...
# 查看输出的 Excel 文件
```

### 示例 2：批量爬取（从文本文件）

创建 `my_companies.txt`：
```
腾讯科技（深圳）有限公司
阿里巴巴（中国）有限公司
百度在线网络技术（北京）有限公司
```

运行：
```bash
python main.py
# 选择 2
# 选择 3（从文本文件读取）
# 输入文件路径：my_companies.txt
# 等待完成...
```

### 示例 3：批量爬取（从 Excel）

创建 `companies.xlsx`：

| 公司名称 |
|---------|
| 腾讯科技（深圳）有限公司 |
| 阿里巴巴（中国）有限公司 |

运行：
```bash
python main.py
# 选择 2
# 选择 1（从 Excel 读取）
# 输入文件路径：companies.xlsx
# 输入工作表：Sheet1
# 输入列名：公司名称
```

## ⚙️ 常用配置调整

### 调整延迟（速度 vs 安全性）

编辑 `config.json`：

```json
{
  "delays": {
    "min": 1.0,    // 最小延迟（秒）
    "max": 3.0     // 最大延迟（秒）
  }
}
```

- **快速爬取**：`min: 0.5, max: 1.5` （风险较高）
- **安全爬取**：`min: 3.0, max: 6.0` （推荐）
- **极慢爬取**：`min: 5.0, max: 10.0` （最安全）

### 无头模式（不显示浏览器）

```json
{
  "browser": {
    "headless": true   // true=不显示，false=显示
  }
}
```

### 修改输出格式

```json
{
  "output": {
    "format": "excel",  // 或 "csv"
    "filename": "my_results",
    "timestamp": true
  }
}
```

## 🐛 常见问题解决

### 问题 1：提示"Cookie 未配置"

**解决：**
1. 检查 `config.json` 是否存在
2. 确保 Cookie 字段不是 `your_cookie_string_here`
3. 重新获取 Cookie（可能已过期）

### 问题 2：提示"联系方式需要 VIP"

**解决：**
1. 确认你的账号是 VIP 状态
2. 重新登录启信宝并获取新的 Cookie
3. 检查 Cookie 是否完整复制

### 问题 3：找不到搜索框/结果

**原因：** 网站结构变化，选择器失效

**解决：**
1. 运行 `python test.py`
2. 选择"选择器验证"
3. 手动查找新的选择器
4. 更新 `crawler.py` 中的选择器

### 问题 4：爬取速度很慢

**说明：** 这是正常的，为了避免被检测

**如需加速：**
1. 降低 `delays` 的值（不推荐）
2. 使用更快的网络
3. 使用性能更好的电脑

### 问题 5：浏览器启动失败

**解决：**
```bash
# 重新安装 Playwright 浏览器
playwright install chromium
```

## 📊 输出文件

爬取完成后，会在项目目录生成 Excel 文件：

```
qixinbao_companies_20240101_120000.xlsx
```

包含的字段：
- 公司名称
- 法定代表人
- 注册资本
- 成立日期
- 经营状态
- 联系电话
- 企业邮箱
- 注册地址
- 股东信息
- 主要人员
- 爬取时间

## 🔒 安全建议

1. **不要分享你的 Cookie** - 这相当于你的账号密码
2. **定期更换 Cookie** - Cookie 会过期
3. **使用虚拟环境** - 隔离项目依赖
4. **合理设置延迟** - 避免被封禁
5. **遵守服务条款** - 仅用于个人学习研究

## 📞 获取帮助

遇到问题？

1. 查看 `README.md` 详细文档
2. 运行 `python test.py` 诊断问题
3. 检查日志输出
4. 提交 Issue

## 🎓 下一步

- ✅ 完成首次测试
- ✅ 爬取几个测试公司
- ✅ 根据需要调整配置
- ✅ 尝试批量爬取
- ✅ 学习如何添加自定义字段

---

**祝你使用愉快！** 🎉
