import os
from .repository import Repository, RepositoryError


class Branch:
    @staticmethod
    def get_head_ref(repo):
        ref = Repository.find_repo_root(repo.worktree)
        path = os.path.join(ref, '.cvs', 'HEAD')
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()

    @staticmethod
    def update_head(repo, sha):
        ref = Repository.find_repo_root(repo.worktree)
        path = os.path.join(ref, '.cvs', Branch.get_head_ref(repo))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(sha)

    @staticmethod
    def get_head(repo):
        ref = Branch.get_head_ref(repo)
        path = os.path.join(repo.cvsdir, ref)
        if os.path.exists(path):
            return open(path, 'r', encoding='utf-8').read().strip() 
        return None
    
    @staticmethod
    def create(repo, name, target_sha=None):
        if not target_sha and not Branch.get_head(repo):
            raise RepositoryError('Cannot create branch: no commits yet')
        elif not target_sha:
            target_sha = Branch.get_head(repo)
        path = os.path.join(repo.cvsdir, 'refs', 'heads', name)
        if os.path.exists(path):
            raise RepositoryError('Branch already exists')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(target_sha)
    
    @staticmethod
    def get_current_branch(repo):
        ref = Branch.get_head_ref(repo)
        prefix = 'refs/heads/'
        if ref.startswith(prefix):
            return ref[len(prefix):]
        return None
