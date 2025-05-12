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
        os.makedirs(os.path.join(self.cvsdir, 'references', 'heads'), exist_ok=True)
        with open(head, 'w', encoding='utf-8') as f:
            f.write('references/heads/master')