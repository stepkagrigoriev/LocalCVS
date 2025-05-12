from Core.object_store import ObjectStore
from Core.branch import Branch
from Core.repository import Repository

class Commit:
    def __init__(self, repo : Repository, entries : dict, message : str):
        self.repo = repo
        self.entries = entries
        self.message = message

    def write(self):
        # 1) build tree object
        data = b''
        for path, sha in self.entries.items():
            data += f"{sha} {path}\n".encode()
        tree = ObjectStore(self.repo).hash_object(data, 'tree')
        content = f"tree {tree}\n"
        prev = Branch.get_head(self.repo)
        if prev:
            content += f"parent {prev}\n"
        content += f"message {self.message}\n"

        sha = ObjectStore(self.repo).hash_object(content.encode(), 'commit')
        Branch.update_head(self.repo, sha)
        return sha