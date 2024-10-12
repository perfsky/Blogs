import os
import subprocess
import sys
from datetime import datetime

# 获取当前日期和时间
current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

# 检查是否提供了提交信息
commit_message = "Update " + current_time if len(sys.argv) == 1 else sys.argv[1]

# 定义执行命令的函数
def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result

# 处理 public 目录的变更
def handle_public_directory():
    os.chdir("public")
    
    # 执行 git status
    print("Running git status in 'public' directory...")
    run_command(["git", "status"])

    # 添加所有变更
    print("Adding changes in 'public' directory...")
    run_command(["git", "add", "."])

    # 提交变更
    print(f"Committing changes in 'public' directory with message: {commit_message}")
    run_command(["git", "commit", "-m", commit_message])

    # 推送到远程仓库
    print("Pushing changes in 'public' directory to origin main...")
    run_command(["git", "push", "origin", "main"])

    os.chdir("..")

# 处理根目录的变更
def handle_root_directory():
    # 执行 git status
    print("Running git status in root directory...")
    run_command(["git", "status"])

    # 添加所有变更
    print("Adding changes in root directory...")
    run_command(["git", "add", "."])

    # 提交变更
    print(f"Committing changes in root directory with message: {commit_message}")
    run_command(["git", "commit", "-m", commit_message])

    # 推送到远程仓库
    print("Pushing changes in root directory to origin main...")
    run_command(["git", "push", "origin", "main"])

# 脚本执行过程
if __name__ == "__main__":
    # 确保 public 目录存在并是子模块
    if os.path.exists("public"):
        print("Handling changes in 'public' directory...")
        handle_public_directory()

    # 处理根目录的变更
    print("Handling changes in root directory...")
    handle_root_directory()



# import os
# import subprocess
# import sys
# from datetime import datetime

# # 获取当前日期和时间
# current_time = datetime.now().strftime("%Y-%m-%d-%H-%M")

# # 检查是否提供了提交信息
# commit_message = "Update " + current_time if len(sys.argv) == 1 else sys.argv[1]

# # 定义函数：检查是否有变更，并执行 git 提交和推送
# def check_and_commit(directory):
#     print(f"检查目录 {directory} 下的变更...")

#     # 切换到指定目录
#     os.chdir(directory)

#     # 检查 git 状态是否有变更
#     result = subprocess.run(["git", "status", "--porcelain"], stdout=subprocess.PIPE)

#     if result.returncode == 0 and result.stdout:
#         # 如果有变更，执行 git add 和 commit
#         print("有变更，准备提交...")
#         subprocess.run(["git", "add", "."])
#         subprocess.run(["git", "commit", "-m", commit_message])
#         subprocess.run(["git", "push", "origin", "main"])
#     else:
#         print("无变更，跳过此目录的提交操作。")

# # 在根目录执行 git 操作
# root_directory = os.getcwd()
# print("执行根目录下的 Git 操作...")
# check_and_commit(root_directory)

# # 执行 hugo 命令
# print("执行 Hugo 生成静态文件...")
# subprocess.run(["hugo", "-t", "hextra", "--ignoreCache"])

# # 转到 public 目录执行相同的 git 操作
# public_directory = os.path.join(root_directory, "public")
# print("执行 public 目录下的 Git 操作...")
# check_and_commit(public_directory)
