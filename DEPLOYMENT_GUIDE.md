# 🚀 网易云音乐HTTP控制器 - 部署指南

## 📋 部署前准备

### 1. 系统要求
- **Python 3.10+**
- **网易云音乐桌面客户端**（已安装）
- **网络连接**（用于搜索和播放功能）

### 2. 支持的操作系统
- **Windows 10/11**: 完整功能支持 ✅
- **macOS 10.15+**: 基础功能支持 ⚠️
- **Linux**: 基础功能支持 ⚠️

## 🔧 部署步骤

### 步骤1: 获取项目代码

#### 方法一：从GitHub克隆（推荐）
```bash
git clone https://github.com/xiduan/CloudMusic_Auto_Player.git
cd CloudMusic_Auto_Player
```

#### 方法二：下载ZIP文件
1. 访问项目GitHub页面
2. 点击 "Code" -> "Download ZIP"
3. 解压到目标目录

### 步骤2: 安装依赖

#### 使用pip安装（推荐）
```bash
# 安装所有依赖（使用国内源）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 或逐个安装
pip install fastapi uvicorn requests psutil pyautogui pywin32 selenium -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 使用虚拟环境（推荐）
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖（使用国内源）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 步骤3: 配置路径

#### 自动配置（推荐）
运行自动配置工具：
```bash
python auto_config.py
```

#### 手动配置

**方法一：环境变量**
```bash
# Windows
set NETEASE_MUSIC_PATH=D:\NetEase\CloudMusic\cloudmusic.exe
set CHROMEDRIVER_PATH=C:\path\to\chromedriver.exe

# macOS/Linux
export NETEASE_MUSIC_PATH="/Applications/NeteaseMusic.app/Contents/MacOS/NeteaseMusic"
```

**方法二：修改配置文件**
编辑 `netease_config.json`：
```json
{
  "netease_music_path": "你的网易云音乐路径",
  "debug_port": 9222,
  "chromedriver_path": "src/chromedriver/win64/chromedriver.exe"
}
```

### 步骤4: 启动服务器

```bash
# 使用启动脚本（推荐）
python start_http_server.py

# 或直接运行
python src/http_server.py

# 或使用uvicorn
uvicorn src.http_server:app --host 0.0.0.0 --port 8000
```

### 步骤5: 验证部署

1. **访问API文档**: http://localhost:8000/docs
2. **检查配置**: http://localhost:8000/config
3. **测试功能**: http://localhost:8000/info

## 🎯 不同平台的部署说明

### Windows部署

#### 完整功能部署
```bash
# 1. 克隆项目
git clone https://github.com/xiduan/CloudMusic_Auto_Player.git
cd CloudMusic_Auto_Player

# 2. 安装依赖（使用国内源）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 3. 配置路径
python auto_config.py

# 4. 启动服务器
python start_http_server.py
```

#### 常见问题解决
- **pywin32安装失败**: 先安装Microsoft Visual C++ Build Tools
- **权限问题**: 以管理员身份运行命令提示符
- **端口占用**: 使用 `--port` 参数指定其他端口

### macOS部署

#### 基础功能部署
```bash
# 1. 克隆项目
git clone https://github.com/xiduan/CloudMusic_Auto_Player.git
cd CloudMusic_Auto_Player

# 2. 安装依赖（不包含pywin32，使用国内源）
pip install fastapi uvicorn requests psutil pyautogui selenium -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 3. 配置网易云音乐路径
export NETEASE_MUSIC_PATH="/Applications/NeteaseMusic.app/Contents/MacOS/NeteaseMusic"

# 4. 启动服务器
python start_http_server.py
```

#### 注意事项
- macOS不支持每日推荐和私人漫游功能
- 需要安装网易云音乐桌面版（非App Store版本）
- 可能需要授予辅助功能权限

### Linux部署

#### 基础功能部署
```bash
# 1. 克隆项目
git clone https://github.com/xiduan/CloudMusic_Auto_Player.git
cd CloudMusic_Auto_Player

# 2. 安装依赖（使用国内源）
pip install fastapi uvicorn requests psutil pyautogui selenium -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 3. 配置路径
export NETEASE_MUSIC_PATH="/path/to/netease/music"

# 4. 启动服务器
python start_http_server.py
```

## 🔍 路径配置指南

### 查找网易云音乐安装路径

#### Windows
```bash
# 搜索文件
dir /s C:\ cloudmusic.exe

# 检查常见位置
dir "C:\Program Files (x86)\Netease\CloudMusic\cloudmusic.exe"
dir "C:\Program Files\Netease\CloudMusic\cloudmusic.exe"
dir "C:\Users\%USERNAME%\AppData\Local\NetEase\CloudMusic\cloudmusic.exe"
dir "D:\NetEase\CloudMusic\cloudmusic.exe"
```

#### macOS
```bash
# 查找网易云音乐
find /Applications -name "*Netease*" -o -name "*网易云*"

# 常见路径
ls -la "/Applications/NeteaseMusic.app/Contents/MacOS/NeteaseMusic"
ls -la "/Applications/网易云音乐.app/Contents/MacOS/网易云音乐"
```

#### Linux
```bash
# 查找网易云音乐
find /opt /usr/local -name "*netease*" -o -name "*cloudmusic*"
```

### 常见安装路径

#### Windows
- `C:\Program Files (x86)\Netease\CloudMusic\cloudmusic.exe`
- `C:\Program Files\Netease\CloudMusic\cloudmusic.exe`
- `C:\Users\{用户名}\AppData\Local\NetEase\CloudMusic\cloudmusic.exe`
- `D:\NetEase\CloudMusic\cloudmusic.exe`

#### macOS
- `/Applications/NeteaseMusic.app/Contents/MacOS/NeteaseMusic`
- `/Applications/网易云音乐.app/Contents/MacOS/网易云音乐`

## 🚀 快速部署脚本

### Windows快速部署脚本
```batch
@echo off
echo 网易云音乐HTTP控制器 - Windows快速部署
echo =====================================

echo 1. 克隆项目...
git clone https://github.com/xiduan/CloudMusic_Auto_Player.git
cd CloudMusic_Auto_Player

echo 2. 安装依赖...
pip install -r requirements.txt

echo 3. 自动配置...
python auto_config.py

echo 4. 启动服务器...
python start_http_server.py
```

### macOS/Linux快速部署脚本
```bash
#!/bin/bash
echo "网易云音乐HTTP控制器 - macOS/Linux快速部署"
echo "======================================"

echo "1. 克隆项目..."
git clone https://github.com/xiduan/CloudMusic_Auto_Player.git
cd CloudMusic_Auto_Player

echo "2. 安装依赖..."
pip install fastapi uvicorn requests psutil pyautogui selenium

echo "3. 配置路径..."
export NETEASE_MUSIC_PATH="/Applications/NeteaseMusic.app/Contents/MacOS/NeteaseMusic"

echo "4. 启动服务器..."
python start_http_server.py
```

## 🔧 高级配置

### 自定义端口
```bash
python start_http_server.py --port 8080
```

### 开发模式
```bash
python start_http_server.py --reload
```

### 生产环境部署
```bash
# 使用gunicorn
pip install gunicorn
gunicorn src.http_server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📝 部署检查清单

- [ ] Python 3.10+ 已安装
- [ ] 项目代码已获取
- [ ] 依赖包已安装
- [ ] 网易云音乐路径已配置
- [ ] ChromeDriver路径已配置（Windows）
- [ ] 服务器已启动
- [ ] API文档可访问
- [ ] 基础功能测试通过
- [ ] 高级功能测试通过（可选）

## 🆘 故障排除

### 常见问题

1. **依赖安装失败**
   ```bash
   # 升级pip
   python -m pip install --upgrade pip
   
   # 使用国内镜像
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
   ```

2. **路径配置错误**
   ```bash
   # 验证路径
   python check_config.py
   ```

3. **端口被占用**
   ```bash
   # 使用其他端口
   python start_http_server.py --port 8080
   ```

4. **权限问题**
   - Windows: 以管理员身份运行
   - macOS: 授予辅助功能权限
   - Linux: 使用sudo或配置用户权限

## 📞 技术支持

- **项目仓库**: https://github.com/xiduan/CloudMusic_Auto_Player
- **问题反馈**: 请在GitHub Issues中提交
- **联系邮箱**: lxd4094@foxmail.com

---

**享受音乐，让控制更简单！** 🎵
