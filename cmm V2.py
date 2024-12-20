import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import re

class SubtitleRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("字幕重命名工具")
        self.root.geometry("340x90")  # 设置初始窗口大小
        self.root.resizable(True, True)  # 允许调整大小

        # 默认后缀
        self.suffix = tk.StringVar(value=".chs")

        # 创建输入框和标签
        self.label_suffix = tk.Label(root, text="后缀:")
        self.label_suffix.grid(row=0, column=0, padx=10, pady=5)

        self.entry_suffix = tk.Entry(root, textvariable=self.suffix, font=('Arial', 14))
        self.entry_suffix.grid(row=0, column=1, padx=10, pady=5)

        # 创建一个按钮用于选择文件和启动重命名操作
        self.btn_rename = tk.Button(root, text="选择文件并启动重命名", command=self.rename_files)
        self.btn_rename.grid(row=1, column=0, columnspan=2, pady=10)

    def rename_files(self):
        """
        启动选择视频和字幕文件并重命名操作。
        """
        # 选择视频文件
        video_files = filedialog.askopenfilenames(title="选择视频文件", filetypes=[("视频文件", "*.mp4;*.avi;*.mkv;*.mov")])
        if not video_files:
            messagebox.showerror("错误", "未选择视频文件！")
            return

        # 选择字幕文件
        subtitle_files = filedialog.askopenfilenames(title="选择字幕文件", filetypes=[("字幕文件", "*.srt;*.ass;*.vtt")])
        if not subtitle_files:
            messagebox.showerror("错误", "未选择字幕文件！")
            return

        if len(video_files) != len(subtitle_files):
            # 允许用户继续操作并尝试匹配
            if not messagebox.askyesno("文件数量不一致", "视频文件和字幕文件数量不一致！是否继续尝试匹配？"):
                return

        # 顺序匹配字幕和视频文件
        matched_pairs = self.match_files(video_files, subtitle_files)

        # 列出所有匹配和未匹配的文件（只显示文件名）
        matched_files = "\n".join([f"{os.path.basename(video)} <--> {os.path.basename(subtitle)}" for video, subtitle in matched_pairs])
        unmatched_files = "\n".join([f"{os.path.basename(video)} <--> 未匹配字幕" for video in video_files if video not in [x[0] for x in matched_pairs]])
        unmatched_subtitles = "\n".join([f"未匹配视频: {os.path.basename(subtitle)}" for subtitle in subtitle_files if subtitle not in [x[1] for x in matched_pairs]])

        # 显示匹配文件列表并确认
        confirmation_text = f"以下文件将被重命名：\n{matched_files}\n\n未匹配的文件：\n{unmatched_files}\n{unmatched_subtitles}"

        if not messagebox.askyesno("确认匹配", confirmation_text):
            return

        renamed_count = 0

        # 执行重命名
        for video_file, subtitle_file in matched_pairs:
            video_filename = os.path.splitext(os.path.basename(video_file))[0]
            video_dir = os.path.dirname(video_file)
            subtitle_dir = os.path.dirname(subtitle_file)
            subtitle_ext = os.path.splitext(subtitle_file)[1]
            new_subtitle_name = video_filename + self.suffix.get() + subtitle_ext
            new_subtitle_path = os.path.join(video_dir, new_subtitle_name)  # 新路径为视频文件的文件夹

            # 检查目标目录中是否已经存在同名文件
            if os.path.exists(new_subtitle_path):
                response = messagebox.askyesno("文件已存在", f"目标文件 {new_subtitle_name} 已存在，是否覆盖？")
                if not response:
                    continue  # 如果用户选择不覆盖，跳过当前文件

            # 重命名并移动字幕文件
            try:
                shutil.move(subtitle_file, new_subtitle_path)
                renamed_count += 1
            except Exception as e:
                messagebox.showerror("错误", f"无法重命名或移动文件 {subtitle_file}:\n{e}")
                return

            # 删除原字幕文件夹（如果为空）
            try:
                if not os.listdir(subtitle_dir):  # 检查文件夹是否为空
                    os.rmdir(subtitle_dir)
            except Exception as e:
                messagebox.showerror("错误", f"无法删除文件夹 {subtitle_dir}:\n{e}")
                return

        # 显示结果
        messagebox.showinfo("操作完成", f"成功重命名并移动 {renamed_count} 个文件！")

    def normalize_filename(self, filename):
        """
        标准化文件名，去掉括号中的内容，并统一为小写格式，去除多余空格。
        :param filename: 文件名
        :return: 标准化后的文件名
        """
        # 去掉括号和方括号内的内容
        filename = re.sub(r'\[.*?\]|\(.*?\)', '', filename)

        # 将文件名转化为小写，并去除多余空格
        filename = filename.lower().replace(' ', '')

        # 打印标准化后的文件名用于调试
        print(f"Normalized filename: {filename}")
        return filename

    def extract_episode_number(self, filename):
        """
        提取文件名中的集数数字部分（例如 S01E02、02）
        :param filename: 文件名
        :return: 集数部分
        """
        # 匹配 'S01E02' 或者 '01' 格式的集数
        match = re.search(r'(?:s\d{2}e(\d{2})|(\d{2}))', filename.lower())  # 匹配 S01E02 或 02 格式
        if match:
            # 如果是 S01E02 格式，提取集数部分（02）
            episode = match.group(1) if match.group(1) else match.group(2)  # 提取集数部分
            print(f"Extracted episode: {episode} from {filename}")  # 打印提取的集数
            return episode.zfill(2)  # 确保返回的集数是2位数
        return None

    def match_files(self, video_files, subtitle_files):
        """
        基于集数数字模糊匹配视频和字幕文件
        """
        matched_pairs = []

        # 遍历视频文件和字幕文件
        for video, subtitle in zip(video_files, subtitle_files):
            # 提取视频和字幕文件的名称
            video_name = os.path.splitext(os.path.basename(video))[0]
            subtitle_name = os.path.splitext(os.path.basename(subtitle))[0]

            # 标准化文件名，去掉括号和转化为小写
            normalized_video_name = self.normalize_filename(video_name)
            normalized_subtitle_name = self.normalize_filename(subtitle_name)

            # 提取集数信息
            video_episode = self.extract_episode_number(normalized_video_name)
            subtitle_episode = self.extract_episode_number(normalized_subtitle_name)

            # 比较视频和字幕的集数信息
            if video_episode and subtitle_episode and video_episode == subtitle_episode:
                matched_pairs.append((video, subtitle))
            else:
                print(f"Failed to match: {video_name} and {subtitle_name}")  # 打印匹配失败的文件对

        return matched_pairs

# 创建主窗口
root = tk.Tk()
app = SubtitleRenamerApp(root)

# 运行主循环
root.mainloop()
