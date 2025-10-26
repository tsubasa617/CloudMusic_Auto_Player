# 🎵 网易云音乐 HTTP 控制器 API 文档

## 概述

网易云音乐 HTTP 控制器提供了一套完整的 HTTP API 接口，让您可以通过 HTTP 请求来控制网易云音乐的各种功能。

## 🚀 快速开始

### 1. 安装依赖

```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip（使用国内源）
pip install fastapi uvicorn pyautogui pywin32 psutil selenium requests -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 2. 启动服务器

```bash
# 使用 uv 运行
uv run src/http_server.py

# 或直接运行
python src/http_server.py
```

服务器将在 `http://localhost:8000` 启动。

### 3. 访问 API 文档

启动服务器后，访问以下地址查看交互式 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📋 API 端点列表

### 基础信息

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/` | 获取 API 基本信息 |
| GET | `/info` | 获取控制器信息 |
| GET | `/config` | 获取配置信息 |
| GET | `/now-playing` | 获取当前播放的歌曲信息 |

### 应用控制

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/launch` | 启动网易云音乐 |
| POST | `/playback` | 播放控制（播放/暂停/上一首/下一首） |
| POST | `/volume` | 音量控制（音量加/减） |
| POST | `/mini-mode` | 切换迷你模式 |
| POST | `/like` | 喜欢当前歌曲 |
| POST | `/lyrics` | 切换歌词显示 |

### 音乐播放

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/search-play` | 搜索并播放歌曲 |
| POST | `/playlist-play` | 播放歌单 |
| POST | `/daily-recommend` | 播放每日推荐 |
| POST | `/roaming` | 启动私人漫游 |

### 歌单管理

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/playlist-manage` | 管理自定义歌单（添加/删除/列出） |

## 📖 详细 API 说明

### 1. 启动网易云音乐

**POST** `/launch`

**请求体：**
```json
{
  "minimize_window": true
}
```

**响应示例：**
```json
{
  "success": true,
  "data": {
    "scheme_url": "orpheus://",
    "minimized": true,
    "platform": "windows"
  },
  "message": "✅ 网易云音乐启动成功"
}
```

### 2. 播放控制

**POST** `/playback`

**请求体：**
```json
{
  "action": "play_pause"
}
```

**支持的 action 值：**
- `play_pause`: 播放/暂停
- `previous`: 上一首
- `next`: 下一首

**响应示例：**
```json
{
  "success": true,
  "data": {
    "action": "play_pause",
    "hotkey": "ctrl+alt+p",
    "platform": "windows"
  },
  "message": "✅ 播放控制成功 - play_pause"
}
```

### 3. 音量控制

**POST** `/volume`

**请求体：**
```json
{
  "action": "volume_up"
}
```

**支持的 action 值：**
- `volume_up`: 音量加
- `volume_down`: 音量减

### 4. 获取当前播放信息

**GET** `/now-playing`

获取当前正在播放的歌曲信息，支持两种方式：
- Selenium 方式：通过浏览器自动化获取准确的歌曲信息
- 窗口标题方式：从网易云音乐窗口标题获取信息（Windows）

**响应示例（成功）：**
```json
{
  "success": true,
  "data": {
    "song_name": "稻香 - 周杰伦",
    "is_playing": true,
    "method": "window_title"
  },
  "message": "[OK] 从窗口标题获取: 稻香 - 周杰伦"
}
```

**响应示例（失败）：**
```json
{
  "success": false,
  "data": {
    "song_name": null,
    "is_playing": null,
    "method": "none"
  },
  "message": "无法获取当前播放信息",
  "error": "可能需要先启动网易云音乐并播放歌曲"
}
```

**注意：**
- 此接口需要网易云音乐正在运行并播放歌曲
- Windows 系统优先使用窗口标题方式，无需额外配置
- 如需更准确的信息，建议先启动每日推荐功能以初始化 Selenium 控制器

### 5. 搜索并播放歌曲

**POST** `/search-play`

**请求体：**
```json
{
  "query": "稻香 周杰伦",
  "minimize_window": true
}
```

**响应示例：**
```json
{
  "success": true,
  "data": {
    "query": "稻香 周杰伦",
    "song_name": "稻香",
    "artist": "周杰伦",
    "song_id": "185008",
    "play_url": "orpheus://song/185008",
    "minimized": true,
    "platform": "windows"
  },
  "message": "✅ 成功播放: 《稻香》- 周杰伦"
}
```

### 6. 播放歌单

**POST** `/playlist-play`

**请求体：**
```json
{
  "query": "",
  "playlist_name": "飙升榜",
  "minimize_window": true
}
```

**支持的预设歌单：**
- `飙升榜`: 音乐飙升榜
- `新歌榜`: 音乐新歌榜
- `热歌榜`: 音乐热歌榜
- `排行榜`: 音乐排行榜
- `原创榜`: 原创音乐榜
- `私人雷达`: 私人雷达

### 7. 歌单管理

**POST** `/playlist-manage`

#### 列出所有歌单

**请求体：**
```json
{
  "action": "list"
}
```

#### 添加歌单

**请求体：**
```json
{
  "action": "add",
  "playlist_name": "我的收藏",
  "playlist_id": "123456789",
  "description": "个人收藏歌单"
}
```

#### 删除歌单

**请求体：**
```json
{
  "action": "remove",
  "playlist_name": "我的收藏"
}
```

### 8. 每日推荐

**POST** `/daily-recommend`

无需请求体，直接调用即可播放每日推荐歌单。

**注意：** 此功能需要先配置网易云音乐路径。

### 9. 私人漫游

**POST** `/roaming`

无需请求体，直接调用即可启动私人漫游功能。

**注意：** 此功能需要网易云音乐 VIP 会员。

## 🔧 配置说明

### 环境变量配置

在启动服务器前，建议设置以下环境变量：

**Windows：**
```bash
set NETEASE_MUSIC_PATH=C:\Program Files (x86)\Netease\CloudMusic\cloudmusic.exe
set CHROMEDRIVER_PATH=C:\path\to\chromedriver.exe
```

**macOS/Linux：**
```bash
export NETEASE_MUSIC_PATH=/Applications/NeteaseMusic.app/Contents/MacOS/NeteaseMusic
```

### 配置文件

项目支持通过配置文件进行设置：

1. **netease_config.json**: 网易云音乐配置
2. **playlists.json**: 歌单配置
3. **src/config/hotkeys.json**: 快捷键配置

## 🌐 使用示例

### Python 示例

```python
import requests

# 启动网易云音乐
response = requests.post("http://localhost:8000/launch", 
                        json={"minimize_window": True})
print(response.json())

# 播放控制
response = requests.post("http://localhost:8000/playback", 
                        json={"action": "play_pause"})
print(response.json())

# 搜索并播放歌曲
response = requests.post("http://localhost:8000/search-play", 
                        json={"query": "稻香 周杰伦"})
print(response.json())

# 播放歌单
response = requests.post("http://localhost:8000/playlist-play", 
                        json={"playlist_name": "飙升榜"})
print(response.json())
```

### JavaScript 示例

```javascript
// 启动网易云音乐
fetch('http://localhost:8000/launch', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        minimize_window: true
    })
})
.then(response => response.json())
.then(data => console.log(data));

// 播放控制
fetch('http://localhost:8000/playback', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        action: 'play_pause'
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

### curl 示例

```bash
# 启动网易云音乐
curl -X POST "http://localhost:8000/launch" \
     -H "Content-Type: application/json" \
     -d '{"minimize_window": true}'

# 播放控制
curl -X POST "http://localhost:8000/playback" \
     -H "Content-Type: application/json" \
     -d '{"action": "play_pause"}'

# 搜索并播放歌曲
curl -X POST "http://localhost:8000/search-play" \
     -H "Content-Type: application/json" \
     -d '{"query": "稻香 周杰伦"}'

# 播放歌单
curl -X POST "http://localhost:8000/playlist-play" \
     -H "Content-Type: application/json" \
     -d '{"playlist_name": "飙升榜"}'
```

## ⚠️ 注意事项

1. **平台支持**：
   - Windows: 完整功能支持
   - macOS: 基础功能支持（不支持每日推荐和私人漫游）

2. **依赖要求**：
   - 需要安装网易云音乐桌面客户端
   - 每日推荐和私人漫游功能需要 Selenium 和 ChromeDriver

3. **权限要求**：
   - 私人漫游功能需要网易云音乐 VIP 会员
   - 全局快捷键功能需要相应的系统权限

4. **网络要求**：
   - 搜索和播放功能需要稳定的网络连接

## 🐛 故障排除

### 常见问题

1. **快捷键不响应**
   - 确保已安装 `pyautogui`
   - 检查是否有其他程序占用快捷键

2. **网易云音乐启动失败**
   - 检查 URL scheme 是否正确注册
   - 尝试重新安装网易云音乐

3. **每日推荐无法播放**
   - 确认网易云音乐路径配置正确
   - 检查是否已登录账户
   - 确保 ChromeDriver 版本兼容

4. **API 请求失败**
   - 检查服务器是否正在运行
   - 确认请求格式是否正确
   - 查看服务器日志获取详细错误信息

## 📞 技术支持

- **项目仓库**: https://github.com/xiduan/CloudMusic_Auto_Player
- **问题反馈**: 请在 GitHub Issues 中提交
- **联系邮箱**: lxd4094@foxmail.com

## 📄 许可证

本项目采用 MIT 许可证开源。

---

**享受音乐，让控制更简单！** 🎵
