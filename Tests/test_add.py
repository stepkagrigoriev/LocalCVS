import unittest
import os
import shutil
import contextlib
import io
from Core.commands import run_command
from Core.repository import Repository


class AddTests(unittest.TestCase):
    def setUp(self):
        self.initial_dir = os.getcwd()
        self.test_dir = os.path.join(self.initial_dir, 'test_repo')
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        repo = Repository(self.test_dir)
        repo.init()
        os.chdir(self.test_dir)
        with open('f1.txt', 'w', encoding='utf-8') as f:
            f.write('lublu python')

    def tearDown(self):
        os.chdir(self.initial_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    '''
    Тестим, что в .cvs есть index
    '''
    def test_add_create_index_file(self):
        with contextlib.redirect_stdout(io.StringIO()):
            run_command('add', ['f1.txt'])
        self.assertTrue(os.path.isfile(os.path.join('.cvs', 'index')))

    '''
    Тестим, функция сработала корректно и сформировала всю структуру
    '''
    def test_add_correct(self):
        with contextlib.redirect_stdout(io.StringIO()):
            run_command('add', ['f1.txt'])
        with open(os.path.join('.cvs', 'index'), 'r') as f:
            value = f.read().splitlines()
        self.assertEqual(1, len(value))

        sha, path = value[0].split(' ', 1)
        self.assertEqual(path, 'f1.txt')

        objects_directory = os.path.join('.cvs', 'objects', sha[:2])
        self.assertTrue(os.path.isdir(objects_directory))
        objects_path = os.path.join(objects_directory, sha[2::])
        self.assertTrue(os.path.isfile(objects_path))

    '''
    Тестим, что повторный add не меняет дублирует запись
    '''
    def test_add_dont_change_double(self):
        with contextlib.redirect_stdout(io.StringIO()):
            run_command('add', ['f1.txt'])
            run_command('add', ['f1.txt'])
        with open(os.path.join('.cvs', 'index'), 'r') as f:
            value = f.read().splitlines()
        self.assertEqual(1, len(value))

    '''
    Тест на добавление несуществующего файла
    '''
    def test_add_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            run_command('add', ['f2.txt'])


if __name__ == '__main__':
    unittest.main()
