import sys
from Core.repository import Repository, RepositoryError
from Core.buffer import Buffer
available_commands = ['init', 'add']

def run_command(command : str, args : list[str]):
    if command == 'init':
        if len(args) != 1:
            print('Usage: cvs init <repository-name>')
            sys.exit(1)
        init(args[0])
    elif command == 'add':
        if len(args) == 0:
            print('Usage: cvs add [files]')
            sys.exit(1)
        add_files(args)
    else:
        print(f'Unknown command: {command}')
        print(f'Available commands: {', '.join(available_commands)}')
        sys.exit(1)


def init(repo_name : str):
    try:
        repo = Repository(repo_name)
        repo.init()
        print(f'Initialized empty MyVCS repository in {repo.cvsdir}')
    except RepositoryError as e:
        print(f'RepositoryError: {e}')
        sys.exit(1)


def add_files(file_names : list[str]):
    repo = Repository('.')
    buffer = Buffer(repo)
    buffer.read()
    for path in file_names:
        buffer.add(path)
    buffer.write()
    print(f'Added {len(file_names)} files to buffer area')