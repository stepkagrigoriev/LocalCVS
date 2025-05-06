import unittest
import os
import shutil

from Core.commands import run_command
from Core.repository import Repository, RepositoryError
from Core.buffer import Buffer
from Core.object_store import ObjectStore

class AddTests(unittest.TestCase):
    def setUp(self):
        self.initial_dir = os.getcwd()
        self.dir = 'test_repo'
        if os.path.exists(self.dir):
            shutil.rmtree(self.dir)
        os.makedirs(self.dir)
        repo = Repository(self.dir)
        repo.init()
        os.chdir(self.dir)
        with open('f1.txt', 'w', encoding='utf-8') as f:
            f.write('lublu python')

    def tearDown(self):
        os.chdir(self.initial_dir)
        if os.path.exists(self.dir):
            shutil.rmtree(self.dir)

    '''
    Тестим, что есть файл index.cvs
    '''
    def test_add_create_index_file(self):
        run_command('add', ['f1.txt'])
        self.assertTrue(os.path.isfile(os.path.join('.cvs', 'index')))

    '''
    Тестим, функция сработала корректно на корректных вводных и сформировала всю структуру
    '''
    def test_add_correct(self):
        run_command('add', ['f1.txt'])
        with open(os.path.join('.cvs', 'index'), 'r', encoding='utf-8') as f:
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
        run_command('add', ['f1.txt'])
        run_command('add', ['f1.txt'])
        with open(os.path.join('.cvs', 'index'), 'r', encoding='utf-8') as f:
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