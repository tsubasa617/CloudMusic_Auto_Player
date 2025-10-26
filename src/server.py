#!/usr/bin/env python3
"""
网易云音乐 MCP 控制器 - 重构版
支持 URL scheme 启动和全局快捷键控制
"""

import logging
from typing import Dict, Any
from fastmcp import FastMCP

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

# 创建MCP服务器实例
mcp = FastMCP("网易云音乐控制器")

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

def set_custom_playlists(playlists_dict):
    """设置用户自定义歌单（从客户端配置调用）"""
    global USER_CUSTOM_PLAYLISTS
    USER_CUSTOM_PLAYLISTS = playlists_dict or {}
    logger.info(f"已设置 {len(USER_CUSTOM_PLAYLISTS)} 个自定义歌单: {list(USER_CUSTOM_PLAYLISTS.keys())}")

# ============ MCP 工具定义 ============

@mcp.tool()
def launch_netease_music(minimize_window: bool = True) -> dict:
    """启动网易云音乐应用
    
    Args:
        minimize_window: 是否自动最小化窗口（默认True，避免弹窗干扰）
    """
    try:
        # 使用orpheus://直接启动
        scheme_url = music_controller.url_schemes["open"]
        
        # 启动应用
        success = music_controller.launch_by_url_scheme(scheme_url, minimize_window)
        
        if success:
            return {
                "success": True,
                "data": {
                    "scheme_url": scheme_url,
                    "minimized": minimize_window,
                    "platform": get_platform()
                },
                "message": "✅ 网易云音乐启动成功"
            }
        else:
            return {
                "success": False,
                "error": "网易云音乐启动失败"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"启动网易云音乐时出错: {str(e)}"
        }

@mcp.tool()
def control_playback(action: str = "play_pause") -> dict:
    """控制网易云音乐播放（全局快捷键）
    
    Args:
        action: 播放控制动作 - play_pause(播放/暂停), previous(上一首), next(下一首)
    """
    try:
        valid_actions = ["play_pause", "previous", "next"]
        if action not in valid_actions:
            return {
                "success": False,
                "error": f"无效的action参数: {action}，支持的值: {', '.join(valid_actions)}"
            }
        
        success = music_controller.send_global_hotkey(action)
        
        if success:
            return {
                "success": True,
                "data": {
                    "action": action,
                    "hotkey": music_controller.get_hotkey_for_action(action),
                    "platform": get_platform()
                },
                "message": f"✅ 播放控制成功 - {action}"
            }
        else:
            return {
                "success": False,
                "error": f"播放控制失败 - {action}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"播放控制时出错: {str(e)}"
        }

@mcp.tool()
def control_volume(action: str = "volume_up") -> dict:
    """控制网易云音乐音量（全局快捷键）
    
    Args:
        action: 音量控制动作 - volume_up(音量加), volume_down(音量减)
    """
    try:
        valid_actions = ["volume_up", "volume_down"]
        if action not in valid_actions:
            return {
                "success": False,
                "error": f"无效的action参数: {action}，支持的值: {', '.join(valid_actions)}"
            }
        
        success = music_controller.send_global_hotkey(action)
        
        if success:
            return {
                "success": True,
                "data": {
                    "action": action,
                    "hotkey": music_controller.get_hotkey_for_action(action),
                    "platform": get_platform()
                },
                "message": f"✅ 音量控制成功 - {action}"
            }
        else:
            return {
                "success": False,
                "error": f"音量控制失败 - {action}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"音量控制时出错: {str(e)}"
        }

@mcp.tool()
def toggle_mini_mode() -> dict:
    """切换网易云音乐迷你模式（全局快捷键）
    
    使用全局快捷键切换完整模式和迷你模式
    """
    try:
        success = music_controller.send_global_hotkey("mini_mode")
        
        if success:
            return {
                "success": True,
                "data": {
                    "action": "mini_mode",
                    "hotkey": music_controller.get_hotkey_for_action("mini_mode"),
                    "platform": get_platform()
                },
                "message": "✅ 迷你模式切换成功"
            }
        else:
            return {
                "success": False,
                "error": "迷你模式切换失败"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"迷你模式切换时出错: {str(e)}"
        }

@mcp.tool()
def like_current_song() -> dict:
    """喜欢当前播放的歌曲（全局快捷键）
    
    使用全局快捷键喜欢当前歌曲
    """
    try:
        success = music_controller.send_global_hotkey("like_song")
        
        if success:
            return {
                "success": True,
                "data": {
                    "action": "like_song",
                    "hotkey": music_controller.get_hotkey_for_action("like_song"),
                    "platform": get_platform()
                },
                "message": "✅ 歌曲喜欢操作成功"
            }
        else:
            return {
                "success": False,
                "error": "歌曲喜欢操作失败"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"歌曲喜欢操作时出错: {str(e)}"
        }

@mcp.tool()
def toggle_lyrics() -> dict:
    """打开/关闭歌词显示（全局快捷键）
    
    使用全局快捷键切换歌词显示
    """
    try:
        success = music_controller.send_global_hotkey("lyrics")
        
        if success:
            return {
                "success": True,
                "data": {
                    "action": "lyrics",
                    "hotkey": music_controller.get_hotkey_for_action("lyrics"),
                    "platform": get_platform()
                },
                "message": "✅ 歌词显示切换成功"
            }
        else:
            return {
                "success": False,
                "error": "歌词显示切换失败"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"歌词显示切换时出错: {str(e)}"
        }

@mcp.tool()
def manage_custom_playlists(action: str = "list", playlist_name: str = "", playlist_id: str = "", description: str = "") -> dict:
    """管理用户自定义歌单
    
    Args:
        action: 操作类型 - list(列出所有), add(添加), remove(删除)
        playlist_name: 歌单名称（用于add和remove操作）
        playlist_id: 歌单ID（用于add操作）
        description: 歌单描述（可选，用于add操作）
    """
    try:
        global USER_CUSTOM_PLAYLISTS
        
        if action == "list":
            # 获取完整的歌单数据
            playlists_data = load_playlists_from_file()
            
            return {
                "success": True,
                "data": {
                    "system_playlists": playlists_data.get("systemPlaylists", {}),
                    "user_playlists": playlists_data.get("userPlaylists", {}),
                    "total_system": len(playlists_data.get("systemPlaylists", {})),
                    "total_user": len(playlists_data.get("userPlaylists", {})),
                    "total_count": len(playlists_data.get("systemPlaylists", {})) + len(playlists_data.get("userPlaylists", {})),
                    "source": "playlists_file",
                    "platform": get_platform()
                },
                "message": f"✅ 系统歌单 {len(playlists_data.get('systemPlaylists', {}))} 个，用户歌单 {len(playlists_data.get('userPlaylists', {}))} 个"
            }
        
        elif action == "add":
            if not playlist_name or not playlist_id:
                return {
                    "success": False,
                    "error": "添加歌单需要提供歌单名称和歌单ID"
                }
            
            # 加载当前配置
            playlists_data = load_playlists_from_file()
            
            # 检查是否与系统歌单重名
            if playlist_name in playlists_data.get("systemPlaylists", {}):
                return {
                    "success": False,
                    "error": f"歌单名称 '{playlist_name}' 与系统预设歌单重名，请使用其他名称"
                }
            
            # 添加到用户歌单
            if "userPlaylists" not in playlists_data:
                playlists_data["userPlaylists"] = {}
            
            playlists_data["userPlaylists"][playlist_name] = {
                "id": playlist_id,
                "name": playlist_name,
                "description": description if description else f"用户自定义歌单: {playlist_name}"
            }
            
            # 保存到文件
            if save_playlists_to_file(playlists_data):
                logger.info(f"已将歌单添加到playlists.json: {playlist_name}")
                return {
                    "success": True,
                    "data": {
                        "playlist_name": playlist_name,
                        "playlist_id": playlist_id,
                        "description": description,
                        "storage": "playlists_file",
                        "platform": get_platform()
                    },
                    "message": f"✅ 成功添加用户歌单: {playlist_name} (ID: {playlist_id})"
                }
            else:
                return {
                    "success": False,
                    "error": "保存歌单配置失败"
                }
        
        elif action == "remove":
            if not playlist_name:
                return {
                    "success": False,
                    "error": "删除歌单需要提供歌单名称"
                }
            
            # 加载当前配置
            playlists_data = load_playlists_from_file()
            
            # 检查是否尝试删除系统歌单
            if playlist_name in playlists_data.get("systemPlaylists", {}):
                return {
                    "success": False,
                    "error": f"不能删除系统预设歌单: {playlist_name}"
                }
            
            # 检查用户歌单中是否存在
            if playlist_name not in playlists_data.get("userPlaylists", {}):
                return {
                    "success": False,
                    "error": f"未找到用户歌单: {playlist_name}"
                }
            
            # 获取要删除的歌单信息
            removed_playlist = playlists_data["userPlaylists"][playlist_name]
            removed_id = removed_playlist.get("id", "unknown")
            
            # 从用户歌单中删除
            del playlists_data["userPlaylists"][playlist_name]
            
            # 保存到文件
            if save_playlists_to_file(playlists_data):
                logger.info(f"已从playlists.json中删除歌单: {playlist_name}")
                return {
                    "success": True,
                    "data": {
                        "playlist_name": playlist_name,
                        "playlist_id": removed_id,
                        "storage": "playlists_file",
                        "platform": get_platform()
                    },
                    "message": f"✅ 成功删除用户歌单: {playlist_name} (ID: {removed_id})"
                }
            else:
                return {
                    "success": False,
                    "error": "保存歌单配置失败"
                }
        
        else:
            return {
                "success": False,
                "error": f"不支持的操作: {action}，支持的值: list, add, remove"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"管理自定义歌单时出错: {str(e)}"
        }

@mcp.tool()
def get_controller_info() -> dict:
    """获取控制器信息和支持的功能"""
    try:
        # 加载自定义歌单
        custom_playlists = load_custom_playlists()
        
        return {
            "success": True,
            "data": {
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
            "message": "✅ 控制器信息获取成功"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"获取控制器信息时出错: {str(e)}"
        }

@mcp.tool()
def search_and_play(query: str, minimize_window: bool = True) -> dict:
    """搜索歌曲并直接播放
    
    Args:
        query: 搜索关键词（歌曲名或歌曲名+歌手）
        minimize_window: 是否自动最小化网易云音乐窗口（默认True，避免弹窗干扰）
    """
    try:
        # 搜索歌曲
        song_id, song_name, artist_name = search_netease_music(query)
        
        if not song_id:
            return {
                "success": False,
                "error": f"未找到歌曲: {query}"
            }
        
        # 生成播放URL
        play_url = generate_play_url(song_id)
        
        if not play_url:
            return {
                "success": False,
                "error": "生成播放URL失败"
            }
        
        # 直接播放歌曲（带最小化选项）
        success = music_controller.launch_by_url_scheme(play_url, minimize_window)
        
        if success:
            return {
                "success": True,
                "data": {
                    "query": query,
                    "song_name": song_name,
                    "artist": artist_name,
                    "song_id": song_id,
                    "play_url": play_url,
                    "minimized": minimize_window,
                    "platform": get_platform()
                },
                "message": f"✅ 成功播放: 《{song_name}》- {artist_name}"
            }
        else:
            return {
                "success": False,
                "error": f"播放失败: 《{song_name}》- {artist_name}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"搜索播放歌曲时出错: {str(e)}"
        }

@mcp.tool()
def search_and_play_playlist(query: str = "", playlist_name: str = "", minimize_window: bool = True) -> dict:
    """搜索歌单并直接播放
    
    Args:
        query: 搜索关键词（歌单名称），为空时使用playlist_name参数
        playlist_name: 歌单名称 - 可以是系统预设榜单("飙升榜", "新歌榜", "热歌榜", "排行榜", "原创榜", "私人雷达")或用户自定义歌单名称
        minimize_window: 是否自动最小化网易云音乐窗口（默认True，避免弹窗干扰）
    """
    try:
        # 加载所有歌单配置
        all_playlists = load_custom_playlists()
        
        playlist_id = None
        playlist_name_result = None
        
        # 检查是否在配置的歌单中
        if playlist_name and playlist_name in all_playlists:
            playlist_id = all_playlists[playlist_name]
            playlist_name_result = playlist_name
            logger.info(f"✅ 使用配置歌单: {playlist_name_result} (ID: {playlist_id})")
        elif query:
            # 搜索歌单
            playlist_id, playlist_name_result = search_netease_playlist(query)
            if not playlist_id:
                return {
                    "success": False,
                    "error": f"未找到歌单: {query}"
                }
        else:
            return {
                "success": False,
                "error": "请提供搜索关键词(query)或常用歌单名称(playlist_name)"
            }
        
        # 生成播放URL
        play_url = generate_playlist_play_url(playlist_id)
        
        if not play_url:
            return {
                "success": False,
                "error": "生成歌单播放URL失败"
            }
        
        # 直接播放歌单（带最小化选项）
        success = music_controller.launch_by_url_scheme(play_url, minimize_window)
        
        if success:
            return {
                "success": True,
                "data": {
                    "query": query if query else playlist_name,
                    "playlist_name": playlist_name_result,
                    "playlist_id": playlist_id,
                    "play_url": play_url,
                    "minimized": minimize_window,
                    "platform": get_platform()
                },
                "message": f"✅ 成功播放歌单: 《{playlist_name_result}》"
            }
        else:
            return {
                "success": False,
                "error": f"播放歌单失败: 《{playlist_name_result}》"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"搜索播放歌单时出错: {str(e)}"
        }

# ============ 每日推荐相关 MCP 工具 ============



@mcp.tool()
def get_netease_config() -> dict:
    """
    获取网易云音乐配置信息
    
    Returns:
        dict: 当前配置信息
    """
    try:
        import os
        
        config = load_netease_config()
        
        # 检查路径状态
        netease_path = config.get("netease_music_path", "")
        path_status = "未配置"
        if netease_path:
            if os.path.exists(netease_path):
                path_status = "✅ 有效"
            else:
                path_status = "❌ 无效"
        
        # 获取项目根目录
        project_root = os.path.dirname(os.path.dirname(__file__))
        
        # 检查ChromeDriver状态
        chromedriver_path = os.path.join(
            project_root,
            config.get("chromedriver_path", "src/chromedriver/win64/chromedriver.exe")
        )
        chromedriver_status = "✅ 存在" if os.path.exists(chromedriver_path) else "❌ 不存在"
        
        return {
            "success": True,
            "config": {
                "netease_music_path": netease_path or "未配置",
                "path_status": path_status,
                "debug_port": config.get("debug_port", 9222),
                "chromedriver_path": config.get("chromedriver_path", "src/chromedriver/win64/chromedriver.exe"),
                "chromedriver_status": chromedriver_status,
                "selenium_available": SELENIUM_AVAILABLE,
                "platform": get_platform()
            },
            "ready_for_daily_recommend": (
                bool(netease_path) and 
                os.path.exists(netease_path) and 
                os.path.exists(chromedriver_path) and 
                SELENIUM_AVAILABLE
            )
        }
        
    except Exception as e:
        logger.error(f"获取配置失败: {e}")
        return {
            "success": False,
            "message": f"获取配置失败: {str(e)}"
        }

@mcp.tool()
def get_now_playing() -> dict:
    """
    获取当前正在播放的歌曲信息
    
    Returns:
        dict: 当前播放的歌曲信息
    """
    try:
        # 如果Selenium可用，尝试从每日推荐控制器获取
        if SELENIUM_AVAILABLE and _daily_controller.driver:
            try:
                # 连接网易云音乐
                if _daily_controller.connect_to_netease():
                    # 获取当前播放的音乐信息
                    current_music = _daily_controller.get_current_music()
                    is_playing = _daily_controller.is_playing()
                    
                    if current_music:
                        return {
                            "success": True,
                            "song_name": current_music,
                            "is_playing": is_playing,
                            "method": "selenium_driver",
                            "message": f"当前播放: {current_music}"
                        }
            except Exception as e:
                logger.debug(f"Selenium方式获取失败: {e}")
        
        # 方法2: 尝试从窗口标题获取（Windows）
        try:
            import win32gui
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
                return {
                    "success": True,
                    "song_name": title,
                    "is_playing": True,
                    "method": "window_title",
                    "message": f"从窗口标题获取: {title}"
                }
        except Exception as e:
            logger.debug(f"窗口标题方式获取失败: {e}")
        
        # 如果所有方法都失败
        return {
            "success": False,
            "song_name": None,
            "is_playing": None,
            "method": "none",
            "message": "无法获取当前播放信息",
            "hint": "可能需要先启动网易云音乐并播放歌曲"
        }
        
    except Exception as e:
        logger.error(f"获取当前播放信息失败: {e}")
        return {
            "success": False,
            "message": f"获取当前播放信息失败: {str(e)}"
        }

@mcp.tool()
def play_daily_recommend() -> dict:
    """
    播放网易云音乐每日推荐歌单
    
    使用预先验证的按钮路径，提供更高的成功率和更快的执行速度。
    注意: 此功能需要先设置环境变量 NETEASE_MUSIC_PATH 或在 netease_config.json 中配置网易云音乐客户端路径
    
    Returns:
        dict: 播放结果，包含success状态和详细信息
    """
    global _daily_controller
    
    try:
        # 检查Selenium可用性
        if not SELENIUM_AVAILABLE:
            return {
                "success": False,
                "message": "Selenium不可用",
                "solution": "请安装selenium: pip install selenium -i https://pypi.tuna.tsinghua.edu.cn/simple/"
            }
        
        # 检查配置
        config = load_netease_config()
        netease_path = config.get("netease_music_path", "")
        
        if not netease_path:
            return {
                "success": False,
                "message": "网易云音乐路径未配置",
                "solution": "请设置环境变量 NETEASE_MUSIC_PATH 或在 netease_config.json 中配置 netease_music_path"
            }
        
        import os
        if not os.path.exists(netease_path):
            return {
                "success": False,
                "message": f"网易云音乐路径无效: {netease_path}",
                "solution": "请重新设置环境变量 NETEASE_MUSIC_PATH 或在 netease_config.json 中配置正确的路径"
            }
        
        # 创建或重用控制器实例
        if not _daily_controller:
            _daily_controller = DailyRecommendController(config)
        
        logger.info("🎵 开始播放每日推荐（固定路径版本）...")
        
        # 连接到网易云音乐
        if not _daily_controller.connect_to_netease():
            return {
                "success": False,
                "message": "无法连接到网易云音乐",
                "details": [
                    "可能的原因:",
                    "1. 网易云音乐启动失败",
                    "2. ChromeDriver连接失败",
                    "3. 调试端口被占用"
                ]
            }
        
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
            return {
                "success": True,
                "message": "🎵 每日推荐播放成功（固定路径版本）！",
                "details": {
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
                "tips": [
                    "✅ 使用固定路径策略，播放操作成功执行",
                    "🎶 当前音乐: " + (current_music or "加载中..."),
                    "💡 此版本执行速度更快，成功率更高",
                    "🔧 如果没有声音，请检查网易云音乐客户端音量设置"
                ]
            }
        else:
            return {
                "success": False,
                "message": "播放每日推荐失败（固定路径版本）",
                "debug_info": {
                    "current_url": current_url,
                    "page_title": page_title,
                    "has_playlist": has_playlist,
                    "is_playing": is_playing,
                    "current_music": current_music,
                    "button_paths_info": button_paths_info,
                    "platform": get_platform()
                },
                "details": [
                    "可能的原因:",
                    "1. 网易云音乐界面已更新，固定路径失效",
                    "2. 网络连接问题 - 检查网络连接",
                    "3. ChromeDriver版本不兼容",
                    "4. 网易云音乐客户端版本过旧或过新"
                ],
                "suggestions": [
                    "🔧 排查步骤:",
                    "1. 重启网易云音乐客户端",
                    "2. 确保网易云音乐已登录",
                    "3. 尝试手动打开推荐页面",
                    "4. 如果固定路径失效，可以尝试使用 play_daily_recommend() 工具",
                    "5. 检查控制台日志获取详细错误信息"
                ]
            }
        
    except Exception as e:
        logger.error(f"播放每日推荐时出错: {e}")
        
        # 重置控制器
        if _daily_controller:
            _daily_controller.disconnect()
            _daily_controller = None
        
        return {
            "success": False,
            "message": f"播放失败: {str(e)}",
            "suggestion": "请重试或检查日志获取更多信息"
        }

@mcp.tool()
def play_roaming() -> dict:
    """
    启动网易云音乐私人漫游功能
    
    使用预先验证的按钮路径，提供更高的成功率和更快的执行速度。
    注意: 此功能需要先设置环境变量 NETEASE_MUSIC_PATH 或在 netease_config.json 中配置网易云音乐客户端路径
    
    Returns:
        dict: 漫游启动结果，包含success状态和详细信息
    """
    global _daily_controller
    
    try:
        # 检查Selenium可用性
        if not SELENIUM_AVAILABLE:
            return {
                "success": False,
                "message": "Selenium不可用",
                "solution": "请安装selenium: pip install selenium -i https://pypi.tuna.tsinghua.edu.cn/simple/"
            }
        
        # 检查配置
        config = load_netease_config()
        netease_path = config.get("netease_music_path", "")
        
        if not netease_path:
            return {
                "success": False,
                "message": "网易云音乐路径未配置",
                "solution": "请设置环境变量 NETEASE_MUSIC_PATH 或在 netease_config.json 中配置 netease_music_path"
            }
        
        import os
        if not os.path.exists(netease_path):
            return {
                "success": False,
                "message": f"网易云音乐路径无效: {netease_path}",
                "solution": "请重新设置环境变量 NETEASE_MUSIC_PATH 或在 netease_config.json 中配置正确的路径"
            }
        
        # 创建或重用控制器实例
        if not _daily_controller:
            _daily_controller = DailyRecommendController(config)
        
        logger.info("🌍 开始启动私人漫游...")
        
        # 连接到网易云音乐
        if not _daily_controller.connect_to_netease():
            return {
                "success": False,
                "message": "无法连接到网易云音乐",
                "details": [
                    "可能的原因:",
                    "1. 网易云音乐启动失败",
                    "2. ChromeDriver连接失败",
                    "3. 调试端口被占用"
                ]
            }
        
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
            return {
                "success": True,
                "message": "🌍 私人漫游启动成功！",
                "details": {
                    "roaming_status": "已启动",
                    "current_url": current_url,
                    "page_title": page_title,
                    "roaming_elements_found": roaming_elements_count,
                    "button_paths_used": roaming_paths_info,
                    "status": "漫游按钮点击操作已执行",
                    "platform": get_platform()
                },
                "tips": [
                    "✅ 使用验证过的按钮路径，漫游按钮点击成功",
                    "🌍 私人漫游功能已启动",
                    "💡 执行速度快，成功率高",
                    "🔧 如果漫游功能未生效，请检查网易云音乐VIP状态"
                ]
            }
        else:
            return {
                "success": False,
                "message": "启动私人漫游失败",
                "debug_info": {
                    "current_url": current_url,
                    "page_title": page_title,
                    "roaming_elements_found": roaming_elements_count,
                    "button_paths_info": roaming_paths_info,
                    "platform": get_platform()
                },
                "details": [
                    "可能的原因:",
                    "1. 网易云音乐界面已更新，按钮路径失效",
                    "2. 漫游按钮不可见或被禁用",
                    "3. 账户没有VIP权限或漫游权限",
                    "4. ChromeDriver版本不兼容"
                ],
                "suggestions": [
                    "🔧 排查步骤:",
                    "1. 确认网易云音乐账户具有VIP权限",
                    "2. 重启网易云音乐客户端并重新登录",
                    "3. 手动查看是否有漫游按钮可见",
                    "4. 检查网络连接是否正常",
                    "5. 检查控制台日志获取详细错误信息"
                ]
            }
        
    except Exception as e:
        logger.error(f"启动私人漫游时出错: {e}")
        
        # 重置控制器
        if _daily_controller:
            _daily_controller.disconnect()
            _daily_controller = None
        
        return {
            "success": False,
            "message": f"漫游启动失败: {str(e)}",
            "suggestion": "请重试或检查日志获取更多信息"
        }

# ============ MCP 服务器启动 ============

def main():
    """主函数"""
    try:
        print("🎵 网易云音乐 MCP 控制器 - 重构版")
    except UnicodeEncodeError:
        print("网易云音乐 MCP 控制器 - 重构版")
    
    print(f"当前平台: {get_platform()}")
    print("支持的功能:")
    print("- URL scheme 启动 (orpheus://)")
    print("- 全局快捷键控制")
    
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
    
    # 运行MCP服务器
    mcp.run()

if __name__ == "__main__":
    main()