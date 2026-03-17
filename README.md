# B站音频下载器

一个用于从B站视频提取音频的Python工具，基于 yt-dlp + ffmpeg 实现，支持多种音频格式。

## 功能特性

- 从B站视频URL提取音频
- 支持多种音频格式：MP3, WAV, FLAC, AAC, OGG, M4A, OPUS
- 自定义保存位置
- 可调节比特率
- 友好的GUI界面
- 实时下载进度显示
- **无需手动安装ffmpeg**：使用 imageio-ffmpeg 自动包含

## 项目结构

```
musicdownloader/
├── core/                  # 核心功能模块
│   ├── __init__.py
│   └── downloader.py      # B站视频下载器（基于 yt-dlp + ffmpeg）
├── gui/                   # GUI界面模块
│   ├── __init__.py
│   └── main_window.py     # 主窗口
├── main.py                # 主程序入口
├── requirements.txt       # 依赖文件
└── README.md              # 说明文档
```

## 安装依赖

### 一键安装所有依赖

```bash
pip install -r requirements.txt
```

**注意：** 
- 所有依赖都会自动安装，包括 ffmpeg（通过 imageio-ffmpeg）
- 无需手动下载或配置 ffmpeg
- 支持 Windows、Linux、macOS

### 使用步骤

1. 在"视频URL"输入框中粘贴B站视频链接
2. 点击"浏览"选择保存位置（默认为项目目录下的downloads文件夹）
3. 选择输出格式（默认为MP3）
4. 选择比特率（默认为192k）
5. 点击"下载音频"开始下载
6. 等待下载完成

## 模块说明

### core.downloader - 下载器模块

基于 yt-dlp 实现的音频下载器，主要功能：
- 提取视频信息（BV号、标题等）
- 下载音频文件
- 自动格式转换
- 支持多种音频格式

### gui.main_window - GUI模块

提供用户交互界面，主要功能：
- URL输入
- 保存位置选择
- 格式和比特率选择
- 进度显示
- 日志输出

## 注意事项

1. 请确保网络连接正常
2. 支持各种格式的B站视频链接，包括：
   - https://www.bilibili.com/video/BVxxxxxx
   - https://www.bilibili.com/video/BVxxxxxx?p=1
   - https://www.bilibili.com/video/BVxxxxxx/?spm_id_from=...
   - 以及其他包含BV号的URL
3. yt-dlp 会自动处理音频格式转换，无需额外配置

## 许可证

MIT License
