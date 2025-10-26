#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网易云音乐HTTP控制器使用示例
"""

import requests
import json
import time

# 服务器地址
BASE_URL = "http://localhost:8000"

def test_api():
    """测试API功能"""
    print("🎵 网易云音乐HTTP控制器API测试")
    print("=" * 50)
    
    # 1. 获取API信息
    print("\n1. 获取API信息")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 服务器名称: {data['data']['name']}")
            print(f"✅ 版本: {data['data']['version']}")
            print(f"✅ 平台: {data['data']['platform']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return
    
    # 2. 获取控制器信息
    print("\n2. 获取控制器信息")
    try:
        response = requests.get(f"{BASE_URL}/info")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 快捷键可用: {data['data']['hotkey_available']}")
            print(f"✅ 窗口控制可用: {data['data']['window_control_available']}")
            print(f"✅ Selenium可用: {data['data']['selenium_available']}")
            print(f"✅ 支持的动作: {data['data']['supported_actions']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    # 3. 获取配置信息
    print("\n3. 获取配置信息")
    try:
        response = requests.get(f"{BASE_URL}/config")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 网易云音乐路径: {data['data']['netease_music_path']}")
            print(f"✅ 路径状态: {data['data']['path_status']}")
            print(f"✅ ChromeDriver状态: {data['data']['chromedriver_status']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    # 4. 测试启动网易云音乐
    print("\n4. 测试启动网易云音乐")
    try:
        response = requests.post(f"{BASE_URL}/launch", 
                               json={"minimize_window": True})
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ {data['message']}")
            else:
                print(f"❌ {data['error']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    # 等待一下
    print("\n等待3秒...")
    time.sleep(3)
    
    # 5. 测试播放控制
    print("\n5. 测试播放控制")
    try:
        response = requests.post(f"{BASE_URL}/playback", 
                               json={"action": "play_pause"})
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ {data['message']}")
            else:
                print(f"❌ {data['error']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    # 6. 测试搜索播放
    print("\n6. 测试搜索播放")
    try:
        response = requests.post(f"{BASE_URL}/search-play", 
                               json={"query": "稻香 周杰伦", "minimize_window": True})
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ {data['message']}")
                print(f"   歌曲: {data['data']['song_name']}")
                print(f"   歌手: {data['data']['artist']}")
            else:
                print(f"❌ {data['error']}")
        else:
            print(f"❌ 请求失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    print("\n" + "=" * 50)
    print("🎵 API测试完成！")
    print("📖 更多API文档请访问: http://localhost:8000/docs")

if __name__ == "__main__":
    test_api()
