from .object_store import ObjectStore
from .branch import Branch
from .repository import RepositoryError
import time


class Commit:
    def __init__(self, repo, entries, message, parent=None, 
                 author=None, creation_time=None):
        self.repo = repo
        self.entries = entries
        self.message = message
        self.parent = parent
        self.author = author
        if creation_time:
            self.creation_time = int(creation_time)
        else:
            self.creation_time = time.time()

    def write(self):
        tree_data = b''
        for path, sha in self.entries.items():
            tree_data += f'{sha} {path}\n'.encode('utf-8')
        tree_sha = ObjectStore(self.repo).write_object('tree', tree_data)
        lines = [f'tree {tree_sha}', f'author {self.author}',
                f'time {self.creation_time}', f'message {self.message}']
        if self.parent:
            lines.append(f"parent {self.parent}")
        name = ('\n'.join(lines) + '\n').encode('utf-8')
        sha = ObjectStore(self.repo).write_object('commit', name)
        Branch.update_head(self.repo, sha)
        return sha

    def load(repo, sha):
        obj_type, raw = ObjectStore(repo).read_object(sha)
        if obj_type != 'commit':
            raise RepositoryError('Not a commit')
        text = raw.decode('utf-8')
        tree,parent,author,creation_time = None,None,None,None
        message = ""
        for l in text.splitlines():
            if l.startswith('tree '):
                tree = l.split(' ', 1)[1]
            elif l.startswith('parent '):
                parent = l.split(' ', 1)[1]
            elif l.startswith('author '):
                author = l.split(' ', 1)[1]
            elif l.startswith('time '):
                creation_time = l.split(' ', 1)[1]
            elif l.startswith('message '):
                message = l[8:]
        entries = {}
        if tree:
            obj_type2, tree_raw = ObjectStore(repo).read_object(tree)
            if obj_type2 != 'tree':
                raise RepositoryError('Tree object expected')
            for l in tree_raw.decode('utf-8').splitlines():
                sha, path = l.split(' ', 1)
                entries[path] = sha
        return Commit(repo, entries, message, parent=parent,
                     author=author, creation_time=creation_time)

