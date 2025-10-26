# 🎵 网易云音乐控制器

一个强大的网易云音乐控制器，提供两种使用方式：
- **HTTP API 服务器**: 通过 HTTP 请求控制网易云音乐
- **MCP 服务器**: 基于 Model Context Protocol 的智能控制器

支持全局快捷键、搜索单曲播放、搜索歌单播放、自定义歌单管理、每日推荐和私人漫游等丰富功能。

## 🚀 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/xiduan/CloudMusic_Auto_Player.git
cd CloudMusic_Auto_Player

# 2. 安装依赖（使用国内源加速）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 3. 启动HTTP服务器
python start_http_server.py

# 4. 访问API文档
# 浏览器打开: http://localhost:8000/docs
```

## ✨ 主要特性

### 🎮 基础控制功能
- **启动网易云音乐**：支持 URL scheme 快速启动，可选自动最小化窗口
- **播放控制**：播放/暂停、上一首/下一首、音量调节
- **界面控制**：切换迷你模式、显示/隐藏歌词
- **互动功能**：一键喜欢当前歌曲

### 🎼 音乐搜索与播放
- **歌曲搜索播放**：直接搜索歌曲名或"歌曲名+歌手"组合播放
- **歌单搜索播放**：搜索并播放指定歌单
- **系统预设歌单**：快速播放飙升榜、新歌榜、热歌榜等官方榜单
- **私人雷达播放**：播放个性化推荐歌单

### 📋 歌单管理
- **自定义歌单管理**：添加、删除、列出用户自定义歌单
- **歌单配置文件**：支持通过 JSON 文件批量管理歌单
- **系统歌单集成**：内置官方热门榜单快速访问

### 🌟 高级功能
- **每日推荐播放**：自动播放网易云音乐每日推荐歌单
- **私人漫游**：启动网易云音乐私人漫游功能
- **全局快捷键**：支持全局快捷键控制，无需切换到音乐应用，支持按键自定义

### ⌨️ 全局快捷键支持

#### Windows 默认快捷键
- `Ctrl+Alt+P`：播放/暂停
- `Ctrl+Alt+Left`：上一首
- `Ctrl+Alt+Right`：下一首  
- `Ctrl+Alt+Up/Down`：音量加/减
- `Ctrl+Alt+M`：切换迷你模式
- `Ctrl+Alt+L`：喜欢当前歌曲
- `Ctrl+Alt+D`：显示/隐藏歌词

#### macOS 默认快捷键
- `command+option+P`：播放/暂停
- `command+option+Left`：上一首
- `command+option+Right`：下一首  
- `command+option+Up/Down`：音量加/减
- `command+option+M`：切换迷你模式
- `command+option+L`：喜欢当前歌曲
- `command+option+D`：显示/隐藏歌词

> 💡 可以在 `src/config/hotkeys.json` 的 `custom_hotkeys` 部分自定义快捷键

## 🔧 环境要求

### 通用要求
- **Python**：3.10+
- **网易云音乐客户端**：需安装并可正常运行
- **uv**：现代 Python 包管理器 ([安装指南](https://docs.astral.sh/uv/getting-started/installation/))

### 平台要求
- **Windows 10/11**：完整功能支持 ✅
  - 全局快捷键控制 ✅
  - 音乐搜索播放 ✅
  - 每日推荐功能 ✅
  - 私人漫游功能 ✅
  - 内置 ChromeDriver (Windows x64)
- **macOS 10.15+**：基础功能支持 ⚠️
  - 全局快捷键控制 ✅
  - 音乐搜索播放 ✅
  - 每日推荐功能 ❌ (不支持)
  - 私人漫游功能 ❌ (不支持)

## 📦 安装指南

### 🚀 快速部署（推荐）

#### Windows用户
```bash
# 下载项目后直接运行
deploy_windows.bat
```

#### macOS/Linux用户
```bash
# 下载项目后直接运行
chmod +x deploy_unix.sh
./deploy_unix.sh
```

#### 自动部署脚本
```bash
# 运行Python自动部署脚本
python deploy.py
```

### 手动安装

### 方法一：使用 uv（推荐）

#### 1. 安装 uv（如果尚未安装）
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 2. 克隆项目并安装依赖
```bash
git clone https://github.com/xiduan/CloudMusic_Auto_Player.git
cd CloudMusic_Auto_Player
uv sync
```

### 方法二：使用 pip

#### 1. 克隆项目
```bash
git clone https://github.com/xiduan/CloudMusic_Auto_Player.git
cd CloudMusic_Auto_Player
```

#### 2. 安装依赖

**Windows 用户：**
```bash
pip install fastapi uvicorn[standard] requests psutil pyautogui pywin32 selenium
```

**macOS/Linux 用户：**
```bash
pip install fastapi uvicorn[standard] requests psutil pyautogui selenium
```

**使用 requirements.txt（推荐）：**
```bash
# 自动处理平台差异
pip install -r requirements.txt
```

**注意：** macOS 用户不需要安装 `pywin32`，因为它是 Windows 专用的库。使用 `requirements.txt` 会自动处理平台差异。

#### 3. 可选：创建虚拟环境（推荐）
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 方法三：使用项目依赖文件

如果您有 `pyproject.toml` 文件，可以使用以下命令：

```bash
# 使用 pip 安装项目依赖
pip install -e .

# 或使用 uv
uv sync
```

### 3. macOS 说明
macOS 版本仅支持基础功能（全局快捷键控制、音乐搜索播放），不支持每日推荐和私人漫游功能。

### 主要依赖
- `fastapi>=0.104.0`：HTTP API 框架
- `uvicorn[standard]>=0.24.0`：ASGI 服务器
- `pyautogui>=0.9.54`：跨平台全局快捷键支持
- `pywin32>=306`：Windows 系统集成（仅 Windows）
- `psutil>=5.9.0`：进程管理
- `selenium>=4.0.0`：Web 自动化（每日推荐/漫游功能）
- `requests>=2.28.0`：HTTP 请求库

## 🚀 使用方法

### HTTP API 服务器（推荐）

#### 1. 启动服务器

**方法一：使用启动脚本（推荐）**
```bash
python start_http_server.py
```

**方法二：直接运行**
```bash
# 使用 uv（如果已安装）
uv run src/http_server.py

# 或直接使用 Python
python src/http_server.py
```

**方法三：使用 uvicorn**
```bash
# 基本启动
uvicorn src.http_server:app --host 0.0.0.0 --port 8000

# 开发模式（自动重载）
uvicorn src.http_server:app --host 0.0.0.0 --port 8000 --reload

# 指定日志级别
uvicorn src.http_server:app --host 0.0.0.0 --port 8000 --log-level debug
```

**方法四：使用启动脚本的高级选项**
```bash
# 指定端口
python start_http_server.py --port 8080

# 启用开发模式
python start_http_server.py --reload

# 指定日志级别
python start_http_server.py --log-level debug

# 查看帮助
python start_http_server.py --help
```

服务器启动后，访问以下地址：
- **API 文档**: http://localhost:8000/docs（离线版本，无需CDN）
- **ReDoc 文档**: http://localhost:8000/redoc（交互式文档）
- **离线文档**: http://localhost:8000/docs-offline（备用版本）
- **服务器地址**: http://localhost:8000

#### 2. API 使用示例

**Python 示例：**
```python
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
```

**curl 示例：**
```bash
# 启动网易云音乐
curl -X POST "http://localhost:8000/launch" \
     -H "Content-Type: application/json" \
     -d '{"minimize_window": true}'

# 播放控制
curl -X POST "http://localhost:8000/playback" \
     -H "Content-Type: application/json" \
     -d '{"action": "play_pause"}'
```

#### 3. 支持的 API 端点

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/` | 获取 API 基本信息 |
| POST | `/launch` | 启动网易云音乐 |
| POST | `/playback` | 播放控制 |
| POST | `/volume` | 音量控制 |
| POST | `/search-play` | 搜索并播放歌曲 |
| POST | `/playlist-play` | 播放歌单 |
| POST | `/daily-recommend` | 播放每日推荐 |
| POST | `/roaming` | 启动私人漫游 |
| POST | `/playlist-manage` | 管理歌单 |
| GET | `/info` | 获取控制器信息 |
| GET | `/config` | 获取配置信息 |

详细的 API 文档请参考 [HTTP_API_DOCS.md](HTTP_API_DOCS.md)

## 🚀 部署到其他电脑

### 快速部署

1. **下载项目**：
   ```bash
   git clone https://github.com/xiduan/CloudMusic_Auto_Player.git
   cd CloudMusic_Auto_Player
   ```

2. **运行部署脚本**：
   ```bash
   # Windows
   deploy_windows.bat
   
   # macOS/Linux
   chmod +x deploy_unix.sh
   ./deploy_unix.sh
   
   # 或使用Python脚本
   python deploy.py
   ```

3. **访问服务**：
   - API文档: http://localhost:8000/docs
   - 服务器: http://localhost:8000

### 详细部署指南

完整的部署指南请参考 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

### MCP 服务器（传统方式）

## ⚙️ 配置说明

### 1. MCP 客户端配置

在你的 MCP 客户端配置文件中添加以下配置：

#### 方式一：使用 uvx（推荐）

直接使用已发布的 PyPI 包，无需下载源码：

```json
{
  "mcpServers": {
    "cloudmusic-auto-player": {
      "command": "uvx",
      "args": ["cloudmusic-auto-player==1.0.2"],
      "env": {
        "NETEASE_MUSIC_PATH": "C:\\Program Files (x86)\\Netease\\CloudMusic\\cloudmusic.exe",
        "CHROMEDRIVER_PATH": "C:\\path\\to\\chromedriver.exe"
      }
    }
  }
}
```

**平台特定配置示例：**

**Windows 配置：**
```json
{
  "mcpServers": {
    "cloudmusic-auto-player": {
      "command": "uvx",
      "args": ["cloudmusic-auto-player==1.0.2"],
      "env": {
        "NETEASE_MUSIC_PATH": "C:\\Program Files (x86)\\Netease\\CloudMusic\\cloudmusic.exe",
        "CHROMEDRIVER_PATH": "C:\\path\\to\\chromedriver.exe"
      }
    }
  }
}
```

**macOS 配置：**
```json
{
  "mcpServers": {
    "cloudmusic-auto-player": {
      "command": "uvx",
      "args": ["cloudmusic-auto-player==1.0.2"],
      "env": {
        "NETEASE_MUSIC_PATH": "/Applications/NeteaseMusic.app/Contents/MacOS/NeteaseMusic"
      }
    }
  }
}
```

> 📝 **注意**：macOS 不支持每日推荐和私人漫游功能，因此无需配置 `CHROMEDRIVER_PATH`

#### 方式二：本地项目运行

如果你需要修改源码或本地开发，可以下载项目后使用：

```json
{
  "mcpServers": {
    "auto-music-player": {
      "command": "uv",
      "args": [
        "run",
        "--project",
        "/path/to/CloudMusic_Auto_Player",
        "src/server.py"
      ],
      "cwd": "/path/to/CloudMusic_Auto_Player",
      "env": {
        "NETEASE_MUSIC_PATH": "/path/to/netease/music/executable",
        "CHROMEDRIVER_PATH": "/path/to/chromedriver"
      }
    }
  }
}
```

**Windows 本地项目示例：**
```json
{
  "mcpServers": {
    "auto-music-player": {
      "command": "uv",
      "args": [
        "run",
        "--project", 
        "C:\\Users\\YourName\\CloudMusic_Auto_Player",
        "src/server.py"
      ],
      "cwd": "C:\\Users\\YourName\\CloudMusic_Auto_Player",
      "env": {
        "NETEASE_MUSIC_PATH": "C:\\Program Files (x86)\\Netease\\CloudMusic\\cloudmusic.exe",
        "CHROMEDRIVER_PATH": "C:\\Users\\YourName\\CloudMusic_Auto_Player\\src\\chromedriver\\win64\\chromedriver.exe"
      }
    }
  }
}
```

**macOS 本地项目示例：**
```json
{
  "mcpServers": {
    "auto-music-player": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "/Users/YourName/CloudMusic_Auto_Player/src/server.py"
      ],
      "cwd": "/Users/YourName/CloudMusic_Auto_Player",
      "env": {
        "NETEASE_MUSIC_PATH": "/Applications/NeteaseMusic.app/Contents/MacOS/NeteaseMusic"
      }
    }
  }
}
```

> ⚠️ **重要提示**：
> - 请将路径替换为你的实际路径
> - Windows 路径中的反斜杠需要转义为 `\\`
> - macOS 不支持每日推荐和私人漫游功能
> - 配置完成后，建议调用 `get_netease_config()` 工具验证环境变量配置是否正确


### 2. 网易云音乐全局快捷键设置

**重要：** 为了使用快捷键控制功能，需要在网易云音乐客户端中启用全局快捷键。

#### Windows 设置步骤：
1. 打开网易云音乐客户端
2. 点击右上角 **设置** 按钮（齿轮图标）
3. 选择 **快捷键** 选项卡
4. 确保 **启用全局快捷键** 选项已勾选
5. 检查以下快捷键是否与项目配置一致：
   - 播放/暂停：`Ctrl+Alt+P`
   - 上一首：`Ctrl+Alt+Left`
   - 下一首：`Ctrl+Alt+Right`
   - 音量加：`Ctrl+Alt+Up`
   - 音量减：`Ctrl+Alt+Down`
   - 迷你模式：`Ctrl+Alt+M`
   - 喜欢歌曲：`Ctrl+Alt+L`
   - 歌词显示：`Ctrl+Alt+D`

#### macOS 设置步骤：
1. 打开网易云音乐客户端
2. 点击菜单栏 **网易云音乐** → **偏好设置**
3. 选择 **快捷键** 选项卡
4. 确保 **启用全局快捷键** 选项已勾选
5. 检查快捷键配置是否与项目一致

> ⚠️ **注意**：如果快捷键没有效果，请确保：
> - 网易云音乐客户端正在运行
> - 全局快捷键功能已启用
> - 没有其他程序占用相同的快捷键
> - 系统允许网易云音乐使用辅助功能权限

### 3. 自定义歌单配置

#### 上传自定义歌单
可调用mcp上传自定义歌单，只需要输入歌单名称和歌单id即可（如有对歌单描述可添加）（推荐）
编辑项目根目录下的 `playlists.json` 文件：

```json
{
  "systemPlaylists": {
    "飙升榜": {"id": "19723756", "name": "音乐飙升榜", "description": "网易云音乐官方飙升榜"},
    "新歌榜": {"id": "3779629", "name": "音乐新歌榜", "description": "网易云音乐官方新歌榜"},
    "热歌榜": {"id": "3778678", "name": "音乐热歌榜", "description": "网易云音乐官方热歌榜"}
  },
  "userPlaylists": {
    "我的收藏": {"id": "123456789", "name": "我的收藏歌单", "description": "个人收藏"},
    "工作音乐": {"id": "987654321", "name": "工作专用歌单", "description": "适合工作时听的音乐"}
  }
}
```

**获取歌单 ID 的方法：**

#### 方法一：通过网易云音乐网页版（推荐）
1. 打开网易云音乐网页版：https://music.163.com
2. 登录您的账号
3. 找到您的歌单（如"我喜欢的音乐"、"我的收藏"等）
4. 点击歌单，查看浏览器地址栏的URL
5. 从URL中提取歌单ID

**示例：**
- URL：`https://music.163.com/#/playlist?id=123456789`
- 歌单ID：`123456789`

#### 方法二：通过网易云音乐客户端
1. 打开网易云音乐客户端
2. 找到您的歌单
3. 右键点击歌单 → 复制链接
4. 从链接中提取歌单ID

#### 方法三：通过歌单分享链接
1. 在网易云音乐中找到您的歌单
2. 点击分享按钮
3. 复制分享链接
4. 从链接中提取歌单ID

**重要提示：**
- 确保获取的是您自己账号的歌单ID，不是其他人的歌单
- 歌单ID必须是纯数字
- 每个用户的歌单ID都是唯一的

## 🚀 使用方法
"""以下方法均推荐使用自然语言从agent调用mcp工具实现"""

### 基础播放控制

```python
# 启动网易云音乐
launch_netease_music(minimize_window=True)

# 播放控制
control_playback(action="play_pause")  # 播放/暂停
control_playback(action="next")        # 下一首
control_playback(action="previous")    # 上一首

# 音量控制
control_volume(action="volume_up")     # 音量加
control_volume(action="volume_down")   # 音量减

# 界面控制
toggle_mini_mode()  # 切换迷你模式
toggle_lyrics()     # 切换歌词显示
like_current_song() # 喜欢当前歌曲
```

### 音乐搜索与播放

```python
# 搜索并播放歌曲
search_and_play(query="稻香 周杰伦", minimize_window=True)

# 播放预设歌单
search_and_play_playlist(playlist_name="飙升榜", minimize_window=True)

# 播放自定义歌单
search_and_play_playlist(playlist_name="我的收藏", minimize_window=True)
```

### 高级功能

```python
# 播放每日推荐（需要先配置网易云音乐路径）
play_daily_recommend()

# 启动私人漫游（需要先配置网易云音乐路径）
play_roaming()

# 获取控制器信息和功能列表
get_controller_info()

# 获取当前配置（验证环境变量配置）
get_netease_config()
```

### 🔍 配置验证

配置完成后，强烈建议使用以下工具验证配置是否正确：

```python
# 验证环境变量和路径配置
get_netease_config()
```

该工具会返回：
- 当前网易云音乐路径配置状态
- ChromeDriver路径配置状态  
- 各路径文件是否存在
- 是否满足每日推荐功能的运行条件

**示例输出：**
```json
{
  "success": true,
  "config": {
    "netease_music_path": "你配置的网易云音乐路径",
    "path_status": "✅ 有效",
    "chromedriver_path": "你配置的chromedriver路径",
    "chromedriver_status": "✅ 存在",
    "platform": "windows"
  },
  "ready_for_daily_recommend": true
}
```

### 歌单管理

```python
# 列出所有歌单
manage_custom_playlists(action="list")

# 添加新歌单
manage_custom_playlists(
    action="add", 
    playlist_name="新歌单", 
    playlist_id="123456789", 
    description="歌单描述"
)

# 删除歌单
manage_custom_playlists(action="remove", playlist_name="旧歌单")
```

## ⚠️ 注意事项

### 重要提醒
1. **平台功能差异**：macOS 仅支持基础功能，不支持每日推荐和私人漫游
2. **网易云音乐路径配置**：Windows 用户使用每日推荐和私人漫游功能前，需要配置网易云音乐客户端路径（通过环境变量 `NETEASE_MUSIC_PATH` 设置）
3. **ChromeDriver要求**：Windows 每日推荐和漫游功能需要 ChromeDriver，项目已包含 Windows 版本
4. **VIP功能限制**：私人漫游功能可能需要网易云音乐 VIP 会员
5. **网络连接**：搜索和播放功能需要稳定的网络连接
6. **配置验证**：配置完成后，建议调用 `get_netease_config()` 工具验证环境变量配置是否正确

### 故障排除

#### 安装问题

**1. pip 安装失败**
```bash
# 升级 pip
python -m pip install --upgrade pip

# 使用国内镜像源（推荐）
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple fastapi uvicorn requests psutil pyautogui pywin32 selenium
```

**2. pywin32 安装失败（Windows）**
```bash
# 先安装 Microsoft Visual C++ Build Tools
# 然后重新安装
pip install pywin32
```

**3. 权限问题（macOS/Linux）**
```bash
# 使用 --user 参数安装到用户目录（推荐使用国内源）
pip install --user -i https://pypi.tuna.tsinghua.edu.cn/simple fastapi uvicorn requests psutil pyautogui selenium
```

#### 运行问题

**1. 服务器启动失败**
- 检查端口8000是否被占用：`netstat -an | findstr 8000`（Windows）或 `lsof -i :8000`（macOS/Linux）
- 尝试使用其他端口：`python start_http_server.py --port 8080`
- 检查Python版本：确保使用Python 3.10+

**2. 模块导入错误**
```bash
# 检查依赖是否正确安装
python -c "import fastapi, uvicorn, requests, psutil, pyautogui; print('所有依赖已安装')"

# 如果使用虚拟环境，确保已激活
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

**3. 快捷键不响应**
- 确保已安装 `pyautogui`
- 检查是否有其他程序占用快捷键
- Windows用户可能需要以管理员权限运行

**4. 网易云音乐启动失败**
- 检查URL scheme是否正确注册
- 尝试重新安装网易云音乐
- 确认网易云音乐客户端路径正确

**5. 每日推荐无法播放**
- 确认网易云音乐路径配置正确
- 检查是否已登录账户
- 确保ChromeDriver版本兼容

**6. 搜索功能异常**
- 检查网络连接
- 确认网易云音乐API可正常访问
- 检查防火墙设置

**7. API文档白屏或无法加载**
- 现在使用离线版本，无需CDN资源
- 如果仍有问题，尝试访问ReDoc：http://localhost:8000/redoc
- 或访问备用文档：http://localhost:8000/docs-offline
- 清除浏览器缓存后重试

#### 常见错误信息

**ModuleNotFoundError**
```bash
# 解决方案：安装缺失的模块
pip install [模块名]
```

**PermissionError**
```bash
# 解决方案：使用管理员权限运行（Windows）或sudo（macOS/Linux）
```

**Port already in use**
```bash
# 解决方案：使用其他端口或关闭占用端口的程序
python start_http_server.py --port 8080
```

### 兼容性说明

#### 支持的操作系统
- **Windows 10/11**：完整功能支持 ✅
  - 全局快捷键控制 ✅
  - 音乐搜索播放 ✅
  - 每日推荐功能 ✅
  - 私人漫游功能 ✅
  - 内置 ChromeDriver ✅

- **macOS 10.15+**：基础功能支持 ⚠️
  - 全局快捷键控制 ✅
  - 音乐搜索播放 ✅
  - 每日推荐功能 ❌ (不支持)
  - 私人漫游功能 ❌ (不支持)

#### 客户端要求
- 需要网易云音乐桌面客户端（不支持 UWP 版本）
- 建议使用最新版本的网易云音乐客户端以获得最佳兼容性
- macOS 用户推荐从官方网站下载桌面版本

## 📁 项目结构

```
auto_music/
├── src/
│   ├── server.py              # MCP 服务器主程序
│   └── chromedriver/          # ChromeDriver 文件
│       └── win64/
├── config.json                # MCP 客户端配置示例
├── netease_config.json        # 网易云音乐配置文件
├── playlists.json             # 歌单配置文件
└── README.md                  # 项目文档
```

## 🤝 技术支持

- **项目仓库**：https://github.com/SpongeBaby-124/CloudMusic_Auto_Player
- **问题反馈**：请在 GitHub Issues 中提交
- **联系邮箱**：lxd4094@foxmail.com

## 📄 许可证

本项目采用 MIT 许可证开源。

## 🔄 更新日志

### v1.0.2
- ✅ 添加uvx配置方式

---

**享受音乐，让控制更简单！** 🎵
