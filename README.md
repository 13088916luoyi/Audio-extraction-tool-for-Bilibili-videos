# B站音频下载器

一个用于从B站视频提取音频的Python工具，基于 yt-dlp + ffmpeg 实现，支持多种音频格式。

## 功能特性

- 从B站视频URL提取音频
- 支持多种音频格式：MP3, WAV, FLAC, AAC, OGG, M4A, OPUS
- 自定义保存位置
- 可调节比特率

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

## 注意事项

1. 请确保网络连接正常
2. 支持各种格式的B站视频链接，包括：
   - https://www.bilibili.com/video/BVxxxxxx
   - https://www.bilibili.com/video/BVxxxxxx?p=1
   - https://www.bilibili.com/video/BVxxxxxx/?spm_id_from=...
   - 以及其他包含BV号的URL
