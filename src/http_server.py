#!/usr/bin/env python3
"""
网易云音乐 HTTP 服务器
通过HTTP请求来控制网易云音乐的各种功能
"""

import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# 导入各个模块
import sys
import os

# 添加src目录到Python路径，确保可以找到模块
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir) if os.path.basename(current_dir) == 'src' else current_dir
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

try:
    # 首先尝试直接导入（适用于打包后的环境）
    from utils.config_manager import (
        load_hotkeys_config,
        load_custom_playlists,
        load_playlists_from_file,
        save_playlists_to_file,
        load_netease_config,
        save_netease_config,
        get_platform
    )
    from utils.music_search import (
        search_netease_music,
        search_netease_playlist,
        generate_play_url,
        generate_playlist_play_url
    )
    from controllers.netease_controller import NeteaseMusicController
    from controllers.daily_controller import DailyRecommendController, SELENIUM_AVAILABLE
except ImportError:
    try:
        # 尝试相对导入（开发环境）
        from .utils.config_manager import (
            load_hotkeys_config,
            load_custom_playlists,
            load_playlists_from_file,
            save_playlists_to_file,
            load_netease_config,
            save_netease_config,
            get_platform
        )
        from .utils.music_search import (
            search_netease_music,
            search_netease_playlist,
            generate_play_url,
            generate_playlist_play_url
        )
        from .controllers.netease_controller import NeteaseMusicController
        from .controllers.daily_controller import DailyRecommendController, SELENIUM_AVAILABLE
    except ImportError:
        # 最后尝试src前缀的绝对导入
        from src.utils.config_manager import (
            load_hotkeys_config,
            load_custom_playlists,
            load_playlists_from_file,
            save_playlists_to_file,
            load_netease_config,
            save_netease_config,
            get_platform
        )
        from src.utils.music_search import (
            search_netease_music,
            search_netease_playlist,
            generate_play_url,
            generate_playlist_play_url
        )
        from src.controllers.netease_controller import NeteaseMusicController
        from src.controllers.daily_controller import DailyRecommendController, SELENIUM_AVAILABLE

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="网易云音乐控制器",
    description="通过HTTP API控制网易云音乐的各种功能",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 自定义Swagger UI配置，使用离线资源
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """自定义Swagger UI页面，使用离线资源避免CDN问题"""
    from fastapi.responses import HTMLResponse
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>网易云音乐控制器 - API文档</title>
        <style>
            body { margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
            .header { background: #1f2937; color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; max-width: 1200px; margin: 0 auto; }
            .endpoint { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin: 12px 0; }
            .method { display: inline-block; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; margin-right: 8px; }
            .get { background: #10b981; color: white; }
            .post { background: #3b82f6; color: white; }
            .path { font-family: monospace; background: #e2e8f0; padding: 4px 8px; border-radius: 4px; }
            .description { margin-top: 8px; color: #64748b; }
            .example { background: #f1f5f9; padding: 12px; border-radius: 6px; margin-top: 8px; font-family: monospace; font-size: 14px; }
            .section { margin: 32px 0; }
            .section h2 { color: #1e293b; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }
            .note { background: #fef3c7; border: 1px solid #f59e0b; border-radius: 6px; padding: 12px; margin: 16px 0; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎵 网易云音乐控制器 API文档</h1>
            <p>通过HTTP API控制网易云音乐的各种功能</p>
        </div>
        
        <div class="content">
            <div class="note">
                <strong>注意：</strong> 由于CDN资源访问问题，此页面使用离线版本。如需交互式文档，请尝试访问 <a href="/redoc">ReDoc文档</a>。
            </div>
            
            <div class="section">
                <h2>基础信息</h2>
                <div class="endpoint">
                    <span class="method get">GET</span> <span class="path">/</span>
                    <div class="description">获取API基本信息</div>
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <span class="path">/info</span>
                    <div class="description">获取控制器信息和支持的功能</div>
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <span class="path">/config</span>
                    <div class="description">获取网易云音乐配置信息</div>
                </div>
                <div class="endpoint">
                    <span class="method get">GET</span> <span class="path">/now-playing</span>
                    <div class="description">获取当前播放的歌曲信息</div>
                </div>
            </div>
            
            <div class="section">
                <h2>应用控制</h2>
                <div class="endpoint">
                    <span class="method post">POST</span> <span class="path">/launch</span>
                    <div class="description">启动网易云音乐应用</div>
                    <div class="example">请求体: {"minimize_window": true}</div>
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> <span class="path">/playback</span>
                    <div class="description">控制播放（播放/暂停/上一首/下一首）</div>
                    <div class="example">请求体: {"action": "play_pause"}<br>支持: play_pause, previous, next</div>
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> <span class="path">/volume</span>
                    <div class="description">控制音量（音量加/减）</div>
                    <div class="example">请求体: {"action": "volume_up"}<br>支持: volume_up, volume_down</div>
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> <span class="path">/mini-mode</span>
                    <div class="description">切换迷你模式</div>
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> <span class="path">/like</span>
                    <div class="description">喜欢当前播放的歌曲</div>
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> <span class="path">/lyrics</span>
                    <div class="description">切换歌词显示</div>
                </div>
            </div>
            
            <div class="section">
                <h2>音乐播放</h2>
                <div class="endpoint">
                    <span class="method post">POST</span> <span class="path">/search-play</span>
                    <div class="description">搜索歌曲并直接播放</div>
                    <div class="example">请求体: {"query": "稻香 周杰伦", "minimize_window": true}</div>
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> <span class="path">/playlist-play</span>
                    <div class="description">播放歌单</div>
                    <div class="example">请求体: {"playlist_name": "飙升榜", "minimize_window": true}<br>支持: 飙升榜, 新歌榜, 热歌榜, 排行榜, 原创榜, 私人雷达</div>
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> <span class="path">/daily-recommend</span>
                    <div class="description">播放每日推荐歌单（需要配置网易云音乐路径）</div>
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> <span class="path">/roaming</span>
                    <div class="description">启动私人漫游功能（需要VIP会员）</div>
                </div>
            </div>
            
            <div class="section">
                <h2>歌单管理</h2>
                <div class="endpoint">
                    <span class="method post">POST</span> <span class="path">/playlist-manage</span>
                    <div class="description">管理自定义歌单</div>
                    <div class="example">请求体: {"action": "list"}<br>支持: list(列出), add(添加), remove(删除)</div>
                </div>
            </div>
            
            <div class="section">
                <h2>使用示例</h2>
                <h3>Python示例</h3>
                <div class="example">
import requests

# 启动网易云音乐
response = requests.post("http://localhost:8000/launch", 
                        json={"minimize_window": True})

# 播放控制
response = requests.post("http://localhost:8000/playback", 
                        json={"action": "play_pause"})

# 搜索并播放歌曲
response = requests.post("http://localhost:8000/search-play", 
                        json={"query": "稻香 周杰伦"})

# 播放歌单
response = requests.post("http://localhost:8000/playlist-play", 
                        json={"playlist_name": "飙升榜"})
                </div>
                
                <h3>curl示例</h3>
                <div class="example">
# 启动网易云音乐
curl -X POST "http://localhost:8000/launch" \\
     -H "Content-Type: application/json" \\
     -d '{"minimize_window": true}'

# 播放控制
curl -X POST "http://localhost:8000/playback" \\
     -H "Content-Type: application/json" \\
     -d '{"action": "play_pause"}'

# 搜索并播放歌曲
curl -X POST "http://localhost:8000/search-play" \\
     -H "Content-Type: application/json" \\
     -d '{"query": "稻香 周杰伦"}'
                </div>
            </div>
            
            <div class="section">
                <h2>其他文档</h2>
                <p>
                    <a href="/redoc">ReDoc文档</a> | 
                    <a href="/docs-offline">离线文档</a> | 
                    <a href="/openapi.json">OpenAPI规范</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# 备用API文档页面（如果CDN有问题）
@app.get("/docs-offline", include_in_schema=False)
async def offline_docs():
    """离线API文档页面"""
    from fastapi.responses import HTMLResponse
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>网易云音乐控制器 - API文档（离线版）</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { font-weight: bold; color: #007bff; }
            .path { font-family: monospace; background: #e9ecef; padding: 2px 5px; }
            h1 { color: #333; }
            h2 { color: #666; border-bottom: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <h1>🎵 网易云音乐控制器 API文档</h1>
        <p>如果Swagger UI无法加载，请使用此离线版本。</p>
        
        <h2>基础信息</h2>
        <div class="endpoint">
            <span class="method">GET</span> <span class="path">/</span> - 获取API基本信息
        </div>
        <div class="endpoint">
            <span class="method">GET</span> <span class="path">/info</span> - 获取控制器信息
        </div>
        <div class="endpoint">
            <span class="method">GET</span> <span class="path">/config</span> - 获取配置信息
        </div>
        <div class="endpoint">
            <span class="method">GET</span> <span class="path">/now-playing</span> - 获取当前播放的歌曲信息
        </div>
        
        <h2>应用控制</h2>
        <div class="endpoint">
            <span class="method">POST</span> <span class="path">/launch</span> - 启动网易云音乐<br>
            请求体: {"minimize_window": true}
        </div>
        <div class="endpoint">
            <span class="method">POST</span> <span class="path">/playback</span> - 播放控制<br>
            请求体: {"action": "play_pause"} (支持: play_pause, previous, next)
        </div>
        <div class="endpoint">
            <span class="method">POST</span> <span class="path">/volume</span> - 音量控制<br>
            请求体: {"action": "volume_up"} (支持: volume_up, volume_down)
        </div>
        <div class="endpoint">
            <span class="method">POST</span> <span class="path">/mini-mode</span> - 切换迷你模式
        </div>
        <div class="endpoint">
            <span class="method">POST</span> <span class="path">/like</span> - 喜欢当前歌曲
        </div>
        <div class="endpoint">
            <span class="method">POST</span> <span class="path">/lyrics</span> - 切换歌词显示
        </div>
        
        <h2>音乐播放</h2>
        <div class="endpoint">
            <span class="method">POST</span> <span class="path">/search-play</span> - 搜索并播放歌曲<br>
            请求体: {"query": "稻香 周杰伦", "minimize_window": true}
        </div>
        <div class="endpoint">
            <span class="method">POST</span> <span class="path">/playlist-play</span> - 播放歌单<br>
            请求体: {"playlist_name": "飙升榜", "minimize_window": true}
        </div>
        <div class="endpoint">
            <span class="method">POST</span> <span class="path">/daily-recommend</span> - 播放每日推荐
        </div>
        <div class="endpoint">
            <span class="method">POST</span> <span class="path">/roaming</span> - 启动私人漫游
        </div>
        
        <h2>歌单管理</h2>
        <div class="endpoint">
            <span class="method">POST</span> <span class="path">/playlist-manage</span> - 管理歌单<br>
            请求体: {"action": "list"} (支持: list, add, remove)
        </div>
        
        <h2>使用示例</h2>
        <h3>Python示例</h3>
        <pre style="background: #f8f9fa; padding: 15px; border-radius: 5px;">
import requests

# 启动网易云音乐
response = requests.post("http://localhost:8000/launch", 
                        json={"minimize_window": True})

# 播放控制
response = requests.post("http://localhost:8000/playback", 
                        json={"action": "play_pause"})

# 搜索并播放歌曲
response = requests.post("http://localhost:8000/search-play", 
                        json={"query": "稻香 周杰伦"})
        </pre>
        
        <h3>curl示例</h3>
        <pre style="background: #f8f9fa; padding: 15px; border-radius: 5px;">
# 启动网易云音乐
curl -X POST "http://localhost:8000/launch" \\
     -H "Content-Type: application/json" \\
     -d '{"minimize_window": true}'

# 播放控制
curl -X POST "http://localhost:8000/playback" \\
     -H "Content-Type: application/json" \\
     -d '{"action": "play_pause"}'
        </pre>
        
        <p><strong>注意：</strong> 如果Swagger UI正常加载，请访问 <a href="/docs">/docs</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# 全局变量
USER_CUSTOM_PLAYLISTS = {}
_daily_controller = None

# 初始化控制器
def _initialize_controller():
    """初始化音乐控制器"""
    hotkeys = load_hotkeys_config()
    return NeteaseMusicController(hotkeys)

# 创建控制器实例
music_controller = _initialize_controller()

@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化逻辑"""
    global _daily_controller
    
    try:
        # 如果Selenium可用，尝试初始化_daily_controller
        if SELENIUM_AVAILABLE:
            logger.info("🔧 初始化Selenium控制器...")
            try:
                config = load_netease_config()
                
                # 检查是否配置了网易云音乐路径
                netease_path = config.get("netease_music_path", "")
                if netease_path and os.path.exists(netease_path):
                    _daily_controller = DailyRecommendController(config)
                    logger.info("✅ Selenium控制器创建成功")
                    
                    # 尝试连接（不强制，如果网易云没运行就跳过）
                    try:
                        if _daily_controller.connect_to_netease():
                            logger.info("✅ Selenium已连接到网易云音乐")
                        else:
                            logger.info("ℹ️ 网易云音乐未运行，Selenium将在首次使用 daily-recommend 时连接")
                    except Exception as e:
                        logger.debug(f"连接网易云失败（正常）: {e}")
                        logger.info("ℹ️ 网易云音乐未运行，将在需要时连接")
                else:
                    logger.info("⚠️ 网易云音乐路径未配置，跳过Selenium初始化")
            except Exception as e:
                logger.warning(f"⚠️ Selenium控制器初始化失败: {e}")
                logger.info("现在playing功能将在首次调用每日推荐时初始化")
        else:
            logger.info("ℹ️ Selenium不可用，跳过初始化")
    except Exception as e:
        logger.error(f"启动事件失败: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的清理逻辑"""
    global _daily_controller
    
    try:
        if _daily_controller and _daily_controller.driver:
            logger.info("🔧 断开Selenium连接...")
            _daily_controller.disconnect()
            _daily_controller = None
            logger.info("✅ Selenium连接已断开")
    except Exception as e:
        logger.error(f"关闭事件失败: {e}")

# Pydantic模型定义
class LaunchRequest(BaseModel):
    minimize_window: bool = True

class PlaybackRequest(BaseModel):
    action: str = "play_pause"

class VolumeRequest(BaseModel):
    action: str = "volume_up"

class SearchPlayRequest(BaseModel):
    query: str
    minimize_window: bool = True

class PlaylistRequest(BaseModel):
    query: str = ""
    playlist_name: str = ""
    minimize_window: bool = True

class PlaylistManageRequest(BaseModel):
    action: str = "list"
    playlist_name: str = ""
    playlist_id: str = ""
    description: str = ""

class ApiResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    error: Optional[str] = None

# ============ HTTP API 端点 ============

@app.get("/", response_model=ApiResponse)
async def root():
    """根路径，返回API信息"""
    return ApiResponse(
        success=True,
        data={
            "name": "网易云音乐控制器",
            "version": "1.0.0",
            "platform": get_platform(),
            "endpoints": [
                "/docs - API文档",
                "/launch - 启动网易云音乐",
                "/playback - 播放控制",
                "/volume - 音量控制",
                "/mini-mode - 切换迷你模式",
                "/like - 喜欢当前歌曲",
                "/lyrics - 切换歌词显示",
                "/search-play - 搜索并播放歌曲",
                "/playlist-play - 播放歌单",
                "/playlist-manage - 管理歌单",
                "/daily-recommend - 播放每日推荐",
                "/roaming - 启动私人漫游",
                "/info - 获取控制器信息",
                "/config - 获取配置信息"
            ]
        },
        message="网易云音乐HTTP控制器API"
    )

@app.post("/launch", response_model=ApiResponse)
async def launch_netease_music(request: LaunchRequest):
    """启动网易云音乐应用"""
    global _daily_controller
    
    try:
        # 使用orpheus://直接启动
        scheme_url = music_controller.url_schemes["open"]
        
        # 启动应用
        success = music_controller.launch_by_url_scheme(scheme_url, request.minimize_window)
        
        if success:
            # 如果Selenium可用且未连接，尝试在启动后连接
            if SELENIUM_AVAILABLE and _daily_controller and not _daily_controller.driver:
                try:
                    logger.info("🔧 网易云启动成功，尝试连接Selenium...")
                    import time
                    import socket
                    
                    # 等待网易云完全启动并检查调试端口
                    debug_port = _daily_controller.config.get("debug_port", 9222)
                    connected = False
                    
                    for i in range(5):  # 最多等待10秒
                        time.sleep(2)
                        # 检查调试端口是否可用
                        try:
                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                                s.settimeout(1)
                                if s.connect_ex(('localhost', debug_port)) == 0:
                                    logger.info(f"调试端口可用，尝试连接...")
                                    if _daily_controller.connect_only():
                                        logger.info("✅ Selenium已连接到网易云音乐")
                                        connected = True
                                        break
                        except:
                            pass
                        logger.debug(f"等待调试端口... ({i+1}/5)")
                    
                    if not connected:
                        logger.info("ℹ️ 暂无法连接，将在首次使用高级功能时连接")
                except Exception as e:
                    logger.debug(f"自动连接失败: {e}")
            
            return ApiResponse(
                success=True,
                data={
                    "scheme_url": scheme_url,
                    "minimized": request.minimize_window,
                    "platform": get_platform(),
                    "selenium_connected": _daily_controller and _daily_controller.driver is not None if SELENIUM_AVAILABLE else False
                },
                message="[OK] 网易云音乐启动成功"
            )
        else:
            return ApiResponse(
                success=False,
                error="网易云音乐启动失败"
            )
            
    except Exception as e:
        return ApiResponse(
            success=False,
            error=f"启动网易云音乐时出错: {str(e)}"
        )

@app.post("/playback", response_model=ApiResponse)
async def control_playback(request: PlaybackRequest):
    """控制网易云音乐播放（全局快捷键）"""
    try:
        valid_actions = ["play_pause", "previous", "next"]
        if request.action not in valid_actions:
            return ApiResponse(
                success=False,
                error=f"无效的action参数: {request.action}，支持的值: {', '.join(valid_actions)}"
            )
        
        success = music_controller.send_global_hotkey(request.action)
        
        if success:
            return ApiResponse(
                success=True,
                data={
                    "action": request.action,
                    "hotkey": music_controller.get_hotkey_for_action(request.action),
                    "platform": get_platform()
                },
                message=f"[OK] 播放控制成功 - {request.action}"
            )
        else:
            return ApiResponse(
                success=False,
                error=f"播放控制失败 - {request.action}"
            )
            
    except Exception as e:
        return ApiResponse(
            success=False,
            error=f"播放控制时出错: {str(e)}"
        )

@app.post("/volume", response_model=ApiResponse)
async def control_volume(request: VolumeRequest):
    """控制网易云音乐音量（全局快捷键）"""
    try:
        valid_actions = ["volume_up", "volume_down"]
        if request.action not in valid_actions:
            return ApiResponse(
                success=False,
                error=f"无效的action参数: {request.action}，支持的值: {', '.join(valid_actions)}"
            )
        
        success = music_controller.send_global_hotkey(request.action)
        
        if success:
            return ApiResponse(
                success=True,
                data={
                    "action": request.action,
                    "hotkey": music_controller.get_hotkey_for_action(request.action),
                    "platform": get_platform()
                },
                message=f"[OK] 音量控制成功 - {request.action}"
            )
        else:
            return ApiResponse(
                success=False,
                error=f"音量控制失败 - {request.action}"
            )
            
    except Exception as e:
        return ApiResponse(
            success=False,
            error=f"音量控制时出错: {str(e)}"
        )

@app.post("/mini-mode", response_model=ApiResponse)
async def toggle_mini_mode():
    """切换网易云音乐迷你模式（全局快捷键）"""
    try:
        success = music_controller.send_global_hotkey("mini_mode")
        
        if success:
            return ApiResponse(
                success=True,
                data={
                    "action": "mini_mode",
                    "hotkey": music_controller.get_hotkey_for_action("mini_mode"),
                    "platform": get_platform()
                },
                message="[OK] 迷你模式切换成功"
            )
        else:
            return ApiResponse(
                success=False,
                error="迷你模式切换失败"
            )
            
    except Exception as e:
        return ApiResponse(
            success=False,
            error=f"迷你模式切换时出错: {str(e)}"
        )

@app.post("/like", response_model=ApiResponse)
async def like_current_song():
    """喜欢当前播放的歌曲（全局快捷键）"""
    try:
        success = music_controller.send_global_hotkey("like_song")
        
        if success:
            return ApiResponse(
                success=True,
                data={
                    "action": "like_song",
                    "hotkey": music_controller.get_hotkey_for_action("like_song"),
                    "platform": get_platform()
                },
                message="[OK] 歌曲喜欢操作成功"
            )
        else:
            return ApiResponse(
                success=False,
                error="歌曲喜欢操作失败"
            )
            
    except Exception as e:
        return ApiResponse(
            success=False,
            error=f"歌曲喜欢操作时出错: {str(e)}"
        )

@app.post("/lyrics", response_model=ApiResponse)
async def toggle_lyrics():
    """打开/关闭歌词显示（全局快捷键）"""
    try:
        success = music_controller.send_global_hotkey("lyrics")
        
        if success:
            return ApiResponse(
                success=True,
                data={
                    "action": "lyrics",
                    "hotkey": music_controller.get_hotkey_for_action("lyrics"),
                    "platform": get_platform()
                },
                message="[OK] 歌词显示切换成功"
            )
        else:
            return ApiResponse(
                success=False,
                error="歌词显示切换失败"
            )
            
    except Exception as e:
        return ApiResponse(
            success=False,
            error=f"歌词显示切换时出错: {str(e)}"
        )

@app.post("/search-play", response_model=ApiResponse)
async def search_and_play(request: SearchPlayRequest):
    """搜索歌曲并直接播放"""
    try:
        # 搜索歌曲
        song_id, song_name, artist_name = search_netease_music(request.query)
        
        if not song_id:
            return ApiResponse(
                success=False,
                error=f"未找到歌曲: {request.query}"
            )
        
        # 生成播放URL
        play_url = generate_play_url(song_id)
        
        if not play_url:
            return ApiResponse(
                success=False,
                error="生成播放URL失败"
            )
        
        # 直接播放歌曲（带最小化选项）
        success = music_controller.launch_by_url_scheme(play_url, request.minimize_window)
        
        if success:
            return ApiResponse(
                success=True,
                data={
                    "query": request.query,
                    "song_name": song_name,
                    "artist": artist_name,
                    "song_id": song_id,
                    "play_url": play_url,
                    "minimized": request.minimize_window,
                    "platform": get_platform()
                },
                message=f"[OK] 成功播放: 《{song_name}》- {artist_name}"
            )
        else:
            return ApiResponse(
                success=False,
                error=f"播放失败: 《{song_name}》- {artist_name}"
            )
            
    except Exception as e:
        return ApiResponse(
            success=False,
            error=f"搜索播放歌曲时出错: {str(e)}"
        )

@app.post("/playlist-play", response_model=ApiResponse)
async def search_and_play_playlist(request: PlaylistRequest):
    """搜索歌单并直接播放"""
    try:
        # 加载所有歌单配置
        all_playlists = load_custom_playlists()
        
        playlist_id = None
        playlist_name_result = None
        
        # 检查是否在配置的歌单中
        if request.playlist_name and request.playlist_name in all_playlists:
            playlist_id = all_playlists[request.playlist_name]
            playlist_name_result = request.playlist_name
            logger.info(f"[OK] 使用配置歌单: {playlist_name_result} (ID: {playlist_id})")
        elif request.query:
            # 搜索歌单
            playlist_id, playlist_name_result = search_netease_playlist(request.query)
            if not playlist_id:
                return ApiResponse(
                    success=False,
                    error=f"未找到歌单: {request.query}"
                )
        else:
            return ApiResponse(
                success=False,
                error="请提供搜索关键词(query)或常用歌单名称(playlist_name)"
            )
        
        # 生成播放URL
        play_url = generate_playlist_play_url(playlist_id)
        
        if not play_url:
            return ApiResponse(
                success=False,
                error="生成歌单播放URL失败"
            )
        
        # 直接播放歌单（带最小化选项）
        success = music_controller.launch_by_url_scheme(play_url, request.minimize_window)
        
        if success:
            return ApiResponse(
                success=True,
                data={
                    "query": request.query if request.query else request.playlist_name,
                    "playlist_name": playlist_name_result,
                    "playlist_id": playlist_id,
                    "play_url": play_url,
                    "minimized": request.minimize_window,
                    "platform": get_platform()
                },
                message=f"[OK] 成功播放歌单: 《{playlist_name_result}》"
            )
        else:
            return ApiResponse(
                success=False,
                error=f"播放歌单失败: 《{playlist_name_result}》"
            )
            
    except Exception as e:
        return ApiResponse(
            success=False,
            error=f"搜索播放歌单时出错: {str(e)}"
        )

@app.post("/playlist-manage", response_model=ApiResponse)
async def manage_custom_playlists(request: PlaylistManageRequest):
    """管理用户自定义歌单"""
    try:
        global USER_CUSTOM_PLAYLISTS
        
        if request.action == "list":
            # 获取完整的歌单数据
            playlists_data = load_playlists_from_file()
            
            return ApiResponse(
                success=True,
                data={
                    "system_playlists": playlists_data.get("systemPlaylists", {}),
                    "user_playlists": playlists_data.get("userPlaylists", {}),
                    "total_system": len(playlists_data.get("systemPlaylists", {})),
                    "total_user": len(playlists_data.get("userPlaylists", {})),
                    "total_count": len(playlists_data.get("systemPlaylists", {})) + len(playlists_data.get("userPlaylists", {})),
                    "source": "playlists_file",
                    "platform": get_platform()
                },
                message=f"[OK] 系统歌单 {len(playlists_data.get('systemPlaylists', {}))} 个，用户歌单 {len(playlists_data.get('userPlaylists', {}))} 个"
            )
        
        elif request.action == "add":
            if not request.playlist_name or not request.playlist_id:
                return ApiResponse(
                    success=False,
                    error="添加歌单需要提供歌单名称和歌单ID"
                )
            
            # 加载当前配置
            playlists_data = load_playlists_from_file()
            
            # 检查是否与系统歌单重名
            if request.playlist_name in playlists_data.get("systemPlaylists", {}):
                return ApiResponse(
                    success=False,
                    error=f"歌单名称 '{request.playlist_name}' 与系统预设歌单重名，请使用其他名称"
                )
            
            # 添加到用户歌单
            if "userPlaylists" not in playlists_data:
                playlists_data["userPlaylists"] = {}
            
            playlists_data["userPlaylists"][request.playlist_name] = {
                "id": request.playlist_id,
                "name": request.playlist_name,
                "description": request.description if request.description else f"用户自定义歌单: {request.playlist_name}"
            }
            
            # 保存到文件
            if save_playlists_to_file(playlists_data):
                logger.info(f"已将歌单添加到playlists.json: {request.playlist_name}")
                return ApiResponse(
                    success=True,
                    data={
                        "playlist_name": request.playlist_name,
                        "playlist_id": request.playlist_id,
                        "description": request.description,
                        "storage": "playlists_file",
                        "platform": get_platform()
                    },
                    message=f"[OK] 成功添加用户歌单: {request.playlist_name} (ID: {request.playlist_id})"
                )
            else:
                return ApiResponse(
                    success=False,
                    error="保存歌单配置失败"
                )
        
        elif request.action == "remove":
            if not request.playlist_name:
                return ApiResponse(
                    success=False,
                    error="删除歌单需要提供歌单名称"
                )
            
            # 加载当前配置
            playlists_data = load_playlists_from_file()
            
            # 检查是否尝试删除系统歌单
            if request.playlist_name in playlists_data.get("systemPlaylists", {}):
                return ApiResponse(
                    success=False,
                    error=f"不能删除系统预设歌单: {request.playlist_name}"
                )
            
            # 检查用户歌单中是否存在
            if request.playlist_name not in playlists_data.get("userPlaylists", {}):
                return ApiResponse(
                    success=False,
                    error=f"未找到用户歌单: {request.playlist_name}"
                )
            
            # 获取要删除的歌单信息
            removed_playlist = playlists_data["userPlaylists"][request.playlist_name]
            removed_id = removed_playlist.get("id", "unknown")
            
            # 从用户歌单中删除
            del playlists_data["userPlaylists"][request.playlist_name]
            
            # 保存到文件
            if save_playlists_to_file(playlists_data):
                logger.info(f"已从playlists.json中删除歌单: {request.playlist_name}")
                return ApiResponse(
                    success=True,
                    data={
                        "playlist_name": request.playlist_name,
                        "playlist_id": removed_id,
                        "storage": "playlists_file",
                        "platform": get_platform()
                    },
                    message=f"[OK] 成功删除用户歌单: {request.playlist_name} (ID: {removed_id})"
                )
            else:
                return ApiResponse(
                    success=False,
                    error="保存歌单配置失败"
                )
        
        else:
            return ApiResponse(
                success=False,
                error=f"不支持的操作: {request.action}，支持的值: list, add, remove"
            )
            
    except Exception as e:
        return ApiResponse(
            success=False,
            error=f"管理自定义歌单时出错: {str(e)}"
        )

@app.get("/info", response_model=ApiResponse)
async def get_controller_info():
    """获取控制器信息和支持的功能"""
    try:
        # 加载自定义歌单
        custom_playlists = load_custom_playlists()
        
        return ApiResponse(
            success=True,
            data={
                "server_name": "网易云音乐控制器",
                "platform": get_platform(),
                "hotkey_available": music_controller.is_hotkey_available(),
                "window_control_available": music_controller.is_window_control_available(),
                "selenium_available": SELENIUM_AVAILABLE,
                "supported_actions": music_controller.get_supported_actions(),
                "hotkey_mappings": music_controller.hotkeys,
                "url_schemes": list(music_controller.url_schemes.keys()),
                "custom_playlists": custom_playlists,
                "custom_playlists_count": len(custom_playlists)
            },
            message="[OK] 控制器信息获取成功"
        )
        
    except Exception as e:
        return ApiResponse(
            success=False,
            error=f"获取控制器信息时出错: {str(e)}"
        )

@app.get("/config", response_model=ApiResponse)
async def get_netease_config():
    """获取网易云音乐配置信息"""
    try:
        import os
        
        config = load_netease_config()
        
        # 检查路径状态
        netease_path = config.get("netease_music_path", "")
        path_status = "未配置"
        if netease_path:
            if os.path.exists(netease_path):
                path_status = "[OK] 有效"
            else:
                path_status = "[ERROR] 无效"
        
        # 获取项目根目录
        project_root = os.path.dirname(os.path.dirname(__file__))
        
        # 检查ChromeDriver状态
        chromedriver_path = os.path.join(
            project_root,
            config.get("chromedriver_path", "src/chromedriver/win64/chromedriver.exe")
        )
        chromedriver_status = "[OK] 存在" if os.path.exists(chromedriver_path) else "[ERROR] 不存在"
        
        return ApiResponse(
            success=True,
            data={
                "netease_music_path": netease_path or "未配置",
                "path_status": path_status,
                "debug_port": config.get("debug_port", 9222),
                "chromedriver_path": config.get("chromedriver_path", "src/chromedriver/win64/chromedriver.exe"),
                "chromedriver_status": chromedriver_status,
                "selenium_available": SELENIUM_AVAILABLE,
                "platform": get_platform()
            },
            message="[OK] 配置信息获取成功"
        )
        
    except Exception as e:
        logger.error(f"获取配置失败: {e}")
        return ApiResponse(
            success=False,
            error=f"获取配置失败: {str(e)}"
        )

@app.get("/now-playing", response_model=ApiResponse)
async def get_now_playing():
    """获取当前正在播放的歌曲信息"""
    try:
        # 初始化播放状态变量
        is_playing = None
        
        # 暂时跳过Selenium检查，因为is_playing的判断逻辑不准确
        # 我们优先使用窗口标题，它更快更稳定
        if SELENIUM_AVAILABLE and _daily_controller and hasattr(_daily_controller, 'driver') and _daily_controller.driver:
            # Selenium已连接，但我们暂时不使用is_playing判断
            # 因为现有的判断逻辑不够准确
            pass
        
        # 方法2: 尝试从窗口标题获取（Windows）
        try:
            import win32gui
            import win32con
            import win32process
            import psutil
            
            def enum_windows_callback(hwnd, result):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    
                    try:
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        process = psutil.Process(pid)
                        process_name = process.name().lower()
                        
                        # 检查是否是网易云音乐进程
                        if process_name == "cloudmusic.exe" or "cloudmusic" in process_name:
                            if window_title and window_title not in ["网易云音乐", "NetEase CloudMusic"]:
                                # 窗口标题通常包含歌曲信息
                                result.append(window_title)
                    except:
                        pass
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                title = windows[0]
                # 如果从Selenium获取了播放状态，使用它
                method = "combined" if is_playing is not None else "window_title"
                return ApiResponse(
                    success=True,
                    data={
                        "song_name": title,
                        "is_playing": is_playing,
                        "method": method,
                        "note": "song_name from window_title, is_playing from Selenium" if method == "combined" else "无法获取播放状态"
                    },
                    message=f"[OK] 从窗口标题获取: {title}"
                )
        except Exception as e:
            logger.debug(f"窗口标题方式获取失败: {e}")
        
        # 如果所有方法都失败
        return ApiResponse(
            success=False,
            data={
                "song_name": None,
                "is_playing": None,
                "method": "none"
            },
            message="无法获取当前播放信息",
            error="可能需要先启动网易云音乐并播放歌曲"
        )
        
    except Exception as e:
        logger.error(f"获取当前播放信息失败: {e}")
        return ApiResponse(
            success=False,
            error=f"获取当前播放信息失败: {str(e)}"
        )

@app.post("/daily-recommend", response_model=ApiResponse)
async def play_daily_recommend():
    """播放网易云音乐每日推荐歌单"""
    global _daily_controller
    
    try:
        # 检查Selenium可用性
        if not SELENIUM_AVAILABLE:
            return ApiResponse(
                success=False,
                error="Selenium不可用，请安装selenium: pip install selenium -i https://pypi.tuna.tsinghua.edu.cn/simple/"
            )
        
        # 检查配置
        config = load_netease_config()
        netease_path = config.get("netease_music_path", "")
        
        if not netease_path:
            return ApiResponse(
                success=False,
                error="网易云音乐路径未配置，请设置环境变量 NETEASE_MUSIC_PATH 或在 netease_config.json 中配置 netease_music_path"
            )
        
        import os
        if not os.path.exists(netease_path):
            return ApiResponse(
                success=False,
                error=f"网易云音乐路径无效: {netease_path}，请重新设置环境变量 NETEASE_MUSIC_PATH 或在 netease_config.json 中配置正确的路径"
            )
        
        # 创建或重用控制器实例
        if not _daily_controller:
            _daily_controller = DailyRecommendController(config)
        
        logger.info("🎵 开始播放每日推荐（固定路径版本）...")
        
        # 连接到网易云音乐
        if not _daily_controller.connect_to_netease():
            return ApiResponse(
                success=False,
                error="无法连接到网易云音乐，可能的原因: 1. 网易云音乐启动失败 2. ChromeDriver连接失败 3. 调试端口被占用"
            )
        
        # 显示使用的按钮路径信息
        button_paths_info = {
            "container_selector": _daily_controller.button_paths["daily_wrapper"]["selector"],
            "button_exact_path": _daily_controller.button_paths["play_button"]["xpath"],
            "backup_selectors_count": len(_daily_controller.button_paths["play_button"]["absolute_selectors"])
        }
        
        # 执行播放每日推荐（使用固定路径策略）
        logger.info("🎵 开始执行每日推荐播放操作（固定路径）...")
        play_result = _daily_controller.play_daily_recommend()
        
        # 获取详细的状态信息
        try:
            current_music = _daily_controller.get_current_music()
            is_playing = _daily_controller.is_playing()
            has_playlist = _daily_controller.has_playlist()
            current_url = _daily_controller.driver.current_url if _daily_controller.driver else "无法获取"
            page_title = _daily_controller.driver.title if _daily_controller.driver else "无法获取"
        except Exception as e:
            logger.warning(f"获取状态信息失败: {e}")
            current_music = "获取失败"
            is_playing = False
            has_playlist = False
            current_url = "获取失败"
            page_title = "获取失败"
        
        if play_result:
            return ApiResponse(
                success=True,
                data={
                    "current_music": current_music or "正在加载...",
                    "is_playing": is_playing,
                    "has_playlist": has_playlist,
                    "current_url": current_url,
                    "page_title": page_title,
                    "button_paths_used": button_paths_info,
                    "version": "fixed_path_optimized",
                    "status": "播放操作已执行并验证成功",
                    "platform": get_platform()
                },
                message="🎵 每日推荐播放成功（固定路径版本）！"
            )
        else:
            return ApiResponse(
                success=False,
                error="播放每日推荐失败（固定路径版本），可能的原因: 1. 网易云音乐界面已更新，固定路径失效 2. 网络连接问题 3. ChromeDriver版本不兼容 4. 网易云音乐客户端版本过旧或过新"
            )
        
    except Exception as e:
        logger.error(f"播放每日推荐时出错: {e}")
        
        # 重置控制器
        if _daily_controller:
            _daily_controller.disconnect()
            _daily_controller = None
        
        return ApiResponse(
            success=False,
            error=f"播放失败: {str(e)}"
        )

@app.post("/roaming", response_model=ApiResponse)
async def play_roaming():
    """启动网易云音乐私人漫游功能"""
    global _daily_controller
    
    try:
        # 检查Selenium可用性
        if not SELENIUM_AVAILABLE:
            return ApiResponse(
                success=False,
                error="Selenium不可用，请安装selenium: pip install selenium -i https://pypi.tuna.tsinghua.edu.cn/simple/"
            )
        
        # 检查配置
        config = load_netease_config()
        netease_path = config.get("netease_music_path", "")
        
        if not netease_path:
            return ApiResponse(
                success=False,
                error="网易云音乐路径未配置，请设置环境变量 NETEASE_MUSIC_PATH 或在 netease_config.json 中配置 netease_music_path"
            )
        
        import os
        if not os.path.exists(netease_path):
            return ApiResponse(
                success=False,
                error=f"网易云音乐路径无效: {netease_path}，请重新设置环境变量 NETEASE_MUSIC_PATH 或在 netease_config.json 中配置正确的路径"
            )
        
        # 创建或重用控制器实例
        if not _daily_controller:
            _daily_controller = DailyRecommendController(config)
        
        logger.info("🌍 开始启动私人漫游...")
        
        # 连接到网易云音乐
        if not _daily_controller.connect_to_netease():
            return ApiResponse(
                success=False,
                error="无法连接到网易云音乐，可能的原因: 1. 网易云音乐启动失败 2. ChromeDriver连接失败 3. 调试端口被占用"
            )
        
        # 显示使用的按钮路径信息
        roaming_paths_info = {
            "primary_xpath": _daily_controller.button_paths["roaming_button"]["xpath"],
            "button_title": _daily_controller.button_paths["roaming_button"]["title"],
            "backup_selectors_count": len(_daily_controller.button_paths["roaming_button"]["backup_selectors"]),
            "description": _daily_controller.button_paths["roaming_button"]["description"]
        }
        
        # 执行漫游功能
        logger.info("🌍 开始执行私人漫游启动操作...")
        roaming_result = _daily_controller.play_roaming()
        
        # 获取详细的状态信息
        try:
            current_url = _daily_controller.driver.current_url if _daily_controller.driver else "无法获取"
            page_title = _daily_controller.driver.title if _daily_controller.driver else "无法获取"
            
            # 检查是否有漫游相关元素
            roaming_elements_count = 0
            if _daily_controller.driver:
                try:
                    from selenium.webdriver.common.by import By
                    roaming_elements = _daily_controller.driver.find_elements(By.XPATH, "//*[contains(text(), '漫游')]")
                    roaming_elements_count = len(roaming_elements)
                except:
                    pass
        except Exception as e:
            logger.warning(f"获取状态信息失败: {e}")
            current_url = "获取失败"
            page_title = "获取失败"
            roaming_elements_count = 0
        
        if roaming_result:
            return ApiResponse(
                success=True,
                data={
                    "roaming_status": "已启动",
                    "current_url": current_url,
                    "page_title": page_title,
                    "roaming_elements_found": roaming_elements_count,
                    "button_paths_used": roaming_paths_info,
                    "status": "漫游按钮点击操作已执行",
                    "platform": get_platform()
                },
                message="🌍 私人漫游启动成功！"
            )
        else:
            return ApiResponse(
                success=False,
                error="启动私人漫游失败，可能的原因: 1. 网易云音乐界面已更新，按钮路径失效 2. 漫游按钮不可见或被禁用 3. 账户没有VIP权限或漫游权限 4. ChromeDriver版本不兼容"
            )
        
    except Exception as e:
        logger.error(f"启动私人漫游时出错: {e}")
        
        # 重置控制器
        if _daily_controller:
            _daily_controller.disconnect()
            _daily_controller = None
        
        return ApiResponse(
            success=False,
            error=f"漫游启动失败: {str(e)}"
        )

# ============ 服务器启动 ============

def main():
    """主函数"""
    try:
        print("🎵 网易云音乐 HTTP 控制器")
    except UnicodeEncodeError:
        print("网易云音乐 HTTP 控制器")
    
    print(f"当前平台: {get_platform()}")
    print("支持的功能:")
    print("- HTTP API 控制")
    print("- 全局快捷键控制")
    print("- 音乐搜索播放")
    print("- 歌单管理")
    print("- 每日推荐播放")
    print("- 私人漫游功能")
    
    # 显示当前快捷键配置
    current_hotkeys = load_hotkeys_config()
    
    try:
        print(f"  • 播放/暂停: {current_hotkeys.get('play_pause', '未配置')}")
        print(f"  • 上一首: {current_hotkeys.get('previous', '未配置')}")
        print(f"  • 下一首: {current_hotkeys.get('next', '未配置')}")
        print(f"  • 音量加/减: {current_hotkeys.get('volume_up', '未配置')}/{current_hotkeys.get('volume_down', '未配置')}")
        print(f"  • 迷你模式: {current_hotkeys.get('mini_mode', '未配置')}")
        print(f"  • 喜欢歌曲: {current_hotkeys.get('like_song', '未配置')}")
        print(f"  • 歌词显示: {current_hotkeys.get('lyrics', '未配置')}")
    except UnicodeEncodeError:
        print("  - 快捷键配置已加载")
    
    # 检查依赖
    if not music_controller.is_hotkey_available():
        try:
            print("⚠️ 警告: 快捷键功能不可用")
        except UnicodeEncodeError:
            print("警告: 快捷键功能不可用")
        print("请安装依赖: pip install pyautogui -i https://pypi.tuna.tsinghua.edu.cn/simple/")
    
    if not SELENIUM_AVAILABLE:
        try:
            print("⚠️ 警告: Selenium不可用，每日推荐功能将无法使用")
        except UnicodeEncodeError:
            print("警告: Selenium不可用，每日推荐功能将无法使用")
        print("请安装依赖: pip install selenium -i https://pypi.tuna.tsinghua.edu.cn/simple/")
    
    print("\n🚀 启动HTTP服务器...")
    print("📖 API文档地址: http://localhost:8000/docs")
    print("🌐 服务器地址: http://localhost:8000")
    
    # 运行HTTP服务器
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
