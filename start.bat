@echo off
chcp 65001 > nul
echo ============================================
echo        启信宝 VIP 爬虫 v1.0
echo ============================================
echo.

REM 检查 Python 是否安装
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

REM 检查是否安装了依赖
if not exist "venv\" (
    echo [提示] 首次运行，正在安装依赖...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    playwright install chromium
) else (
    call venv\Scripts\activate.bat
)

REM 检查配置文件
if not exist "config.json" (
    echo [警告] 未找到 config.json，正在从示例复制...
    copy config.example.json config.json
    echo.
    echo [重要] 请先编辑 config.json 文件，填入你的启信宝 Cookie
    echo 按任意键打开配置文件...
    pause > nul
    notepad config.json
    echo.
    echo 配置完成后，请重新运行此脚本
    pause
    exit /b 0
)

REM 运行主程序
python main.py

pause
