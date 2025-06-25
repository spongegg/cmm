import os
import shutil
import time
import tkinter as tk
from tkinter import filedialog, messagebox

class SubtitleRenamer:
    def __init__(self):
        self.language_suffix = "zh"

    def match_files(self, videos, subtitles):
        return list(zip(videos, subtitles))

    def get_new_subtitle_path(self, video, subtitle):
        base = os.path.splitext(os.path.basename(video))[0]
        ext = os.path.splitext(subtitle)[1]
        filename = f"{base}.{self.language_suffix}{ext}"
        return os.path.join(os.path.dirname(video), filename)

    def safe_copy_remove(self, src, dst, retries=3, delay=1):
        for i in range(retries):
            try:
                shutil.copy2(src, dst)
                os.remove(src)
                return
            except Exception as e:
                if i == retries - 1:
                    raise
                time.sleep(delay)

    def rename_files(self):
        while True:
            suffix = input("请输入字幕语言后缀（回车默认 zh）：").strip()
            if suffix:
                self.language_suffix = suffix
            else:
                self.language_suffix = "zh"

            root = tk.Tk()
            root.withdraw()

            videos = filedialog.askopenfilenames(title="选择视频文件",
                                                 initialdir=os.path.expanduser("~"),
                                                 filetypes=[("视频文件", "*.mp4 *.avi *.mkv *.mov")])
            if not videos:
                print("未选择视频文件，退出。")
                return False  # 退出循环

            subtitles = filedialog.askopenfilenames(title="选择字幕文件",
                                                    initialdir=os.path.expanduser("~"),
                                                    filetypes=[("字幕文件", "*.srt *.ass *.vtt")])
            if not subtitles:
                print("未选择字幕文件，退出。")
                return False  # 退出循环

            if len(videos) != len(subtitles):
                vlist = "\n".join(os.path.basename(v) for v in videos)
                slist = "\n".join(os.path.basename(s) for s in subtitles)
                msg = (f"⚠️ 视频文件数({len(videos)})与字幕文件数({len(subtitles)})不一致！\n\n"
                       f"视频文件:\n{vlist}\n\n字幕文件:\n{slist}\n\n是否继续？")
                if not messagebox.askyesno("数量不一致", msg):
                    return False  # 退出循环

            pairs = self.match_files(videos, subtitles)
            if not pairs:
                messagebox.showwarning("未找到匹配", "没有匹配的文件。")
                return False  # 退出循环

            confirm_text = "\n".join(f"{os.path.basename(v)} <--> {os.path.basename(s)}" for v, s in pairs)
            if not messagebox.askyesno("确认重命名", f"将重命名以下文件：\n{confirm_text}"):
                return False  # 退出循环

            renamed = 0
            dirs_to_check = set()

            for vfile, sfile in pairs:
                try:
                    new_path = self.get_new_subtitle_path(vfile, sfile)
                    self.safe_copy_remove(sfile, new_path)
                    renamed += 1
                    dirs_to_check.add(os.path.dirname(sfile))
                except Exception as e:
                    messagebox.showerror("错误", f"处理失败：\n{sfile}\n\n错误：{e}")

            for folder in dirs_to_check:
                try:
                    if os.path.isdir(folder) and not os.listdir(folder):
                        os.rmdir(folder)
                except Exception as e:
                    print(f"删除文件夹失败 {folder}：{e}")

            messagebox.showinfo("完成", f"成功重命名 {renamed} 个字幕文件！")

            while True:
                choice = input("输入1继续重命名，输入2结束程序: ").strip()
                if choice == "1":
                    break  # 继续外层循环，回到输入语言后缀开始
                elif choice == "2":
                    return False  # 退出循环，结束程序
                else:
                    print("无效输入，请输入1或2。")

if __name__ == "__main__":
    app = SubtitleRenamer()
    app.rename_files()
