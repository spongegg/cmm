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

    # 检查视频和字幕文件数量是否相同
    if len(video_paths) != len(subtitle_paths):
        messagebox.showerror("错误", "视频文件和字幕文件数量不匹配！")
        return

    success_count = 0
    subtitle_folders = set()  # 用于存储字幕文件所在的文件夹路径

    for video_path, subtitle_path in zip(video_paths, subtitle_paths):
        # 构建新的字幕文件名
        new_subtitle_name = os.path.splitext(os.path.basename(video_path))[0] + suffix + os.path.splitext(os.path.basename(subtitle_path))[1]
        new_subtitle_path = os.path.join(os.path.dirname(video_path), new_subtitle_name)

        # 获取字幕文件所在的文件夹路径
        subtitle_folder = os.path.dirname(subtitle_path)
        subtitle_folders.add(subtitle_folder)

        # 重命名字幕文件
        try:
            os.rename(subtitle_path, new_subtitle_path)
            success_count += 1
            print(f"字幕文件已成功重命名: {new_subtitle_path}")
        except Exception as e:
            messagebox.showerror("错误", f"重命名失败: {e}")

    # 如果有文件重命名成功，显示完成对话框
    if success_count > 0:
        messagebox.showinfo("完成", f"共成功重命名 {success_count} 个字幕文件。")
    else:
        messagebox.showinfo("完成", "没有字幕文件被重命名。")

    # 尝试删除字幕文件所在的文件夹
    for folder in subtitle_folders:
        try:
            # 检查文件夹是否为空
            if not os.listdir(folder):  # 文件夹为空
                os.rmdir(folder)  # 删除空文件夹
                print(f"已删除空文件夹: {folder}")
        except Exception as e:
            messagebox.showerror("错误", f"删除文件夹失败: {e}")

# 创建GUI
root = tk.Tk()
root.title("字幕重命名工具")


# 设置窗口大小为 400x300
root.geometry("259x123")



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
