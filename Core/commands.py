import sys
import os
import zlib
from .repository import Repository
from .repository import RepositoryError
from .buffer import Buffer
from .commit import Commit
from .branch import Branch
from .tag import Tag

available_commands = ['init', 'add', 'commit', 'reset', 'log', 'tag']


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
    else:
        print(args)
        print(f'Unknown command: {command}')
        print(f"Available commands: {', '.join(available_commands)}")
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
    for path in file_paths:
        try:
            buffer.add(path)
        except FileNotFoundError:
            print(f'File {path} not found!')
            sys.exit(1)
    buffer.write()
    print(f'Added {len(file_paths)} files to buffer area')


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
        raise RepositoryError(f'Commit {commit_sha} not found')
    Branch.update_head(repo, commit_sha)
    index = os.path.join(repo.cvsdir, 'index')
    if os.path.exists(index):
        os.remove(index)


def log_commits():
    repo = Repository(Repository.find_repo_root('.'))
    sha = Branch.get_head(repo)
    if not sha:
        print('There\'s no commits in repo!')
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
        previous = None
        for line in lines:
            if line.startswith('parent '):
                previous = line[7::]
                break
        sha = previous


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
        except RepositoryError:
            print(f'Tag {flags[1]} not found')
    else:
        sha = flags[1] if len(flags) > 1 else None
        try:
            Tag.create_tag(repo, flags[0], sha)
            print(f'Tag {flags[0]} created')
        except RepositoryError:
            print(f'Tag {flags[0]} already exists')
