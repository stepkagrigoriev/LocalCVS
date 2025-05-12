import unittest, os, shutil
from Core.repository import Repository, RepositoryError
from Core.commands import run_command
from Core.branch import Branch

class ResetTest(unittest.TestCase):
    def setUp(self):
        self.initial_dir = os.getcwd()
        self.test_dir = os.path.join(self.initial_dir, 'test_repo')
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        repo = Repository(self.test_dir)
        repo.init()
        os.chdir(self.test_dir)

        with open('f1.txt', 'w') as f:
            f.write('lublu')
        run_command('add', ['f1.txt'])
        run_command('commit', ['-m', 'first_commit'])
        self.first_commit = Branch.get_head(repo)

        with open('f1.txt', 'w') as f:
            f.write('python')
        run_command('add', ['f1.txt'])
        run_command('commit', ['-m', 'second_commit'])
        self.second_commit = Branch.get_head(repo)

    def tearDown(self):
        os.chdir(self.initial_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    '''
    Тест на то, что reset возвращает первый коммит в ветке при валидных данных
    '''
    def test_reset_valid(self):
        run_command('reset', [self.first_commit])
        new_head = Branch.get_head(Repository('.'))
        self.assertEqual(new_head, self.first_commit)

    '''
    Теперь тест на reset на несуществующий коммит
    '''
    def test_reset_invalid(self):
        with self.assertRaises(RepositoryError):
            run_command('reset', ['fignya_commit'])

if __name__ == '__main__':
    unittest.main()