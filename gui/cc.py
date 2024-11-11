import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def rename_and_copy_files(src_dir, dest_dir, suffix=""):
    try:
        # 获取两个文件夹中的文件列表
        src_files = sorted(os.listdir(src_dir))
        dest_files = sorted(os.listdir(dest_dir))

        # 确保两个文件夹中的文件数量相同
        if len(src_files) != len(dest_files):
            messagebox.showerror("错误", "两个文件夹中的文件数量不相同！")
            return

        for src_file, dest_file in zip(src_files, dest_files):
            # 获取文件的原扩展名
            dest_ext = os.path.splitext(dest_file)[1]
            
            # 构造新的文件名（包含后缀）
            new_name = os.path.splitext(src_file)[0] + suffix + dest_ext
            
            # 获取完整路径
            dest_path = os.path.join(dest_dir, dest_file)
            new_dest_path = os.path.join(dest_dir, new_name)
            
            # 重命名文件夹 b 中的文件
            os.rename(dest_path, new_dest_path)
            
            # 复制重命名后的文件到文件夹 a 中
            new_src_path = os.path.join(src_dir, new_name)
            shutil.copy2(new_dest_path, new_src_path)
        
        messagebox.showinfo("成功", "文件重命名并复制完成！")
    except Exception as e:
        messagebox.showerror("错误", str(e))

def select_src_dir():
    src_dir = filedialog.askdirectory(title="选择文件夹 a")
    src_entry.delete(0, tk.END)
    src_entry.insert(0, src_dir)

def select_dest_dir():
    dest_dir = filedialog.askdirectory(title="选择文件夹 b")
    dest_entry.delete(0, tk.END)
    dest_entry.insert(0, dest_dir)

def on_run():
    src_dir = src_entry.get()
    dest_dir = dest_entry.get()
    suffix = suffix_entry.get()
    
    if not os.path.isdir(src_dir) or not os.path.isdir(dest_dir):
        messagebox.showerror("错误", "请确保选择有效的文件夹路径！")
        return
    
    rename_and_copy_files(src_dir, dest_dir, suffix)

# 创建主窗口
root = tk.Tk()
root.title("文件重命名与复制工具")

# 创建并放置文件夹 a 的路径输入框和按钮
tk.Label(root, text="视频路径:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
src_entry = tk.Entry(root, width=50)
src_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="浏览...", command=select_src_dir).grid(row=0, column=2, padx=10, pady=5)

# 创建并放置文件夹 b 的路径输入框和按钮
tk.Label(root, text="字幕路径:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
dest_entry = tk.Entry(root, width=50)
dest_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="浏览...", command=select_dest_dir).grid(row=1, column=2, padx=10, pady=5)

# 创建并放置后缀输入框
tk.Label(root, text="字幕后缀:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
suffix_entry = tk.Entry(root, width=50)
suffix_entry.insert(0, ".chs")  # 设置默认后缀
suffix_entry.grid(row=2, column=1, padx=10, pady=5)

# 创建并放置运行按钮
tk.Button(root, text="运行", command=on_run).grid(row=3, column=1, padx=10, pady=20)

# 启动主事件循环
root.mainloop()
