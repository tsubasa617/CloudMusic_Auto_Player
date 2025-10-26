# 🚀 网易云音乐HTTP服务器快速启动指南

## 📋 前置要求

1. **Python 3.10+**
2. **网易云音乐桌面客户端**（已安装并可正常运行）
3. **网络连接**（用于搜索和播放功能）

## 🔧 安装依赖

### 方法一：使用pip（推荐）

```bash
pip install fastapi uvicorn requests psutil pyautogui pywin32 selenium
```

### 方法二：使用项目依赖文件

```bash
# 如果有uv
uv sync

# 或使用pip安装项目依赖
pip install -e .
```

## 🚀 启动服务器

### 方法一：使用启动脚本（推荐）

```bash
python start_http_server.py
```

### 方法二：直接运行

```bash
python src/http_server.py
```

### 方法三：使用uvicorn

```bash
uvicorn src.http_server:app --host 0.0.0.0 --port 8000
```

## 🌐 访问服务

服务器启动后，您可以通过以下地址访问：

- **API文档**: http://localhost:8000/docs
- **ReDoc文档**: http://localhost:8000/redoc  
- **服务器根路径**: http://localhost:8000

## 🧪 测试功能

运行测试脚本验证功能：

```bash
python test_http_server.py
```

运行使用示例：

```bash
python example_usage.py
```

## 📖 API使用示例

### Python示例

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
```

### curl示例

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

## ⚙️ 配置说明

### 环境变量（可选）

设置网易云音乐路径以启用高级功能：

**Windows:**
```bash
set NETEASE_MUSIC_PATH=C:\Program Files (x86)\Netease\CloudMusic\cloudmusic.exe
```

**macOS/Linux:**
```bash
export NETEASE_MUSIC_PATH=/Applications/NeteaseMusic.app/Contents/MacOS/NeteaseMusic
```

### 配置文件

- `netease_config.json`: 网易云音乐配置
- `playlists.json`: 歌单配置
- `src/config/hotkeys.json`: 快捷键配置

## 🎯 支持的功能

### 基础控制
- ✅ 启动网易云音乐
- ✅ 播放/暂停控制
- ✅ 上一首/下一首
- ✅ 音量调节
- ✅ 迷你模式切换
- ✅ 歌词显示切换
- ✅ 喜欢歌曲

### 音乐播放
- ✅ 搜索并播放歌曲
- ✅ 播放预设歌单（飙升榜、新歌榜等）
- ✅ 播放自定义歌单
- ✅ 每日推荐播放（需要配置）
- ✅ 私人漫游（需要VIP）

### 歌单管理
- ✅ 列出所有歌单
- ✅ 添加自定义歌单
- ✅ 删除自定义歌单

## ⚠️ 注意事项

1. **平台支持**：
   - Windows: 完整功能支持
   - macOS: 基础功能支持（不支持每日推荐和私人漫游）

2. **权限要求**：
   - 全局快捷键功能需要系统权限
   - 私人漫游功能需要网易云音乐VIP会员

3. **网络要求**：
   - 搜索和播放功能需要稳定的网络连接

## 🐛 故障排除

### 常见问题

1. **服务器启动失败**
   - 检查端口8000是否被占用
   - 确认所有依赖已正确安装

2. **快捷键不响应**
   - 确保已安装pyautogui
   - 检查是否有其他程序占用快捷键

3. **网易云音乐启动失败**
   - 检查URL scheme是否正确注册
   - 尝试重新安装网易云音乐

4. **API请求失败**
   - 检查服务器是否正在运行
   - 确认请求格式是否正确

## 📞 技术支持

- **项目仓库**: https://github.com/xiduan/CloudMusic_Auto_Player
- **问题反馈**: 请在GitHub Issues中提交
- **联系邮箱**: lxd4094@foxmail.com

---

**享受音乐，让控制更简单！** 🎵
