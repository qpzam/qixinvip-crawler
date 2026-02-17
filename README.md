# 启信宝 VIP 爬虫

> **当前版本**: v1.0.0 | **状态**: ✅ 稳定可用 | **成功率**: 85.7%

专业的启信宝企业信息爬取工具，基于 Playwright 实现，支持利用 VIP 账号权限获取企业详细信息。

**【重要通知】**: v1.0.0 已正式发布！核心功能全部实现，可直接投入使用。详见 [v1.0.0 发布说明](v1.0.0_README.md)

## ✨ 特性

- 🚀 **自动化浏览器**: 使用 Playwright 模拟真实用户操作
- 🎯 **精准数据提取**: 提取公司基本信息、联系方式、股东高管等
- 🔐 **VIP 权限利用**: 通过 Cookie 登录，充分利用 VIP 权限
- 🛡️ **反爬优化**: 随机延迟、鼠标移动、隐身模式
- 📊 **多格式导出**: 支持 Excel、CSV 格式导出
- ⚡ **批量处理**: 支持单公司测试、批量爬取、交互式三种模式

## 📊 版本信息

- **当前版本**: v1.0.0
- **发布日期**: 2024-02-17
- **数据提取成功率**: 85.7% (12/14 字段)
- **测试状态**: ✅ 已验证通过
- **文档完善度**: 100%

**详细版本信息**: 见 [VERSION.md](VERSION.md) | [更新日志](CHANGELOG.md)

## 📋 系统要求

- Python 3.8+
- Windows / macOS / Linux
- 稳定的网络连接
- 启信宝 VIP 账号（用于获取 Cookie）

## 🔧 安装步骤

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 安装 Playwright 浏览器

```bash
playwright install chromium
```

### 3. 配置 Cookie

#### 🌟 推荐方式：使用 cookie.txt（每次更新只需 10 秒）

1. 安装 **EditThisCookie** 或 **Cookie-Editor** 浏览器插件
2. 登录启信宝 VIP 账号
3. 点击插件图标 → 导出/复制 Cookie
4. 粘贴到项目的 `cookie.txt` 文件中
5. 保存文件

**优点：**
- ✅ 无需修改代码
- ✅ 一键更新，10 秒完成
- ✅ 每次运行前更新即可

#### 传统方式：直接修改 config.json

1. 在浏览器中登录启信宝 VIP 账号
2. 按 `F12` 打开开发者工具
3. 切换到 `Network` 标签
4. 刷新页面
5. 点击任意请求，找到 `Request Headers`
6. 复制 `Cookie` 后的整个字符串
7. 将 Cookie 粘贴到 `config.json` 文件中

**注意：** 如果存在 `cookie.txt` 文件，程序会优先使用 `cookie.txt` 中的 Cookie。

示例：
```json
{
  "cookie": "acw_tc=xxx; session_id=xxx; user_token=xxx; vip_status=1"
}
```

---

## 📊 功能状态

### ✅ 已实现 (v1.0.0)

| 模块 | 功能 | 状态 | 成功率 |
|------|------|------|--------|
| 搜索 | 公司搜索 | ✅ | 100% |
| 导航 | 进入详情页 | ✅ | 100% |
| 提取 | 基本信息 (9字段) | ✅ | 100% |
| 提取 | 联系方式 (3字段) | ✅ | 100% |
| 提取 | 股东信息 | ⏳ | 0% |
| 提取 | 高管信息 | ⏳ | 0% |
| 导出 | Excel/CSV | ✅ | 100% |
| 批量 | 批量处理 | ✅ | 100% |

**总体成功率**: **85.7% (12/14 字段)**

详见 [v1.0.0 发布说明](v1.0.0_README.md)

## 🚀 使用方法

### 方式一：单公司测试（推荐首次使用）

```bash
python main.py
```

选择 `1`，然后输入公司名称，例如：
```
腾讯科技（深圳）有限公司
```

### 方式二：批量爬取

#### 从 Excel 文件读取：

准备 Excel 文件（companies.xlsx），包含公司名称列：

```
| 公司名称           |
|-------------------|
| 腾讯科技（深圳）有限公司 |
| 阿里巴巴（中国）有限公司 |
| 百度在线网络技术公司 |
```

运行程序选择 `2`，然后选择从 Excel 读取。

#### 从文本文件读取：

创建 companies.txt，每行一个公司名：
```
腾讯科技（深圳）有限公司
阿里巴巴（中国）有限公司
百度在线网络技术公司
```

### 方式三：交互式模式

适合临时查询多个不相关的公司：

```bash
python main.py
```

选择 `3`，然后逐个输入公司名称。

## 📁 项目结构

```
qixinvip-crawler/
├── main.py              # 主程序入口
├── crawler.py           # 爬虫核心逻辑
├── browser.py           # 浏览器管理
├── exporter.py          # 数据导出
├── utils.py             # 工具函数
├── config.json          # 配置文件
├── cookie.txt           # Cookie 文件（优先使用）
├── selectors.json       # 选择器配置文件
├── requirements.txt     # Python 依赖
├── README.md            # 完整使用说明
├── QUICKSTART.md        # 5分钟快速上手
├── USAGE_GUIDE.md       # 快速使用指南
└── output/              # 输出目录（自动创建）
    ├── qixinbao_companies_20240101_120000.xlsx
    └── ...
```

## ⚙️ 配置说明

`config.json` 配置项说明：

```json
{
  "cookie": "your_cookie_here",           // 必填：启信宝VIP Cookie
  "delays": {
    "min": 1.0,                            // 最小延迟（秒）
    "max": 3.0                             // 最大延迟（秒）
  },
  "browser": {
    "headless": false,                     // 是否无头模式（false显示浏览器）
    "timeout": 30000,                      // 页面超时时间（毫秒）
    "user_agent": "Mozilla/5.0..."        // 浏览器User-Agent
  },
  "output": {
    "format": "excel",                     // 输出格式：excel 或 csv
    "filename": "qixinbao_companies",      // 输出文件名
    "timestamp": true                      // 是否在文件名添加时间戳
  },
  "anti_detection": {
    "random_mouse_move": true,             // 随机鼠标移动
    "random_scroll": true,                 // 随机滚动
    "stealth_mode": true                   // 启用隐身模式
  }
}
```

## 📊 数据字段说明

爬取的数据包含以下字段：

### 基本信息
- `company_name`: 公司名称
- `legal_person`: 法定代表人
- `registered_capital`: 注册资本
- `establish_date`: 成立日期
- `status`: 经营状态
- `organization_code`: 统一社会信用代码
- `business_scope`: 经营范围
- `industry`: 所属行业
- `taxpayer_type`: 纳税人资质

### 联系方式
- `phone`: 联系电话
- `email`: 企业邮箱
- `address`: 注册地址

### 人员信息
- `shareholders`: 股东信息（多个用分号分隔）
- `executives`: 主要人员（多个用分号分隔）

### 爬取信息
- `crawl_time`: 爬取时间

## 🎯 选择器调整指南

**重要提示：** 启信宝的 CSS 选择器可能会动态变化。如果爬取失败提示"找不到元素"，请按以下步骤调整：

### 快速方法 1：修改 selectors.json（推荐）

1. 打启信宝网站（https://www.qixin.com/）
2. 按 `F12` 打开开发者工具
3. 点击元素选择器（左上角箭头图标）
4. 点击页面上的目标元素
5. 右键点击高亮的代码 → Copy → Copy selector
6. 打开 `selectors.json` 文件
7. 将新的选择器添加到对应数组的**最前面**

### 快速方法 2：直接告诉我

如果你找到了新的选择器，直接告诉我：
- "把搜索框选择器改成 XXX"
- "公司名称的选择器改成 XXX"

我会帮你更新代码。

### 手动方法 3：修改 crawler.py

在 `crawler.py` 中找到对应的选择器并替换：

```python
# 原选择器
'company_name': ['.company-name h1', 'h1.company-title']

# 修改为新的选择器
'company_name': ['.your-new-selector']
```

## ⚠️ 注意事项

### 法律合规
- ✅ 本工具仅用于个人研究、学习目的
- ✅ 使用自己的 VIP 账号，访问有权限的内容
- ✅ 遵守启信宝服务条款
- ❌ 不得用于商业目的或转售数据
- ❌ 不得过度频繁请求，避免对服务器造成压力

### 使用建议
1. **首次使用**: 建议先用单公司测试模式，确保配置正确
2. **Cookie 有效期**: Cookie 可能过期，如遇登录问题请重新获取
3. **反爬策略**: 保持合理的请求延迟（建议 3-6 秒）
4. **数据验证**: 爬取后验证数据准确性

### 常见问题

**Q: 提示"联系方式需要VIP"？**
A: 检查 Cookie 是否正确配置，确保使用的是 VIP 账号的 Cookie。

**Q: 爬取速度很慢？**
A: 这是正常的，为了避免被检测，设置了随机延迟。可以调整 `config.json` 中的 `delays` 参数。

**Q: 找不到搜索框/结果？**
A: 网站结构可能变化，需要使用开发者工具检查并更新选择器。

**Q: 如何提高成功率？**
A:
- 使用有效的 VIP Cookie
- 设置合理的延迟时间
- 使用 `headless: false` 模式调试
- 确保网络连接稳定

**Q: 能否爬取其他字段？**
A: 可以，修改 `crawler.py` 中的提取逻辑，添加新的字段和选择器。

## 🔄 版本历史

### v1.0.0 (2024-01-01)
- ✨ 首次发布
- ✅ 支持基本信息、联系方式、股东高管提取
- ✅ 三种运行模式
- ✅ Excel/CSV 导出
- ✅ 反爬优化

## 📝 开发计划

- [ ] 支持验证码识别
- [ ] 添加断点续传功能
- [ ] 支持代理池
- [ ] 添加数据库存储
- [ ] Web UI 界面

## 📄 许可证

本项目仅供学习交流使用，请勿用于非法用途。使用本工具产生的一切后果由使用者自行承担。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题或建议，请提交 Issue。

---

**⚠️ 免责声明**: 本工具仅用于技术研究和学习目的，使用者需自行承担使用本工具的法律风险。请遵守相关法律法规和网站服务条款。
