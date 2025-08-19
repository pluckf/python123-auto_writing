# Python123.io 测试工具 - 安装说明

## 环境要求
- Python 3.7+
- Windows

## 安装步骤

### 1. 克隆或下载项目
```bash
# 如果从git克隆
git clone <repository-url>
cd python123

# 或直接下载解压到目录
```

### 2. 安装Python依赖
```bash
# 安装核心依赖
pip install -r requirements.txt

# 或使用简化版本
pip install -r requirements-minimal.txt

# 或手动安装
pip install requests==2.31.0 urllib3==2.1.0
```

### 3. GUI界面额外要求 (tkinter)
- **Windows**: 通常已包含在Python安装中
- **macOS**: 通常已包含在Python安装中  
- **Linux Ubuntu/Debian**: 
  ```bash
  sudo apt-get install python3-tk
  ```
- **Linux CentOS/RHEL**:
  ```bash
  sudo yum install tkinter
  # 或
  sudo dnf install python3-tkinter
  ```

### 4. 验证安装
```bash
python -c "import requests, urllib3, tkinter; print('所有依赖安装成功!')"
```

## 主要工具使用
- **GUI界面**: `python python123_gui.py`
- **全组测试**: `python all_groups_tester.py`
- **单组测试**: `python group7_tester.py`

## 依赖说明
- **requests**: HTTP客户端库，用于API请求
- **urllib3**: HTTP连接池库，requests的底层依赖
- **tkinter**: GUI界面库 (Python标准库)
- 其他: json, re, time, os等为Python标准库，无需单独安装
