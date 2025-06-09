from .object_store import ObjectStore
from .branch import Branch
from .repository import Repository
import os
import shutil

class Commit:
    def __init__(self, repo, entries, message, parent=None):
        self.repo = repo
        self.entries = entries
        self.message = message
        self.parent = parent

    def write(self):
        data = b''
        for path, sha in self.entries.items():
            data += f'{sha} {path}\n'.encode()
        tree = ObjectStore(self.repo).hash_object(data, 'tree')
        content = f'tree {tree}\n'
        if self.parent:
            content += f'parent {self.parent}\n'
        content += f'message {self.message}\n'
        sha = (ObjectStore(self.repo)
               .hash_object(content.encode(), 'commit'))
        Branch.update_head(self.repo, sha)
        return sha

    def restore_working_directory(self):
        for obj in os.listdir(self.repo.worktree):
            if obj != '.cvs':
                path = os.path.join(self.repo.worktree, obj)
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
        store = ObjectStore(self.repo)
        for path, sha in self.entries.items():
            dir_name = os.path.join(self.repo.worktree, path)
            os.makedirs(os.path.dirname(dir_name), exist_ok=True)
            with open(dir_name, 'wb') as f:
                f.write(store.read_object(sha))

    @staticmethod
    def load(repo, sha):
        raw_text = ObjectStore(repo).read_object(sha)
        tree_sha = None
        message = ''
        parent = None
        for line in raw_text.decode().splitlines():
            if line.startswith('tree '):
                tree_sha = line.split()[1]
            elif line.startswith('parent '):
                parent = line.split()[1]
            elif line.startswith('message '):
                message = line[8:]
        tree_raw = ObjectStore(repo).read_object(tree_sha).decode()
        entries = {}
        for l in tree_raw.splitlines():
            sha_obj, path = l.split(' ', 1)
            entries[path] = sha_obj
        return Commit(repo, entries, message, parent)
