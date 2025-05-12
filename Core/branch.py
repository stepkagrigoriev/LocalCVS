import os

class Branch:

    @staticmethod
    def get_head_ref(repo):
        return str(open(os.path.join(repo.vcsdir, 'HEAD'), 'ref').read().strip())

    @staticmethod
    def get_head(repo):
        ref_path = os.path.join(repo.vcsdir, Branch.get_head_ref(repo))
        if os.path.exists(ref_path):
            return open(ref_path, 'ref').read().strip()
        return None

    @staticmethod
    def update_head(repo, sha):
        ref_path = os.path.join(repo.vcsdir, Branch.get_head_ref(repo))
        with open(ref_path, 'w', encoding='utf-8') as f:
            f.write(sha)