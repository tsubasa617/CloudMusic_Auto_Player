#!/bin/bash
echo "网易云音乐HTTP控制器 - macOS/Linux快速部署"
echo "======================================"

echo "1. 检查Python版本..."
python3 --version
if [ $? -ne 0 ]; then
    echo "错误: Python3未安装"
    exit 1
fi

echo "2. 安装依赖包..."
pip3 install fastapi uvicorn requests psutil pyautogui selenium
if [ $? -ne 0 ]; then
    echo "警告: 部分依赖安装失败，请手动安装"
fi

echo "3. 检测网易云音乐路径..."
python3 -c "
import os
paths = [
    '/Applications/NeteaseMusic.app/Contents/MacOS/NeteaseMusic',
    '/Applications/网易云音乐.app/Contents/MacOS/网易云音乐'
]
found = [p for p in paths if os.path.exists(p)]
print('找到路径:', found[0] if found else '未找到')
"

echo "4. 创建配置文件..."
python3 -c "
import json
config = {
    'netease_music_path': '',
    'debug_port': 9222,
    'chromedriver_path': ''
}
with open('netease_config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
print('配置文件已创建')
"

echo "5. 启动服务器..."
echo "服务器将在 http://localhost:8000 启动"
echo "按 Ctrl+C 停止服务器"
python3 start_http_server.py
