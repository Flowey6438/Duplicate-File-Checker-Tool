import os
import hashlib

def calculate_file_hash(file_path, block_size=65536):
    """计算文件的哈希值"""
    hash_algo = hashlib.sha256()
    try:
        with open(file_path, "rb") as file:
            while chunk := file.read(block_size):
                hash_algo.update(chunk)
        return hash_algo.hexdigest()
    except FileNotFoundError:
        return None

def find_duplicate_files(directory):
    """查找指定目录中的重复文件"""
    file_hashes = {}
    duplicates = []

    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_hash = calculate_file_hash(file_path)
            if file_hash:
                if file_hash in file_hashes:
                    duplicates.append((file_path, file_hashes[file_hash]))
                else:
                    file_hashes[file_hash] = file_path

    return duplicates

def delete_files(file_paths):
    """删除指定的文件"""
    for file_path in file_paths:
        try:
            os.remove(file_path)
            print(f"已删除：{file_path}")
        except FileNotFoundError:
            print(f"文件未找到：{file_path}")
        except Exception as e:
            print(f"无法删除文件 {file_path}：{e}")

if __name__ == "__main__":
    print("欢迎使用文件重复检查工具！")

    directory = input("请输入要检查的目录路径：").strip()
    if not os.path.isdir(directory):
        print("输入的路径无效或不是一个目录。")
    else:
        duplicates = find_duplicate_files(directory)
        if duplicates:
            print("\n找到以下重复文件：")
            for i, (dup, orig) in enumerate(duplicates, 1):
                print(f"{i}. 重复文件：{dup} | 原始文件：{orig}")

            choice = input("\n是否删除所有重复文件？（y/n）：").lower()
            if choice == "y":
                delete_files([dup for dup, _ in duplicates])
            else:
                print("未删除任何文件。")
        else:
            print("未找到任何重复文件。")
