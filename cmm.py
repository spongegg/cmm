import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import re
import threading

class SubtitleRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("字幕重命名工具")
        self.root.geometry("310x100")
        self.root.resizable(True, True)

        # 默认后缀
        self.suffix = tk.StringVar(value=".chs")

        # 创建输入框和标签
        tk.Label(root, text="后缀:").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.suffix, font=('Arial', 14)).grid(row=0, column=1, padx=10, pady=5)

        # 按钮
        tk.Button(root, text="选择文件并启动重命名", command=self.start_rename).grid(row=1, column=0, columnspan=2, pady=10)

    def start_rename(self):
        threading.Thread(target=self.rename_files, daemon=True).start()

    def rename_files(self):
        initial_dir = os.path.expanduser("~")

        video_files = filedialog.askopenfilenames(
            title="选择视频文件",
            initialdir=initial_dir,
            filetypes=[("视频文件", "*.mp4 *.avi *.mkv *.mov")]
        )
        if not video_files:
            messagebox.showerror("错误", "未选择视频文件！")
            return

        subtitle_files = filedialog.askopenfilenames(
            title="选择字幕文件",
            initialdir=initial_dir,
            filetypes=[("字幕文件", "*.srt *.ass *.vtt")]
        )
        if not subtitle_files:
            messagebox.showerror("错误", "未选择字幕文件！")
            return

        # 提示文件数量不一致
        if len(video_files) != len(subtitle_files):
            if not messagebox.askyesno("文件数量不一致", "视频文件和字幕文件数量不一致！是否继续尝试匹配？"):
                return

        # 顺序匹配文件
        matched_pairs = self.match_files(video_files, subtitle_files)

        if not matched_pairs:
            messagebox.showwarning("未找到匹配", "无法匹配任何文件。")
            return

        confirmation_text = "\n".join([
            f"{os.path.basename(video)} <--> {os.path.basename(subtitle)}"
            for video, subtitle in matched_pairs
        ])

        if not messagebox.askyesno("确认重命名", f"以下文件将被重命名：\n{confirmation_text}"):
            return

        renamed_count = 0
        subtitle_dirs = set()  # 新增：记录字幕文件夹
        
        for video_file, subtitle_file in matched_pairs:
            try:
                new_subtitle_path = self.get_new_subtitle_path(video_file, subtitle_file)
                shutil.move(subtitle_file, new_subtitle_path)
                renamed_count += 1
            except Exception as e:
                messagebox.showerror("错误", f"处理文件失败：{subtitle_file}\n{e}")
		
		# 尝试删除空的字幕文件夹
        for folder in subtitle_dirs:
            try:
                if os.path.isdir(folder) and not os.listdir(folder):
                    os.rmdir(folder)
            except Exception as e:
                print(f"无法删除文件夹 {folder}：{e}")
                
        messagebox.showinfo("完成", f"成功重命名 {renamed_count} 个字幕文件！")

    def normalize_filename(self, filename):
        filename = re.sub(r'\[.*?\]|\(.*?\)', '', filename)  # 去括号
        return re.sub(r'[^a-zA-Z0-9]', '', filename.lower())  # 小写并去特殊字符

    def match_files(self, video_files, subtitle_files):
        matched_pairs = []

        # 顺序匹配视频文件和字幕文件
        for i in range(len(video_files)):
            if i < len(subtitle_files):
                matched_pairs.append((video_files[i], subtitle_files[i]))

        return matched_pairs

    def get_new_subtitle_path(self, video_file, subtitle_file):
        video_basename = os.path.splitext(os.path.basename(video_file))[0]
        subtitle_ext = os.path.splitext(subtitle_file)[1]
        subtitle_dir = os.path.dirname(video_file)
        return os.path.join(subtitle_dir, f"{video_basename}{self.suffix.get()}{subtitle_ext}")

# 主程序
if __name__ == "__main__":
    root = tk.Tk()
    app = SubtitleRenamerApp(root)
    root.mainloop()
