#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网易云音乐HTTP控制器 - 自动部署脚本
"""

import os
import sys
import subprocess
import json
import platform
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    print("检查Python版本...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"❌ Python版本过低: {version.major}.{version.minor}")
        print("需要Python 3.10或更高版本")
        return False
    else:
        print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
        return True

def install_dependencies():
    """安装依赖"""
    print("\n安装依赖包...")
    print("=" * 50)
    
    # 根据平台选择依赖
    if platform.system() == "Windows":
        packages = [
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0", 
            "requests>=2.28.0",
            "psutil>=5.9.0",
            "pyautogui>=0.9.54",
            "pywin32>=306",
            "selenium>=4.0.0"
        ]
    else:
        packages = [
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "requests>=2.28.0", 
            "psutil>=5.9.0",
            "pyautogui>=0.9.54",
            "selenium>=4.0.0"
        ]
    
    for package in packages:
        try:
            print(f"安装 {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✅ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ {package} 安装失败: {e}")
            return False
    
    return True

def detect_netease_music():
    """检测网易云音乐安装路径"""
    print("\n检测网易云音乐安装路径...")
    print("=" * 50)
    
    # 常见安装路径
    if platform.system() == "Windows":
        common_paths = [
            r"D:\NetEase\CloudMusic\cloudmusic.exe",
            r"C:\Program Files (x86)\Netease\CloudMusic\cloudmusic.exe",
            r"C:\Program Files\Netease\CloudMusic\cloudmusic.exe",
            r"C:\Users\{}\AppData\Local\NetEase\CloudMusic\cloudmusic.exe".format(os.getenv('USERNAME', ''))
        ]
    elif platform.system() == "Darwin":  # macOS
        common_paths = [
            "/Applications/NeteaseMusic.app/Contents/MacOS/NeteaseMusic",
            "/Applications/网易云音乐.app/Contents/MacOS/网易云音乐"
        ]
    else:  # Linux
        common_paths = [
            "/opt/netease/cloudmusic/cloudmusic",
            "/usr/local/bin/cloudmusic"
        ]
    
    for path in common_paths:
        if os.path.exists(path):
            print(f"✅ 找到网易云音乐: {path}")
            return path
    
    print("❌ 未找到网易云音乐安装路径")
    return None

def create_config(netease_path):
    """创建配置文件"""
    print("\n创建配置文件...")
    print("=" * 50)
    
    config = {
        "netease_music_path": netease_path or "",
        "debug_port": 9222,
        "chromedriver_path": "src/chromedriver/win64/chromedriver.exe",
        "description": "网易云音乐配置文件 - 用于每日推荐播放功能"
    }
    
    try:
        with open("netease_config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print("✅ 配置文件已创建: netease_config.json")
        return True
    except Exception as e:
        print(f"❌ 创建配置文件失败: {e}")
        return False

def test_server():
    """测试服务器"""
    print("\n测试服务器...")
    print("=" * 50)
    
    try:
        # 导入服务器模块
        sys.path.insert(0, 'src')
        from http_server import app
        print("✅ 服务器模块导入成功")
        
        # 检查路由
        routes = [route.path for route in app.routes if hasattr(route, 'path')]
        print(f"✅ 发现 {len(routes)} 个API端点")
        
        return True
    except Exception as e:
        print(f"❌ 服务器测试失败: {e}")
        return False

def show_usage():
    """显示使用说明"""
    print("\n" + "=" * 60)
    print("🎵 部署完成！")
    print("=" * 60)
    
    print("\n启动服务器:")
    print("python start_http_server.py")
    
    print("\n访问地址:")
    print("- API文档: http://localhost:8000/docs")
    print("- ReDoc文档: http://localhost:8000/redoc")
    print("- 服务器: http://localhost:8000")
    
    print("\n测试功能:")
    print("- 检查配置: curl http://localhost:8000/config")
    print("- 获取信息: curl http://localhost:8000/info")
    print("- 启动音乐: curl -X POST http://localhost:8000/launch")
    
    print("\n功能说明:")
    print("- 基础功能: 播放控制、搜索播放、歌单管理")
    print("- 高级功能: 每日推荐、私人漫游（需要配置路径）")
    
    if platform.system() == "Darwin":
        print("\n⚠️  macOS用户注意:")
        print("- 仅支持基础功能")
        print("- 不支持每日推荐和私人漫游")

def main():
    """主函数"""
    print("网易云音乐HTTP控制器 - 自动部署脚本")
    print("=" * 60)
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"Python版本: {sys.version}")
    
    # 检查Python版本
    if not check_python_version():
        return False
    
    # 安装依赖
    if not install_dependencies():
        print("\n❌ 依赖安装失败，请手动安装")
        return False
    
    # 检测网易云音乐路径
    netease_path = detect_netease_music()
    
    # 创建配置文件
    if not create_config(netease_path):
        print("\n❌ 配置文件创建失败")
        return False
    
    # 测试服务器
    if not test_server():
        print("\n❌ 服务器测试失败")
        return False
    
    # 显示使用说明
    show_usage()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ 部署成功！")
        else:
            print("\n❌ 部署失败！")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n部署被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 部署过程中出现错误: {e}")
        sys.exit(1)
