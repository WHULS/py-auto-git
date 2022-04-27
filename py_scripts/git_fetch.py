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


def green(str: str):
    return '\x1b[32m{:s}\x1b[0m'.format(str)


def yellow(str: str):
    return '\x1b[33m{:s}\x1b[0m'.format(str)


def blue(str: str):
    return '\x1b[96m{:s}\x1b[0m'.format(str)


def gray(str: str):
    return '\x1b[90m{:s}\x1b[0m'.format(str)


def get_config(repo: git.Repository,
               key: str):
    try:
        val: str = repo.config.__getitem__(key)
        return val
    except:
        print('获取配置[{:s}]失败，请通过以下命令配置：'.format(key))
        print('git config --global {:s}=[...]'.format(key))
        return None


def get_remote_list(repo: git.Repository):
    return [remote.name for remote in repo.remotes]


if __name__ == '__main__':
    # 读取仓库信息
    repo_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    try:
        repo = git.Repository(repo_path)
    except:
        print(red('[{:s}]不是一个git仓库').format(repo_path))
        exit()

    # 远程仓库名称列表
    remote_list = get_remote_list(repo)

    if len(remote_list) > 0:
        for remote_name in remote_list:
            print('**********获取远程分支[{:s}]**********'.format(gray(remote_name)))
            cmd = 'git fetch {:s}'.format(remote_name)
            print(green('执行命令：') + '[{:s}]'.format(gray(cmd)))
            os.system('cd {repo_path} && {cmd}'.format(
                repo_path=repo_path, cmd=cmd))
            print(yellow('ok'))
    else:
        print(yellow('没有远程分支'))
    
    print('**********所有分支**********')
    os.system('cd {repo_path} && git branch -v -a'.format(repo_path=repo_path))