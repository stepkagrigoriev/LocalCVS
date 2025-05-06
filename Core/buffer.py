import os
from Core.object_store import ObjectStore
from Core.repository import Repository

class Buffer:
    def __init__(self, repo : Repository):
        self.index = os.path.join(repo.cvsdir, 'index')
        self.entries = {}
        self.repo = repo

    def read(self):
        if os.path.exists(self.index):
            with open(self.index, 'r', encoding='utf-8') as f:
                for line in f:
                    sha, path = line.strip().split(' ', 1)
                    self.entries[path] = sha

    def write(self):
        with open(self.index, 'w', encoding='utf-8') as f:
            for path, sha in self.entries.items():
                f.write(f"{sha} {path}\n")

    def add(self, file_path : str):
        store = ObjectStore(self.repo)
        with open(file_path, 'rb') as f:
            data = f.read()
        sha = store.hash_object(data, 'blob')
        self.entries[file_path] = sha
