import os

"""
Класс Repository для работы с CVS
"""
class Repository:
    def __init__(self, path):
        self.worktree = path
        self.cvsdir = os.path.join(path, '.cvs')

    """
    Создаёт структуру .cvs/ и директории в ней
    """
    def init(self):
        os.makedirs(self.cvsdir)
        os.makedirs(os.path.join(self.cvsdir, 'objects'))
        os.makedirs(os.path.join(self.cvsdir, 'references', 'heads'))
        os.makedirs(os.path.join(self.cvsdir, 'HEAD'))
        HEAD = os.path.join(self.cvsdir, 'HEAD')
        with open(HEAD, 'w', encoding='utf-8') as f:
            f.write('references/heads/master')
