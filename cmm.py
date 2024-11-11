import os
import shutil

def rename_files_with_suffix(src_dir, dest_dir, suffix=""):
    # 获取两个文件夹中的文件列表
    src_files = sorted(os.listdir(src_dir))
    dest_files = sorted(os.listdir(dest_dir))

    # 确保两个文件夹中的文件数量相同
    if len(src_files) != len(dest_files):
        print("Error: 两个文件夹中的文件数量不相同！")
        return

    for src_file, dest_file in zip(src_files, dest_files):
        # 获取文件的原扩展名
        dest_ext = os.path.splitext(dest_file)[1]
        
        # 构造新的文件名（包含后缀）
        new_name = os.path.splitext(src_file)[0] + suffix + dest_ext
        
        # 获取完整路径
        src_path = os.path.join(src_dir, src_file)
        dest_path = os.path.join(dest_dir, dest_file)
        new_dest_path = os.path.join(dest_dir, new_name)
        
        # 重命名文件夹b中的文件
        os.rename(dest_path, new_dest_path)
        print(f"重命名 {dest_file} 为 {new_name}")

        # 复制重命名后的文件到文件夹 a 中
        new_src_path = os.path.join(src_dir, new_name)
        shutil.copy2(new_dest_path, new_src_path)

# 示例用法
src_dir = 'C:Users\Sponge\Videosa'  # 文件夹 a 的路径
dest_dir = 'C:\Users\Sponge\Pictures\b' # 文件夹 b 的路径
suffix = ".chs" # 想要添加的后缀

rename_files_with_suffix(src_dir, dest_dir, suffix)
