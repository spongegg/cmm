import tkinter as tk
from tkinter import filedialog, messagebox
import os

def rename_subtitles():
    # 获取视频文件路径
    video_paths = filedialog.askopenfilenames(title="选择视频文件", filetypes=[("视频文件", "*.mp4;*.avi;*.mkv")])
    if not video_paths:
        return

    # 获取字幕文件路径
    subtitle_paths = filedialog.askopenfilenames(title="选择字幕文件", filetypes=[("字幕文件", "*.srt;*.ass")])
    if not subtitle_paths:
        return

    # 获取后缀
    suffix = entry_suffix.get()

    for video_path, subtitle_path in zip(video_paths, subtitle_paths):
        # 构建新的字幕文件名
        new_subtitle_name = os.path.splitext(os.path.basename(video_path))[0] + suffix + os.path.splitext(os.path.basename(subtitle_path))[1]
        new_subtitle_path = os.path.join(os.path.dirname(video_path), new_subtitle_name)

        # 重命名字幕文件
        try:
            os.rename(subtitle_path, new_subtitle_path)
            messagebox.showinfo("成功", f"字幕文件已成功重命名: {new_subtitle_path}")
        except Exception as e:
            messagebox.showerror("错误", f"重命名失败: {e}")

# 创建GUI
root = tk.Tk()
root.title("字幕重命名工具")

# 设置字体为中文支持的字体
#root.configure(font=('楷体', 10))

# 创建一个按钮，点击后触发rename_subtitles函数
button_rename = tk.Button(root, text="重命名字幕", command=rename_subtitles)
button_rename.pack(pady=20)

# 创建一个输入框，用于输入后缀
entry_suffix = tk.Entry(root)
entry_suffix.pack(pady=10)

# 设置输入框的提示文本为中文
entry_suffix.insert(0, ".chs")

# 运行GUI
root.mainloop()
