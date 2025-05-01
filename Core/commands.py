import os
import sys
from Core.repository import Repository, RepositoryError

available_commands = ['init']

def run_command(command : str, args : list[str]):
    if command == 'init':
        if len(args) != 1:
            print('Usage: cvs init <repository-name>')
            sys.exit(1)
        init(args[0])
    else:
        print(f"Unknow command: {command}")
        print(f"Available commands: {', '.join(available_commands)}")
        sys.exit(1)


def init(repo_name):
    try:
        repo = Repository(repo_name)
        repo.init()
        print(f"Initialized empty MyVCS repository in {repo.cvsdir}")
    except RepositoryError as e:
        print(f"RepositoryError: {e}")
        sys.exit(1)


def add():
    pass