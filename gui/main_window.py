# -*- coding: utf-8 -*-
"""
主窗口GUI模块
提供用户交互界面 - 液态玻璃风格
"""

import os
import sys
import threading
from typing import Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
except ImportError:
    print("请安装tkinter: pip install tk")
    sys.exit(1)

from core import BilibiliDownloader


class GlassStyle:
    """液态玻璃风格配色方案"""
    # 主色调 - 深天空蓝
    PRIMARY_START = "#5DADE2"       # 深天空蓝
    PRIMARY_END = "#2E86C1"         # 更深蓝色
    PRIMARY_DARK = "#1B4F72"        # 深蓝

    # 毛玻璃效果 - 更深的背景
    GLASS_BG = "#AED6F1"            # 深天蓝背景

    # 边框和阴影 - 更细更精致
    BORDER_LIGHT = "#85C1E9"        # 浅蓝边框
    BORDER_FOCUS = "#2874A6"        # 聚焦边框加深

    # 文字颜色 - 全部加深
    TEXT_TITLE = "#154360"          # 标题深蓝加深
    TEXT_SUBTITLE = "#1F618D"       # 副标题蓝加深
    TEXT_LABEL = "#2471A3"          # 标签蓝加深
    TEXT_INPUT = "#1B4F72"          # 输入框文字加深
    TEXT_PLACEHOLDER = "#5DADE2"    # 占位符加深

    # 输入框背景
    INPUT_BG = "#FFFFFF"            # 白色背景
    INPUT_FOCUS_BG = "#EBF5FB"      # 聚焦时浅蓝

    # 状态颜色
    SUCCESS = "#1E8449"             # 深绿色
    ERROR = "#C0392B"               # 深红色

    # 按钮颜色
    BUTTON_BG = "#2E86C1"           # 按钮加深
    BUTTON_HOVER = "#1B4F72"        # 悬停加深
    BUTTON_SECONDARY = "#5DADE2"    # 次要按钮


class MainWindow:
    """主窗口类 - 液态玻璃风格"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("B站音频下载器")
        self.root.geometry("520x700")
        self.root.resizable(False, False)

        # 设置窗口背景色
        self.root.configure(bg=GlassStyle.GLASS_BG)

        # 初始化核心模块
        self.downloader = BilibiliDownloader()

        # 状态变量
        self.is_downloading = False
        self.current_file = None

        # 创建界面
        self._create_widgets()

    def _create_widgets(self):
        """创建界面组件"""
        # 配置ttk样式
        self._setup_styles()

        # 主容器 - 占满整个窗口，无边框
        container = tk.Frame(
            self.root,
            bg=GlassStyle.GLASS_BG,
            padx=40,
            pady=35
        )
        container.pack(fill='both', expand=True)

        # 标题
        title_label = tk.Label(
            container,
            text="B站音频下载器",
            font=('Microsoft YaHei UI', 24, 'bold'),
            fg=GlassStyle.TEXT_TITLE,
            bg=GlassStyle.GLASS_BG
        )
        title_label.pack(pady=(0, 6))

        # 副标题
        subtitle_label = tk.Label(
            container,
            text="轻松下载B站视频音频",
            font=('Microsoft YaHei UI', 11),
            fg=GlassStyle.TEXT_SUBTITLE,
            bg=GlassStyle.GLASS_BG
        )
        subtitle_label.pack(pady=(0, 25))

        # URL输入区域
        self._create_input_group(
            container,
            "视频链接",
            "请输入B站视频链接",
            'url'
        )

        # 保存位置
        self._create_save_path_group(container)

        # 设置区域 - 使用Frame分组
        settings_frame = tk.Frame(container, bg=GlassStyle.GLASS_BG)
        settings_frame.pack(fill='x', pady=(0, 20))

        # 格式选择
        format_frame = tk.Frame(settings_frame, bg=GlassStyle.GLASS_BG)
        format_frame.pack(side='left', fill='x', expand=True)

        format_label = tk.Label(
            format_frame,
            text="输出格式",
            font=('Microsoft YaHei UI', 10, 'bold'),
            fg=GlassStyle.TEXT_LABEL,
            bg=GlassStyle.GLASS_BG
        )
        format_label.pack(anchor='w', pady=(0, 6))

        self.format_var = tk.StringVar(value="mp3")
        format_combo = ttk.Combobox(
            format_frame,
            textvariable=self.format_var,
            values=BilibiliDownloader.SUPPORTED_FORMATS,
            state="readonly",
            width=12,
            font=('Microsoft YaHei UI', 10),
            style='Blue.TCombobox'
        )
        format_combo.pack(anchor='w', ipady=4)

        # 比特率选择
        bitrate_frame = tk.Frame(settings_frame, bg=GlassStyle.GLASS_BG)
        bitrate_frame.pack(side='right', fill='x', expand=True)

        bitrate_label = tk.Label(
            bitrate_frame,
            text="比特率",
            font=('Microsoft YaHei UI', 10, 'bold'),
            fg=GlassStyle.TEXT_LABEL,
            bg=GlassStyle.GLASS_BG
        )
        bitrate_label.pack(anchor='w', pady=(0, 6))

        self.bitrate_var = tk.StringVar(value="192k")
        bitrate_combo = ttk.Combobox(
            bitrate_frame,
            textvariable=self.bitrate_var,
            values=['128k', '192k', '256k', '320k'],
            state="readonly",
            width=12,
            font=('Microsoft YaHei UI', 10),
            style='Blue.TCombobox'
        )
        bitrate_combo.pack(anchor='w', ipady=4)

        # 进度区域
        progress_frame = tk.Frame(container, bg=GlassStyle.GLASS_BG)
        progress_frame.pack(fill='x', pady=(0, 15))

        progress_label = tk.Label(
            progress_frame,
            text="下载进度",
            font=('Microsoft YaHei UI', 10, 'bold'),
            fg=GlassStyle.TEXT_LABEL,
            bg=GlassStyle.GLASS_BG
        )
        progress_label.pack(anchor='w', pady=(0, 6))

        # 进度条
        self.progress_var = tk.DoubleVar(value=0)

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            style="Blue.Horizontal.TProgressbar",
            length=340
        )
        self.progress_bar.pack(fill='x')

        # 状态标签
        self.status_var = tk.StringVar(value="就绪")
        self.status_label = tk.Label(
            progress_frame,
            textvariable=self.status_var,
            font=('Microsoft YaHei UI', 9),
            fg='#2E86C1',
            bg=GlassStyle.GLASS_BG
        )
        self.status_label.pack(anchor='w', pady=(6, 0))

        # 下载按钮
        self.download_btn = tk.Button(
            container,
            text="开始下载",
            font=('Microsoft YaHei UI', 12, 'bold'),
            bg=GlassStyle.BUTTON_BG,
            fg='white',
            activebackground=GlassStyle.BUTTON_HOVER,
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            width=18,
            height=1,
            command=self._start_download
        )
        self.download_btn.pack(pady=(5, 15))

        # 按钮悬停效果
        self.download_btn.bind('<Enter>', lambda e: self.download_btn.configure(bg=GlassStyle.BUTTON_HOVER))
        self.download_btn.bind('<Leave>', lambda e: self.download_btn.configure(bg=GlassStyle.BUTTON_BG))

        # 输出信息区域
        output_frame = tk.Frame(container, bg=GlassStyle.GLASS_BG)
        output_frame.pack(fill='both', expand=True)

        output_label = tk.Label(
            output_frame,
            text="输出信息",
            font=('Microsoft YaHei UI', 10, 'bold'),
            fg=GlassStyle.TEXT_LABEL,
            bg=GlassStyle.GLASS_BG
        )
        output_label.pack(anchor='w', pady=(0, 6))

        # 输出文本框
        text_frame = tk.Frame(output_frame, bg='white', padx=1, pady=1)
        text_frame.pack(fill='both', expand=True)

        self.log_text = tk.Text(
            text_frame,
            height=6,
            font=('Consolas', 9),
            bg='white',
            fg='#1B4F72',
            relief='flat',
            borderwidth=0,
            highlightthickness=0,
            padx=10,
            pady=8
        )
        self.log_text.pack(side='left', fill='both', expand=True)

        scrollbar = tk.Scrollbar(
            text_frame,
            orient='vertical',
            command=self.log_text.yview,
            bg='#AED6F1'
        )
        scrollbar.pack(side='right', fill='y')
        self.log_text.configure(yscrollcommand=scrollbar.set)

    def _setup_styles(self):
        """配置ttk样式"""
        style = ttk.Style()
        style.theme_use('clam')

        # 配置Combobox样式
        style.configure('Blue.TCombobox',
            background='white',
            foreground='#1B4F72',
            fieldbackground='white',
            selectbackground='#AED6F1',
            selectforeground='#1B4F72',
            arrowcolor='#2E86C1',
            bordercolor='#85C1E9',
            lightcolor='white',
            darkcolor='#EBF5FB'
        )

        # 配置Combobox下拉列表样式
        style.map('Blue.TCombobox',
            fieldbackground=[('readonly', 'white')],
            selectbackground=[('readonly', '#AED6F1')],
            background=[('readonly', 'white')]
        )

        # 配置进度条样式
        style.configure("Blue.Horizontal.TProgressbar",
            troughcolor='white',
            background='#2E86C1',
            darkcolor='#2E86C1',
            lightcolor='#5DADE2',
            borderwidth=0,
            thickness=16
        )

    def _create_input_group(self, parent, label_text, placeholder, var_name):
        """创建输入组"""
        frame = tk.Frame(parent, bg=GlassStyle.GLASS_BG)
        frame.pack(fill='x', pady=(0, 15))

        label = tk.Label(
            frame,
            text=label_text,
            font=('Microsoft YaHei UI', 10, 'bold'),
            fg=GlassStyle.TEXT_LABEL,
            bg=GlassStyle.GLASS_BG
        )
        label.pack(anchor='w', pady=(0, 6))

        var = tk.StringVar()
        entry = tk.Entry(
            frame,
            textvariable=var,
            font=('Microsoft YaHei UI', 10),
            bg='white',
            fg=GlassStyle.TEXT_INPUT,
            relief='solid',
            borderwidth=1,
            highlightthickness=0
        )
        entry.pack(fill='x', ipady=8, padx=0, pady=0)
        entry.insert(0, placeholder)
        entry.configure(fg=GlassStyle.TEXT_PLACEHOLDER)

        # 绑定焦点事件
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.configure(fg=GlassStyle.TEXT_INPUT)
            entry.configure(highlightcolor=GlassStyle.BORDER_FOCUS, highlightbackground=GlassStyle.BORDER_FOCUS)

        def on_focus_out(event):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.configure(fg=GlassStyle.TEXT_PLACEHOLDER)
            entry.configure(highlightcolor=GlassStyle.BORDER_LIGHT, highlightbackground=GlassStyle.BORDER_LIGHT)

        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

        setattr(self, f'{var_name}_var', var)
        setattr(self, f'{var_name}_entry', entry)

    def _create_save_path_group(self, parent):
        """创建保存路径组"""
        frame = tk.Frame(parent, bg=GlassStyle.GLASS_BG)
        frame.pack(fill='x', pady=(0, 15))

        label = tk.Label(
            frame,
            text="保存位置",
            font=('Microsoft YaHei UI', 10, 'bold'),
            fg=GlassStyle.TEXT_LABEL,
            bg=GlassStyle.GLASS_BG
        )
        label.pack(anchor='w', pady=(0, 6))

        # 输入框和按钮容器
        path_frame = tk.Frame(frame, bg=GlassStyle.GLASS_BG)
        path_frame.pack(fill='x')

        self.save_dir_var = tk.StringVar(value=os.path.join(os.getcwd(), "downloads"))
        entry = tk.Entry(
            path_frame,
            textvariable=self.save_dir_var,
            font=('Microsoft YaHei UI', 10),
            bg='white',
            fg=GlassStyle.TEXT_INPUT,
            relief='solid',
            borderwidth=1,
            highlightthickness=0
        )
        entry.pack(side='left', fill='x', expand=True, ipady=8)

        # 绑定焦点事件
        def on_focus_in(event):
            entry.configure(highlightcolor=GlassStyle.BORDER_FOCUS, highlightbackground=GlassStyle.BORDER_FOCUS)

        def on_focus_out(event):
            entry.configure(highlightcolor=GlassStyle.BORDER_LIGHT, highlightbackground=GlassStyle.BORDER_LIGHT)

        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

        # 浏览按钮
        browse_btn = tk.Button(
            path_frame,
            text="浏览",
            font=('Microsoft YaHei UI', 9, 'bold'),
            bg=GlassStyle.BUTTON_SECONDARY,
            fg='white',
            activebackground='#2E86C1',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8,
            command=self._browse_directory
        )
        browse_btn.pack(side='right', padx=(8, 0))

        # 按钮悬停效果
        browse_btn.bind('<Enter>', lambda e: browse_btn.configure(bg='#2E86C1'))
        browse_btn.bind('<Leave>', lambda e: browse_btn.configure(bg=GlassStyle.BUTTON_SECONDARY))

    def _browse_directory(self):
        """浏览选择目录"""
        directory = filedialog.askdirectory(
            title="选择保存目录",
            initialdir=self.save_dir_var.get()
        )
        if directory:
            self.save_dir_var.set(directory)

    def _log(self, message: str):
        """添加输出信息（线程安全）"""
        self.root.after(0, lambda: self._do_log(message))

    def _do_log(self, message: str):
        """实际执行输出更新（在主线程中）"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)

    def _update_progress(self, downloaded: int, total: int):
        """更新进度条（线程安全）"""
        if total > 0:
            progress = (downloaded / total) * 100
            self.root.after(0, lambda: self._do_update_progress(progress))

    def _do_update_progress(self, progress: float):
        """实际执行进度更新（在主线程中）"""
        self.progress_var.set(progress)
        self.status_var.set(f"下载中... {progress:.1f}%")

    def _start_download(self):
        """开始下载"""
        url = self.url_entry.get().strip()

        # 检查是否是占位符
        if url == "请输入B站视频链接" or not url:
            messagebox.showerror("错误", "请输入视频URL")
            return

        # 验证URL并提取BV号
        bvid = self.downloader.extract_bvid_from_url(url)
        if not bvid:
            messagebox.showerror("错误", "无法识别B站视频链接，请检查URL是否正确")
            return

        save_dir = self.save_dir_var.get().strip()
        if not save_dir:
            messagebox.showerror("错误", "请选择保存位置")
            return

        # 禁用下载按钮
        self.download_btn.config(state=tk.DISABLED, bg='#B0BEC5')
        self.is_downloading = True

        # 清空输出信息
        self.log_text.delete(1.0, tk.END)
        self._log(f"识别到视频ID: {bvid}")
        self._log(f"开始下载: {url}")

        # 在新线程中执行下载
        thread = threading.Thread(
            target=self._download_thread,
            args=(url, save_dir),
            daemon=True
        )
        thread.start()

    def _download_thread(self, url: str, save_dir: str):
        """下载线程"""
        try:
            # 获取输出格式和比特率
            output_format = self.format_var.get()
            bitrate = self.bitrate_var.get()

            self._log(f"输出格式: {output_format}")
            self._log(f"比特率: {bitrate}")

            # 使用 yt-dlp 下载音频
            success, message, file_path = self.downloader.download_audio(
                url=url,
                save_dir=save_dir,
                output_format=output_format,
                bitrate=bitrate,
                progress_callback=self._update_progress
            )

            if success:
                self._log(message)
                self.current_file = file_path
                self._finish_download(True, "下载完成!")
            else:
                self._log(f"错误: {message}")
                self._finish_download(False, message)

        except Exception as e:
            self._log(f"发生错误: {str(e)}")
            self._finish_download(False, f"发生错误: {str(e)}")

    def _finish_download(self, success: bool, message: str):
        """完成下载"""
        self.is_downloading = False
        self.root.after(0, self._update_ui_after_download, success, message)

    def _update_ui_after_download(self, success: bool, message: str):
        """下载完成后更新UI"""
        self.download_btn.config(state=tk.NORMAL, bg=GlassStyle.BUTTON_BG)

        # 重置进度条
        self.progress_var.set(0)

        if success:
            self.status_var.set("下载完成")
            self.status_label.config(fg=GlassStyle.SUCCESS)
            messagebox.showinfo("完成", message)
        else:
            self.status_var.set("下载失败")
            self.status_label.config(fg=GlassStyle.ERROR)
            messagebox.showerror("错误", message)

        # 延迟重置状态为就绪
        self.root.after(2000, self._reset_status)

    def _reset_status(self):
        """重置状态为就绪"""
        self.status_var.set("就绪")
        self.status_label.config(fg='#2E86C1')

    def run(self):
        """运行主窗口"""
        self.root.mainloop()


def main():
    """主函数"""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
