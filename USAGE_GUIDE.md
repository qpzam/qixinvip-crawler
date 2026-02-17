# 快速使用指南

## 🚀 超简单三步走

### 第 1 步：更新 Cookie（每次使用前）

**推荐方式 - 使用浏览器插件：**

1. 安装 **EditThisCookie** 或 **Cookie-Editor** 插件（Chrome/Edge）
2. 登录启信宝 VIP 账号
3. 点击插件图标 → 导出/复制 Cookie
4. 粘贴到项目的 `cookie.txt` 文件中
5. 保存文件

**传统方式：**
- 按 F12 → Network → 复制 Cookie → 粘贴到 `cookie.txt`

### 第 2 步：运行爬虫

```bash
python main.py
```

选择模式：
- **1** = 测试单个公司
- **2** = 批量爬取
- **3** = 交互式输入

### 第 3 步：查看结果

在项目目录找到生成的 Excel 文件：
```
qixinbao_companies_20240101_120000.xlsx
```

---

## 🔧 选择器调整方法

### 如果提示"找不到搜索框"：

1. 打启信宝网站（https://www.qixin.com/）
2. 按 **F12** 打开开发者工具
3. 点击左上角的小箭头 📍
4. 点击页面上的搜索框
5. 在 Elements 标签中，右键点击高亮的代码
6. 选择 **Copy** → **Copy selector**
7. 告诉我："把搜索框选择器改成 XXX"

或者直接编辑 `selectors.json` 文件，添加新的选择器到最前面。

---

## 📝 输入文件格式

### companies.txt（推荐）
```
腾讯科技（深圳）有限公司
阿里巴巴（中国）有限公司
百度在线网络技术（北京）有限公司
```

### companies.xlsx
| 公司名称 |
|---------|
| 腾讯科技（深圳）有限公司 |
| 阿里巴巴（中国）有限公司 |

---

## ⚡ 常用命令

```bash
# 测试配置
python test.py

# 单公司测试
python main.py
# 选择 1

# 批量爬取（文本文件）
python main.py
# 选择 2 → 3 → 输入文件路径

# 交互式模式
python main.py
# 选择 3
```

---

## 💡 技巧

### Cookie 快速更新
- 安装浏览器 Cookie 插件
- 一键复制 → 粘贴到 cookie.txt
- 无需修改代码

### 调整速度
编辑 `config.json`：
```json
{
  "delays": {
    "min": 1.0,   // 改小 = 更快但风险高
    "max": 3.0    // 改大 = 更慢但更安全
  }
}
```

### 无头模式（不显示浏览器）
```json
{
  "browser": {
    "headless": true  // true = 后台运行，false = 显示浏览器
  }
}
```

---

## ❓ 常见问题

**Q: Cookie 多久更新一次？**
A: 建议每次使用前更新，Cookie 通常 24 小时内有效

**Q: 爬取失败怎么办？**
A:
1. 先运行 `python test.py` 检查配置
2. 检查 Cookie 是否有效
3. 查看浏览器窗口（headless: false）
4. 可能需要更新选择器

**Q: 能爬取所有字段吗？**
A: 需要 VIP 账号才能看到联系方式等字段

**Q: 如何避免被封？**
A:
- 使用合理的延迟（3-6秒）
- 不要频繁运行
- 使用 VIP 账号

---

需要帮助？查看 README.md 获取详细文档！
