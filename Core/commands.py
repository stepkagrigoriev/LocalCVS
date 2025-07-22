import sys
import os
import zlib
from .repository import Repository
from .repository import RepositoryError
from .buffer import Buffer
from .commit import Commit
from .branch import Branch
from .tag import Tag

available_commands = ['init', 'add', 'commit', 'reset', 'log', 'tag', 'branch']


def run_command(command, args):
    if command == 'init':
        if len(args) != 1:
            print('Usage: LocalCVS init .')
            sys.exit(1)
        init()
    elif command == 'add':
        if len(args) == 0:
            print('Usage: LocalCVS add [file_names]')
            sys.exit(1)
        add_files(args)
    elif command == 'commit':
        if len(args) == 1 or args[0] != '-m':
            print('Usage: LocalCVS commit -m <your description>')
            sys.exit(1)
        commit_changes(' '.join(args[1::]))
    elif command == 'reset':
        if len(args) == 0:
            print('Usage: LocalCVS reset <commit-sha>')
            sys.exit(1)
        reset_to(args[0])
        print(f'Reset to {args[0]}')
    elif command == 'log':
        if len(args) != 0:
            print('Usage: LocalCVS log')
            sys.exit(1)
        log_commits()
    elif command == 'tag':
        tag(args)
    elif command == 'branch':
        branch(args)
    else:
        print(args)
        print(f'Unknown command: {command}')
        print(f'Available commands: {', '.join(available_commands)}')
        sys.exit(1)


def init():
    try:
        repo = Repository('.')
        repo.init()
        print(f'Initialized empty LocalCVS repo in {repo.cvsdir}')
    except RepositoryError as e:
        print(f'RepositoryError: {e}')
        sys.exit(1)


def add_files(file_paths):
    repo = Repository(Repository.find_repo_root('.'))
    buffer = Buffer(repo)
    buffer.read()
    if file_paths == ['.']:
        for dirpath, dirname, filenames in os.walk(repo.worktree):
            if '.cvs' in dirname:
                dirname.remove('.cvs')
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                buffer.add(full_path)
        print("Added all files")
    else:
        for path in file_paths:
            try:
                buffer.add(path)
                print(f'Added {len(file_paths)} files to buffer area')
            except FileNotFoundError:
                print(f'Repository Error: File {path} not found!')
                sys.exit(1)
    buffer.write()


def commit_changes(text):
    repo = Repository(Repository.find_repo_root('.'))
    buffer = Buffer(repo)
    buffer.read()
    commit = Commit(repo, buffer.entries, text)
    print(f'Commited: {commit.write()}')


def reset_to(commit_sha):
    repo = Repository(Repository.find_repo_root('.'))
    sha_key, sha_value = commit_sha[:2], commit_sha[2:]
    commit_path = os.path.join(repo.cvsdir, 'objects', sha_key, sha_value)
    if not os.path.isfile(commit_path):
        raise RepositoryError(f'Repository Error: Commit {commit_sha} not found')
    Branch.update_head(repo, commit_sha)
    index = os.path.join(repo.cvsdir, 'index')
    if os.path.exists(index):
        os.remove(index)


def log_commits():
    repo = Repository(Repository.find_repo_root('.'))
    sha = Branch.get_head(repo)
    if not sha:
        print('Repository Error: There\'s no commits in repo!')
    while sha:
        key, data = sha[:2], sha[2:]
        with open(os.path.join(repo.cvsdir, 'objects', key, data), 'rb') as f:
            lines = zlib.decompress(f.read()).decode().splitlines()
        message = ''
        for line in lines:
            if line.startswith('message '):
                message = line[8::]
                break
        print(f'commit {sha}\n       {message}\n')
        prev = None
        for line in lines:
            if line.startswith('parent '):
                prev = line[7::]
                break
        sha = prev


def tag(flags):
    repo = Repository(Repository.find_repo_root('.'))
    if not flags:
        for t in Tag.list_tags(repo):
            print(f'{t}: {Tag.get_tag_commit(repo, t)}')
    elif flags[0] == '-d':
        if len(flags) == 1:
            print('Repository Error: no tag name to delete')
        try:
            Tag.delete_tag(repo, flags[1])
            print(f'Tag {flags[1]} deleted')
        except FileNotFoundError:
            print(f'Repository Error: Tag {flags[1]} not found')
    else:
        sha = flags[1] if len(flags) > 1 else None
        try:
            Tag.create_tag(repo, flags[0], sha)
            print(f'Tag {flags[0]} created')
        except FileExistsError:
            print(f'Repository Error: Tag {flags[0]} already exists')


def branch(flags):
    repo = Repository(Repository.find_repo_root('.'))
    if not flags:
        current_branch = Branch.get_head_ref(repo).split('/')[-1]
        for branch_name in os.listdir(os.path.join(repo.cvsdir, 'refs', 'heads')):
            if branch_name == current_branch:
                print(f'* {branch_name}')
            else:
                print(f'  {branch_name}')
    else:
        path = os.path.join(repo.cvsdir, 'refs', 'heads', flags[0])
        if os.path.exists(path):
            print(f'Repository Error: Branch {flags[0]} already exists.')
        else:
            sha = Branch.get_head(repo)
            with open(path, 'w') as f:
                f.write(sha)
            print(f'Branch {flags[0]} created at {sha}')
