import os

'''Специальная ошибка для работы с репозиторием'''
class RepositoryError(Exception):
    pass

'''Класс Repository для работы с CVS'''
class Repository:
    def __init__(self, path : str):
        self.worktree = path
        self.cvsdir = os.path.join(path, '.cvs')

    '''Создаёт структуру .cvs/ и директории в ней'''
    def init(self):
        head = os.path.join(self.cvsdir, 'HEAD')
        if os.path.isdir(self.cvsdir) and os.path.exists(head):
            raise RepositoryError('Repository already has been initialized')
        os.makedirs(self.cvsdir, exist_ok=True)
        os.makedirs(os.path.join(self.cvsdir, 'objects'), exist_ok=True)
        os.makedirs(os.path.join(self.cvsdir, 'refs', 'heads'), exist_ok=True)
        with open(head, 'w') as f:
            f.write('refs/heads/master')


    def find_repo_root(self : str):
        path = os.path.abspath(self)
        while True:
            if os.path.isdir(os.path.join(path, '.cvs')):
                return path
            parent = os.path.dirname(path)
            if parent == path:
                raise RepositoryError('No repository found')
            path = parent