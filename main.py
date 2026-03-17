"""
B站音频下载器 - 主程序入口
支持从B站视频提取音频并转换为多种格式
"""

import sys
import os

# 确保项目根目录在路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import MainWindow


def main():
    """主函数"""
    print("=" * 50)
    print("B站音频下载器")
    print("=" * 50)
    print("正在启动GUI界面...")

    try:
        app = MainWindow()
        app.run()
    except KeyboardInterrupt:
        print("\n程序已退出")
    except Exception as e:
        print(f"程序运行出错: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
