#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网易云音乐 HTTP 服务器启动脚本
"""

import os
import sys
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description="网易云音乐 HTTP 服务器")
    parser.add_argument("--host", default="0.0.0.0", help="服务器主机地址 (默认: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="服务器端口 (默认: 8000)")
    parser.add_argument("--reload", action="store_true", help="启用自动重载 (开发模式)")
    parser.add_argument("--log-level", default="info", choices=["debug", "info", "warning", "error"], help="日志级别")
    parser.add_argument("--allowed-ips", help="允许访问的IP地址，用逗号分隔，例如: 192.168.1.100,127.0.0.1")
    parser.add_argument("--allow-all-ips", action="store_true", default=True, help="允许所有IP访问 (默认: True)")
    
    args = parser.parse_args()
    
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_file = os.path.join(script_dir, "src", "http_server.py")
    
    if not os.path.exists(server_file):
        print(f"错误: 找不到服务器文件 {server_file}")
        sys.exit(1)
    
    # 处理IP白名单
    allowed_ips = []
    if args.allowed_ips:
        allowed_ips = [ip.strip() for ip in args.allowed_ips.split(',')]
        args.allow_all_ips = False
    
    print("网易云音乐 HTTP 控制器")
    print(f"服务器地址: http://localhost:{args.port}")
    print(f"API文档: http://localhost:{args.port}/docs")
    print(f"离线文档: http://localhost:{args.port}/docs-offline")
    print(f"ReDoc文档: http://localhost:{args.port}/redoc")
    
    if allowed_ips:
        print(f"允许访问的IP: {', '.join(allowed_ips)}")
        # 通过环境变量传递允许的IP列表
        os.environ['ALLOWED_IPS'] = ','.join(allowed_ips)
    elif not args.allow_all_ips:
        print("警告: 未指定允许的IP地址，将只允许本地访问")
        os.environ['ALLOWED_IPS'] = '127.0.0.1,::1'
    else:
        print("允许所有IP访问")
    
    print()
    
    # 构建uvicorn命令
    cmd = [
        sys.executable, "-m", "uvicorn",
        "src.http_server:app",
        "--host", args.host,
        "--port", str(args.port),
        "--log-level", args.log_level
    ]
    
    if args.reload:
        cmd.append("--reload")
        print("开发模式: 启用自动重载")
    
    print("启动服务器...")
    print(f"命令: {' '.join(cmd)}")
    print()
    
    try:
        subprocess.run(cmd, cwd=script_dir)
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
