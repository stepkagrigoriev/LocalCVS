import unittest
import os
import shutil
import io
import zlib

from Core.repository import Repository, RepositoryError
from Core.commands import run_command
from Core.branch import Branch

class CommitTests(unittest.TestCase):
    def setUp(self):
        self.initial_dir = os.getcwd()
        self.test_dir = os.path.join(self.initial_dir, 'test_repo')
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        repo = Repository(self.test_dir)
        repo.init()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.initial_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    '''
    Тестим коммит на неверные аргументы
    '''
    def test_commit_wrong_args(self):
        with self.assertRaises(SystemExit):
            run_command('commit', ['АААА', 'НЕ РАБОТАЕТ'])

    '''
    Коммит без изменений должен создать пустой объект
    '''
    def test_commit_without_staged_files(self):
        run_command('commit', ['-m', 'пустой коммит'])
        sha = Branch.get_head(Repository('.'))
        key, data = sha[:2], sha[2::]
        obj_path = os.path.join('.cvs', 'objects',key, data)
        self.assertTrue(os.path.isfile(obj_path))


    '''
    Тестим, что коммит сохраняет все изменяемые файлы в свой tree
    '''
    def test_commit_includes_staged_files(self):
        with open('f1.txt', 'w') as f:
            f.write('lublu python')
        run_command('add', ['f1.txt'])
        run_command('commit', ['-m', 'add lublu python'])
        sha = Branch.get_head(Repository('.'))
        key, data = sha[:2], sha[2::]
        with open(os.path.join('.cvs', 'objects', key, data), 'rb') as f:
            decomp = zlib.decompress(f.read())
        self.assertIn(b'add lublu python', decomp)

    '''
    Тестим, что коммит сохраняет последовательность изменений 
    (для текущего изменения всегда известно предыдущее)
    '''
    def test_multiple_commits_chain(self):
        with open('f1.txt', 'w') as f:
            f.write('lublu')
        run_command('add', ['f1.txt'])
        run_command('commit', ['-m', 'first'])
        sha1 = Branch.get_head(Repository('.'))
        with open('f1.txt', 'w') as f:
            f.write('python')
        run_command('add', ['f1.txt'])
        run_command('commit', ['-m', 'second'])
        sha2 = Branch.get_head(Repository('.'))

        key, data = sha2[:2], sha2[2::]
        with open(os.path.join('.cvs', 'objects', key, data), 'rb') as f:
            decomp = zlib.decompress(f.read())
        self.assertIn(sha1.encode(), decomp)

if __name__ == '__main__':
    unittest.main()