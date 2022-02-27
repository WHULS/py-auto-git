import time
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


def get_current_branch(repo: git.Repository):
    for name in repo.branches.local:
        branch = repo.lookup_branch(name)
        if branch.is_head():
            bName: str = branch.branch_name
            return bName
    return None


if __name__ == '__main__':
    bFull = input('是否完整显示? [y/N]')
    bFull = True if bFull == 'y' else False

    # 读取仓库信息
    repo_path = os.getcwd()
    try:
        repo = git.Repository(repo_path)
    except:
        print(red('[{:s}]不是一个git仓库').format(repo_path))
        exit()

    if repo.head_is_unborn:
        print(gray('该仓库未发生过提交'))
        exit()

    last = repo[repo.head.target]
    i = 1
    for commit in repo.walk(last.id, git.GIT_SORT_TIME | git.GIT_SORT_REVERSE):
        hash = blue(str(commit.id)[0:10] + '...')
        _time = yellow(time.strftime('%Y年%m月%d日 %H:%M:%S',
                                     time.localtime(commit.commit_time)))
        name = commit.author.name
        email = commit.author.email

        diff = repo.diff(commit.id, commit.parent_ids[0] if len(
            commit.parent_ids) > 0 else '4b825dc642cb6eb9a060e54bf8d69288fbee4904')
        new_lines = 0
        rmv_lines = 0
        files_changed = [[], [], []]
        for patch in diff:
            # ([更改的行的前后留白位置], [删除的行数], [新增的行数])
            line_stat = patch.line_stats
            new_lines += line_stat[2]
            rmv_lines += line_stat[1]

            line_modi = '{:s} {:s}'.format(green('+{:d}'.format(line_stat[2])), red(
                '-{:d}'.format(line_stat[1]))) if patch.delta.is_binary == False else ''

            if bFull:  # 完整显示
                if patch.delta.status == 2:  # create
                    files_changed[0].append('* {type} {file} {line_modi}'.format(
                        file=gray(patch.delta.new_file.path),
                        type=green('create'),
                        line_modi=line_modi)
                    )
                elif patch.delta.status == 1:  # delete
                    files_changed[2].append('* {type} {file} {line_modi}'.format(
                        file=gray(patch.delta.new_file.path),
                        type=red('delete'),
                        line_modi=line_modi)
                    )
                else:  # modify and other
                    files_changed[1].append('* {type} {file} {line_modi}'.format(
                        file=gray(patch.delta.new_file.path),
                        type=yellow('modify'),
                        line_modi=line_modi)
                    )

        files_changed = files_changed[0] + files_changed[1] + files_changed[2]

        msg = commit.message.replace('\n', '')
        print(
            '{id}. {hash} {time} {author} {new_lines} {rmv_lines} {msg}'.format(
                id=i, hash=hash, time=_time, msg=msg,
                author=gray('{name}[{email}]'.format(name=name, email=email)),
                new_lines=green('+{:d}'.format(new_lines)),
                rmv_lines=red('-{:d}'.format(rmv_lines)),
            )
        )
        i += 1
        for item in files_changed:
            print(' ', item)
