import os
from .repository import Repository


class Branch:
    @staticmethod
    def get_head_ref(repo):
        root = Repository.find_repo_root(repo.worktree)
        head_path = os.path.join(root, '.cvs', 'HEAD')
        with open(head_path, 'r') as f:
            return f.read().strip()

    @staticmethod
    def update_head(repo, sha):
        root = Repository.find_repo_root(repo.worktree)
        ref_path = os.path.join(root, '.cvs', Branch.get_head_ref(repo))
        os.makedirs(os.path.dirname(ref_path), exist_ok=True)
        with open(ref_path, 'w') as f:
            f.write(sha)

    @staticmethod
    def get_head(repo):
        root = Repository.find_repo_root(repo.worktree)
        ref_path = os.path.join(root, '.cvs', Branch.get_head_ref(repo))
        if os.path.isfile(ref_path):
            with open(ref_path, 'r') as f:
                return f.read().strip()
        return None
