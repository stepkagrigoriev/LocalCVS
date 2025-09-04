import os
from .object_store import ObjectStore


class Buffer:
    def __init__(self, repo):
        self.index = os.path.join(repo.cvsdir, 'index')
        self.entries = {}
        self.repo = repo

    def read(self):
        if os.path.exists(self.index):
            with open(self.index, 'r') as f:
                for line in f:
                    sha, path = line.strip().split(' ', 1)
                    self.entries[path] = sha

    def write(self):
        with open(self.index, 'w') as f:
            for path, sha in self.entries.items():
                f.write(f'{sha} {path}\n')

    def add(self, file_path):
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)
        store = ObjectStore(self.repo)
        with open(file_path, 'rb') as f:
            data = f.read()
        sha = store.write_object(data, 'blob')
        self.entries[os.path.relpath(file_path, self.repo.worktree)] = sha
