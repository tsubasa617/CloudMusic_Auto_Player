# 🔧 网易云音乐控制器路径配置指南

## 📋 需要配置的路径

### 1. 网易云音乐客户端路径
**用途**：每日推荐和私人漫游功能
**必需**：是（如果要使用高级功能）

### 2. ChromeDriver路径
**用途**：Web自动化功能
**必需**：否（项目已包含Windows版本）

## 🎯 配置方法

### 方法一：环境变量配置（推荐）

#### Windows用户
```bash
# 设置网易云音乐路径
set NETEASE_MUSIC_PATH=C:\Program Files (x86)\Netease\CloudMusic\cloudmusic.exe

# 设置ChromeDriver路径（可选）
set CHROMEDRIVER_PATH=C:\Users\34360\Desktop\CloudMusic_Auto_Player-master\src\chromedriver\win64\chromedriver.exe
```

#### macOS/Linux用户
```bash
# 设置网易云音乐路径
export NETEASE_MUSIC_PATH="/Applications/NeteaseMusic.app/Contents/MacOS/NeteaseMusic"
```

### 方法二：修改配置文件

编辑 `netease_config.json` 文件：

**Windows示例：**
```json
{
  "netease_music_path": "C:\\Program Files (x86)\\Netease\\CloudMusic\\cloudmusic.exe",
  "debug_port": 9222,
  "chromedriver_path": "src/chromedriver/win64/chromedriver.exe"
}
```

**macOS示例：**
```json
{
  "netease_music_path": "/Applications/NeteaseMusic.app/Contents/MacOS/NeteaseMusic",
  "debug_port": 9222,
  "chromedriver_path": "/opt/homebrew/bin/chromedriver"
}
```

## 🔍 如何找到网易云音乐安装路径

### Windows常见路径：
1. `C:\Program Files (x86)\Netease\CloudMusic\cloudmusic.exe`
2. `C:\Program Files\Netease\CloudMusic\cloudmusic.exe`
3. `C:\Users\{用户名}\AppData\Local\NetEase\CloudMusic\cloudmusic.exe`

### macOS常见路径：
1. `/Applications/NeteaseMusic.app/Contents/MacOS/NeteaseMusic`
2. `/Applications/网易云音乐.app/Contents/MacOS/网易云音乐`

### 查找方法：

#### Windows：
```bash
# 方法1：搜索文件
dir /s C:\ cloudmusic.exe

# 方法2：使用PowerShell
Get-ChildItem -Path C:\ -Recurse -Name "cloudmusic.exe" -ErrorAction SilentlyContinue

# 方法3：检查注册表
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" /s /f "NetEase"
```

#### macOS：
```bash
# 查找网易云音乐
find /Applications -name "*Netease*" -o -name "*网易云*"
```

## ✅ 验证配置

### 1. 检查路径是否存在
```bash
# Windows
dir "C:\Program Files (x86)\Netease\CloudMusic\cloudmusic.exe"

# macOS
ls -la "/Applications/NeteaseMusic.app/Contents/MacOS/NeteaseMusic"
```

### 2. 使用API验证配置
启动服务器后，访问：
```
GET http://localhost:8000/config
```

### 3. 测试功能
```bash
# 测试每日推荐功能
curl -X POST "http://localhost:8000/daily-recommend"
```

## ⚠️ 注意事项

1. **路径格式**：
   - Windows：使用双反斜杠 `\\` 或正斜杠 `/`
   - macOS/Linux：使用正斜杠 `/`

2. **权限问题**：
   - 确保路径可访问
   - Windows可能需要管理员权限

3. **功能限制**：
   - macOS不支持每日推荐和私人漫游功能
   - 基础功能（播放控制、搜索播放）无需配置路径

4. **优先级**：
   - 环境变量 > 配置文件 > 默认值

## 🚀 快速开始

如果您只想使用基础功能（播放控制、搜索播放），可以跳过路径配置，直接启动服务器：

```bash
python start_http_server.py
```

访问 http://localhost:8000/docs 查看可用的API功能。
