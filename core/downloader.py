"""
使用 yt-dlp 从B站视频提取音频
使用 ffmpeg 命令行进行格式转换
"""

import os
import re
import subprocess
from typing import Optional, Tuple, Callable
import yt_dlp
import imageio_ffmpeg


class BilibiliDownloader:
    """B站视频下载器（基于 yt-dlp + ffmpeg）"""

    # 支持的音频格式
    SUPPORTED_FORMATS = ['mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a', 'opus']
    
    # 格式转换参数映射
    FORMAT_PARAMS = {
        'mp3': ['-acodec', 'libmp3lame', '-b:a'],
        'wav': ['-acodec', 'pcm_s16le'],
        'flac': ['-acodec', 'flac'],
        'aac': ['-acodec', 'aac', '-b:a'],
        'ogg': ['-acodec', 'libvorbis', '-b:a'],
        'opus': ['-acodec', 'libopus', '-b:a'],
        'm4a': ['-acodec', 'aac', '-b:a'],
    }

    def __init__(self):
        self.download_progress = 0
        self.is_cancelled = False
        # 获取ffmpeg路径
        self.ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        
        # 打印ffmpeg配置信息
        print(f"[INFO] FFmpeg路径: {self.ffmpeg_path}")
        print(f"[INFO] FFmpeg文件存在: {os.path.exists(self.ffmpeg_path)}")

    def extract_bvid_from_url(self, url: str) -> Optional[str]:
        """
        :param url: 任意格式的URL或文本
        :return: BV号或None
        """
        # BV号格式：BV + 10位字符（字母和数字混合）
        # 简化识别：直接匹配BV开头+10位字符
        bv_pattern = r'(BV[a-zA-Z0-9]{10})'
        match = re.search(bv_pattern, url)
        
        if match:
            return match.group(1)
        
        return None

    def _progress_hook(self, d: dict, progress_callback: Optional[Callable[[int, int], None]] = None):
        """
        yt-dlp 进度回调
        :param d: yt-dlp 返回的进度信息
        :param progress_callback: 自定义进度回调函数
        """
        if self.is_cancelled:
            raise Exception("下载已取消")

        if d['status'] == 'downloading':
            # 获取下载进度
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            
            if total > 0 and progress_callback:
                progress_callback(downloaded, total)

    def _clean_url(self, url: str) -> str:
        """
        清理URL，移除标题等额外信息
        :param url: 原始URL
        :return: 清理后的URL
        """
        # 提取BV号
        bvid = self.extract_bvid_from_url(url)
        if not bvid:
            return url
        
        # 构建标准URL
        return f"https://www.bilibili.com/video/{bvid}"

    def _convert_audio(self, input_file: str, output_file: str, 
                       output_format: str, bitrate: Optional[str] = None) -> Tuple[bool, str]:
        """
        使用ffmpeg命令行转换音频格式
        :param input_file: 输入文件路径
        :param output_file: 输出文件路径
        :param output_format: 输出格式
        :param bitrate: 比特率
        :return: (是否成功, 消息)
        """
        try:
            print(f"[INFO] 开始转换音频: {input_file} -> {output_file}")
            
            # 构建ffmpeg命令
            cmd = [
                self.ffmpeg_path,
                '-i', input_file,
                '-y',  # 覆盖输出文件
            ]
            
            # 使用格式参数映射
            format_lower = output_format.lower()
            if format_lower in self.FORMAT_PARAMS:
                params = self.FORMAT_PARAMS[format_lower].copy()
                # 如果参数列表包含 -b:a，添加比特率
                if '-b:a' in params:
                    params.append(bitrate or '192k')
                cmd.extend(params)
            
            cmd.append(output_file)
            
            print(f"[INFO] 执行命令: {' '.join(cmd)}")
            
            # 执行转换
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            if result.returncode == 0:
                if os.path.exists(output_file):
                    file_size = os.path.getsize(output_file)
                    print(f"[INFO] 转换成功，文件大小: {file_size/1024/1024:.2f} MB")
                    return True, f"转换成功: {output_file}"
                else:
                    return False, "转换失败：输出文件不存在"
            else:
                error_msg = result.stderr.split('\n')[-2] if result.stderr else "未知错误"
                print(f"[ERROR] ffmpeg错误: {error_msg}")
                return False, f"转换失败: {error_msg}"
            
        except subprocess.TimeoutExpired:
            print(f"[ERROR] 转换超时")
            return False, "转换超时"
        except FileNotFoundError:
            print(f"[ERROR] ffmpeg未找到: {self.ffmpeg_path}")
            return False, f"ffmpeg未找到: {self.ffmpeg_path}"
        except Exception as e:
            print(f"[ERROR] 转换异常: {str(e)}")
            return False, f"转换失败: {str(e)}"

    def download_audio(self, url: str, save_dir: str, 
                       output_format: str = 'mp3',
                       bitrate: Optional[str] = None,
                       progress_callback: Optional[Callable[[int, int], None]] = None) -> Tuple[bool, str, Optional[str]]:
        """
        下载音频文件
        :param url: B站视频URL
        :param save_dir: 保存目录
        :param output_format: 输出格式（mp3, wav, flac, aac, ogg, m4a, opus）
        :param bitrate: 比特率（可选，如 '192k'）
        :param progress_callback: 进度回调函数
        :return: (是否成功, 消息, 保存路径)
        """
        try:
            # 重置取消标志
            self.is_cancelled = False

            # 验证URL并清理
            bvid = self.extract_bvid_from_url(url)
            if not bvid:
                return False, "无法识别B站视频链接，请检查URL是否正确", None
            
            # 清理URL，移除标题等额外信息
            clean_url = self._clean_url(url)

            # 确保保存目录存在
            os.makedirs(save_dir, exist_ok=True)

            # 构建输出文件模板（先下载为m4a）
            output_template = os.path.join(save_dir, '%(title)s.%(ext)s')

            # 配置 yt-dlp 选项 - 只下载，不转换
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_template,
                'progress_hooks': [lambda d: self._progress_hook(d, progress_callback)],
                'quiet': True,
                'no_warnings': True,
            }

            # 下载
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # 先获取视频信息（使用清理后的URL）
                info = ydl.extract_info(clean_url, download=False)
                if not info:
                    return False, "无法获取视频信息", None

                # 获取视频标题
                title = info.get('title', bvid)
                
                # 清理文件名中的非法字符
                title = self._clean_filename(title)

                # 执行下载（使用清理后的URL）
                ydl.download([clean_url])

                # 构建实际保存的文件路径
                actual_filename = ydl.prepare_filename(info)
                
                # 检查文件是否存在
                if not os.path.exists(actual_filename):
                    # 尝试在保存目录中查找文件
                    for file in os.listdir(save_dir):
                        if file.startswith(title) or bvid in file:
                            actual_filename = os.path.join(save_dir, file)
                            break
                
                if not os.path.exists(actual_filename):
                    return False, "下载完成，但无法找到文件", None

                print(f"[INFO] 下载完成: {actual_filename}")

                # 如果需要格式转换
                if output_format.lower() != 'm4a':
                    # 构建输出文件路径
                    base, _ = os.path.splitext(actual_filename)
                    output_file = f"{base}.{output_format.lower()}"
                    
                    # 使用ffmpeg转换格式
                    success, message = self._convert_audio(
                        actual_filename, 
                        output_file, 
                        output_format, 
                        bitrate
                    )
                    
                    if success:
                        # 删除原始m4a文件
                        try:
                            os.remove(actual_filename)
                        except Exception:
                            pass
                        except Exception as e:
                            print(f"[DEBUG] 删除原始文件失败: {str(e)}")
                        
                        return True, message, output_file
                    else:
                        # 转换失败，返回原始m4a文件
                        return True, f"下载成功（格式转换失败，已保存为m4a）: {actual_filename}", actual_filename
                else:
                    # 不需要转换，直接返回m4a文件
                    return True, f"下载成功: {actual_filename}", actual_filename

        except Exception as e:
            if "下载已取消" in str(e):
                return False, "下载已取消", None
            return False, f"下载失败: {str(e)}", None

    def _clean_filename(self, filename: str) -> str:
        """清理文件名中的非法字符"""
        illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in illegal_chars:
            filename = filename.replace(char, '_')
        return filename.strip()

    def cancel_download(self):
        """取消下载"""
        self.is_cancelled = True

    def get_video_info(self, url: str) -> Optional[dict]:
        """
        获取视频信息（不下载）
        :param url: B站视频URL
        :return: 视频信息字典
        """
        try:
            bvid = self.extract_bvid_from_url(url)
            if not bvid:
                return None

            # 清理URL
            clean_url = self._clean_url(url)

            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(clean_url, download=False)
                
                if not info:
                    return None

                return {
                    'bvid': bvid,
                    'title': info.get('title', bvid),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', ''),
                    'description': info.get('description', ''),
                    'url': clean_url
                }

        except Exception as e:
            print(f"获取视频信息失败: {str(e)}")
            return None
