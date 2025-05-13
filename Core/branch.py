import os
from .repository import Repository

class Branch:
    @staticmethod
    def get_head_ref(repo : Repository):
        with open(os.path.join(repo.cvsdir, 'HEAD'), 'r') as f:
            ref = f.read().strip()
        return ref

    @staticmethod
    def update_head(repo : Repository, sha : str):
        ref_path = os.path.join(repo.cvsdir, Branch.get_head_ref(repo))
        with open(ref_path, 'w', encoding='utf-8') as f:
            f.write(sha)

    @staticmethod
    def get_head(repo : Repository):
        ref_path = os.path.join(repo.cvsdir, Branch.get_head_ref(repo))
        if os.path.exists(ref_path):
            with open(ref_path, 'r') as f:
                head = f.read().strip()
            return head
        return None
