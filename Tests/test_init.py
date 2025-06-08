import unittest
import os
import shutil
import contextlib
import io
from Core.commands import run_command
from Core.repository import Repository, RepositoryError


class InitTests(unittest.TestCase):
    def setUp(self):
        self.initial_dir = os.getcwd()
        self.test_dir = os.path.join(self.initial_dir, 'test_repo')
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

    def tearDown(self):
        os.chdir(self.initial_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    '''
    Тестим, что инициализировали всю структуру
    '''
    def test_init_creates_structure(self):
        repo = Repository(self.test_dir)
        repo.init()
        path = os.path.join(self.test_dir, '.cvs')
        self.assertTrue(os.path.isdir(path))
        self.assertTrue(os.path.isdir(os.path.join(path, 'objects')))
        self.assertTrue(os.path.isdir(os.path.join(path, 'refs', 'heads')))
        head_file = os.path.join(path, 'HEAD')
        self.assertTrue(os.path.isfile(head_file))
        with open(head_file, 'r') as f:
            self.assertEqual(f.read(), 'refs/heads/master')

    '''
    Тестим, что уже инициализированный репозиторий нельзя ещё раз
    '''
    def test_init_already_initialized_repo(self):
        new_repo = Repository(self.test_dir)
        new_repo.init()
        with self.assertRaises(RepositoryError):
            new_repo.init()

    '''
    Два теста на неправильное число аргументов
    '''
    def test_run_command_init_no_args(self):
        with self.assertRaises(SystemExit) as e:
            with contextlib.redirect_stdout(io.StringIO()):
                run_command('init', [])
        self.assertEqual(e.exception.code, 1)

    def test_run_command_init_a_lot_args(self):
        with self.assertRaises(SystemExit) as cm:
            with contextlib.redirect_stdout(io.StringIO()):
                run_command('init', ['name1', 'name2'])
        self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    unittest.main()
