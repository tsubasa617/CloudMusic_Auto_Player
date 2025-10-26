@echo off
echo 网易云音乐HTTP控制器 - Windows快速部署
echo =====================================

echo 1. 检查Python版本...
python --version
if %errorlevel% neq 0 (
    echo 错误: Python未安装或未添加到PATH
    pause
    exit /b 1
)

echo 2. 安装依赖包...
pip install fastapi uvicorn requests psutil pyautogui pywin32 selenium -i https://pypi.tuna.tsinghua.edu.cn/simple/
if %errorlevel% neq 0 (
    echo 警告: 部分依赖安装失败，请手动安装
)

echo 3. 检测网易云音乐路径...
python -c "import os; paths=['D:\\NetEase\\CloudMusic\\cloudmusic.exe','C:\\Program Files (x86)\\Netease\\CloudMusic\\cloudmusic.exe','C:\\Program Files\\Netease\\CloudMusic\\cloudmusic.exe']; found=[p for p in paths if os.path.exists(p)]; print('找到路径:', found[0] if found else '未找到')"

echo 4. 创建配置文件...
python -c "import json,os; config={'netease_music_path':'','debug_port':9222,'chromedriver_path':'src/chromedriver/win64/chromedriver.exe'}; json.dump(config,open('netease_config.json','w',encoding='utf-8'),indent=2,ensure_ascii=False); print('配置文件已创建')"

echo 5. 启动服务器...
echo 服务器将在 http://localhost:8000 启动
echo 按 Ctrl+C 停止服务器
python start_http_server.py

pause
