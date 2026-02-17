#!/bin/bash

echo "============================================"
echo "       启信宝 VIP 爬虫 v1.0"
echo "============================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python3，请先安装 Python 3.8+"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "[提示] 首次运行，正在安装依赖..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    playwright install chromium
else
    source venv/bin/activate
fi

# 检查配置文件
if [ ! -f "config.json" ]; then
    echo "[警告] 未找到 config.json，正在从示例复制..."
    cp config.example.json config.json
    echo ""
    echo "[重要] 请先编辑 config.json 文件，填入你的启信宝 Cookie"
    echo "配置完成后，请重新运行此脚本"
    exit 0
fi

# 运行主程序
python main.py
