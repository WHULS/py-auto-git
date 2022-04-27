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


def get_all_branch(repo: git.Repository):
    return [name for name in repo.branches]


def get_current_branch(repo: git.Repository):
    for name in repo.branches.local:
        branch = repo.lookup_branch(name)
        if branch.is_head():
            bName: str = branch.branch_name
            return bName
    return None


if __name__ == '__main__':
    # 读取仓库信息
    repo_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    try:
        repo = git.Repository(repo_path)
    except:
        print(red('[{:s}]不是一个git仓库').format(repo_path))
        exit()

    # 若仓库存在更改则不允许merge
    status = [item for item in repo.status().items() if item[1] != 16384]
    if len(list(status)) != 0:
        print('仓库[{:s}]存在更改，请先提交'.format(yellow(repo_path)))
        exit()

    # 当前分支
    cur = get_current_branch(repo)
    if not cur:
        print(red('当前分支读取错误（可能不是本地分支）'))
        exit()

    print('**********当前分支**********')
    cur_branch = repo.branches[cur]
    print('- {cur_branch_name}\t{hash} {msg}'.format(
        cur_branch_name=green(cur),
        hash=gray(str(cur_branch.target)[0:7]),
        msg=repo[cur_branch.target].message
    ))

    # 所有分支名称
    all = get_all_branch(repo)

    # 当前分支外的信息
    all_info = []
    for name in all:
        if name == cur:
            continue

        b = repo.branches[name]
        all_info.append([name, str(b.target)[0:7], repo[b.target].message])

    print('**********请选择一个分支合并到当前**********')
    for idx in range(0, len(all_info)):
        print('{id} {branch}\t{hash} {msg}'.format(
            id=red('{:d}').format(idx),
            branch=yellow(all_info[idx][0]),
            hash=gray(all_info[idx][1]),
            msg=(all_info[idx][2])
        ))

    try:
        idx = int(input('请输入：'))
        if idx < 0 or idx >= len(all_info):
            raise Exception('序号不在范围内')
    except Exception as e:
        print(e)
        exit()

    os.system('git merge {:s}'.format(all_info[idx][0]))
    print(yellow('ok'))
