import os
from Core.repository import Repository

class Branch:

    @staticmethod
    def get_head_ref(repo : Repository):
        return open(os.path.join(repo.cvsdir, 'HEAD'), 'references').read().strip()

    @staticmethod
    def get_head(repo : Repository):
        ref_path = os.path.join(repo.cvsdir, Branch.get_head_ref(repo))
        if os.path.exists(ref_path):
            return open(ref_path, 'references').read().strip()
        return None

    @staticmethod
    def update_head(repo : Repository, sha):
        ref_path = os.path.join(repo.cvsdir, Branch.get_head_ref(repo))
        with open(ref_path, 'w', encoding='utf-8') as f:
            f.write(sha)