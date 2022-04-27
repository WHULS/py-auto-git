import sys
from colorama import init
import os
import pygit2 as git

# 处理命令行输入中文
import locale
locale.setlocale(locale.LC_CTYPE, 'chinese')

# 处理cmd颜色
init(autoreset=True)


def red(str: str):
    return '\x1b[31m{:s}\x1b[0m'.format(str)


if __name__ == '__main__':
    # 读取仓库信息
    repo_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    try:
        repo = git.Repository(repo_path)
    except:
        print(red('[{:s}]不是一个git仓库').format(repo_path))
        exit()

    os.system('cd {repo_path} && git branch -v -a'.format(repo_path=repo_path))
