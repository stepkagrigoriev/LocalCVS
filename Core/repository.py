import os


class RepositoryError(Exception):
    pass


class Repository:
    def __init__(self, path):
        self.worktree = path
        self.cvsdir = os.path.join(path, '.cvs')

    def init(self):
        head = os.path.join(self.cvsdir, 'HEAD')
        if os.path.isdir(self.cvsdir) and os.path.exists(head):
            raise RepositoryError('Repository already has been initialized')
        os.makedirs(self.cvsdir)
        os.makedirs(os.path.join(self.cvsdir, 'objects'))
        os.makedirs(os.path.join(self.cvsdir, 'refs', 'heads'))
        with open(head, 'w') as f:
            f.write('refs/heads/master')

    @staticmethod
    def find_repo_root(root):
        path = os.path.abspath(root)
        while True:
            if os.path.isdir(os.path.join(path, '.cvs')):
                return path
            parent = os.path.dirname(path)
            if parent == path:
                raise RepositoryError('No repository found')
            path = parent
