import unittest
import os
import shutil

from Core.commands import run_command
from Core.repository import Repository, RepositoryError

class InitTest(unittest.TestCase):
    def setUp(self):
        self.dir = 'test_repo'
        if os.path.exists(self.dir):
            shutil.rmtree(self.dir)
        os.makedirs(self.dir)

    def tearDown(self):
        if os.path.exists(self.dir):
            shutil.rmtree(self.dir)

    def test_init_creates_structure(self):
        repo = Repository(self.dir)
        repo.init()
        cvs_path = os.path.join(self.dir, '.cvs')
        self.assertTrue(os.path.isdir(cvs_path))
        self.assertTrue(os.path.isdir(os.path.join(cvs_path, 'objects')))
        self.assertTrue(os.path.isdir(os.path.join(cvs_path, 'references', 'heads')))
        head_file = os.path.join(cvs_path, 'HEAD')
        self.assertTrue(os.path.isfile(head_file))
        with open(head_file, 'r', encoding='utf-8') as f:
            self.assertEqual(f.read(), 'references/heads/master')

    def test_init_already_initialized_repo(self):
        new_repo = Repository(self.dir)
        new_repo.init()
        with self.assertRaises(RepositoryError):
            new_repo.init()

    def test_run_command_init_no_args(self):
        with self.assertRaises(SystemExit) as cm:
            run_command('init', [])
        self.assertEqual(cm.exception.code, 1)

    def test_run_command_init_a_lot_args(self):
        with self.assertRaises(SystemExit) as cm:
            run_command('init', ["name1", "name2"])
        self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    unittest.main()