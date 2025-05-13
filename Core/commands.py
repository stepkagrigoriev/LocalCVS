import sys, os
import zlib

from .repository import Repository, RepositoryError
from .buffer import Buffer
from .commit import Commit
from .branch import Branch

available_commands = ['init', 'add', 'commit', 'reset', 'log']

def run_command(command : str, args : list[str]):
    if command == 'init':
        if len(args) != 1:
            print('Usage: cvs init <repo-name>')
            sys.exit(1)
        init(args[0])
    elif command == 'add':
        if len(args) == 0:
            print('Usage: cvs add [file_names]')
            sys.exit(1)
        add_files(args)
    elif command == 'commit':
        if len(args) == 1 or args[0] != '-m':
            print('Usage: cvs commit -m <your description>')
            sys.exit(1)
        commit_changes(' '.join(args[1::]))
    elif command == 'reset':
        if len(args) == 0:
            print('Usage: cvs reset <commit-sha>')
            sys.exit(1)
        reset_to(args[0])
        print(f'Reset to {args[0]}')
    elif command == 'log':
        if len(args) != 0:
            print('Usage: cvs log')
            sys.exit(1)
        log_commits()
    else:
        print(args)
        print(f'Unknown command: {command}')
        print(f'Available commands: {', '.join(available_commands)}')
        sys.exit(1)


def init(repo_name : str):
    try:
        repo = Repository(repo_name)
        repo.init()
        print(f'Initialized empty LocalCVS repo in {repo.cvsdir}')
    except RepositoryError as e:
        print(f'RepositoryError: {e}')
        sys.exit(1)


def add_files(file_paths : list[str]):
    repo = Repository('.')
    buffer = Buffer(repo)
    buffer.read()
    for path in file_paths:
        buffer.add(path)
    buffer.write()
    print(f'Added {len(file_paths)} files to buffer area')

def commit_changes(text : str):
    repo = Repository('.')
    buffer = Buffer(repo)
    buffer.read()
    commit = Commit(repo, buffer.entries, text)
    print(f'Commited: {commit.write()}')

def reset_to(commit_sha : str):
    repo = Repository('.')
    sha_key, sha_value = commit_sha[:2], commit_sha[2:]
    commit_path = os.path.join(repo.cvsdir, 'objects', sha_key, sha_value)
    if not os.path.isfile(commit_path):
        raise RepositoryError(f'Commit {commit_sha} not found')
    Branch.update_head(repo, commit_sha)
    index = os.path.join(repo.cvsdir, 'index')
    if os.path.exists(index):
        os.remove(index)

def log_commits():
    repo = Repository('.')
    sha = Branch.get_head(repo)
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
