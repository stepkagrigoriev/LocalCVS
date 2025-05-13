import unittest, os, shutil, contextlib, io

from jinja2.runtime import new_context

from Core.repository import Repository, RepositoryError
from Core.commands import run_command
from Core.branch import Branch

class LogTests(unittest.TestCase):
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
        with contextlib.redirect_stdout(io.StringIO()):
            run_command('add', ['f1.txt'])
            run_command('commit', ['-m', 'first_commit'])
        self.first_commit = Branch.get_head(repo)

        with open('f1.txt', 'w') as f:
            f.write('python')
        with contextlib.redirect_stdout(io.StringIO()):
            run_command('add', ['f1.txt'])
            run_command('commit', ['-m', 'second_commit'])
        self.second_commit = Branch.get_head(repo)

        with open('f1.txt', 'w') as f:
            f.write('silno')
        with contextlib.redirect_stdout(io.StringIO()):
            run_command('add', ['f1.txt'])
            run_command('commit', ['-m', 'third_commit'])
        self.third_commit = Branch.get_head(repo)

    def tearDown(self):
        os.chdir(self.initial_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    '''
    Тест на корректный порядок вывода при трёх корректных коммитах
    '''
    def test_correct_log_order(self):
        new_console = io.StringIO()
        with contextlib.redirect_stdout(new_console):
            run_command('log', [])
            data = new_console.getvalue()
        ind1 = data.find(self.first_commit)
        ind2 = data.find(self.second_commit)
        ind3 = data.find(self.third_commit)
        self.assertTrue(ind1 > ind2 > ind3)

    '''
    Тестим, что при log выдаёт всю информацию о текущих коммитах (в обратном порядке)
    '''
    def test_correct_log_messages(self):
        new_console = io.StringIO()
        with contextlib.redirect_stdout(new_console):
            run_command('log', [])
            data = new_console.getvalue().strip().splitlines()
        self.assertTrue(len(data) > 6)
        self.assertTrue(data[0].startswith('commit '))
        self.assertEqual(data[1], '       third_commit')
        self.assertTrue(data[3].startswith('commit '))
        self.assertEqual(data[4], '       second_commit')
        self.assertTrue(data[6].startswith('commit '))
        self.assertEqual(data[7], '       first_commit')

        first_hash = data[6].split()[1]
        second_hash = data[3].split()[1]
        third_hash = data[0].split()[1]
        self.assertTrue(first_hash != second_hash
                        and second_hash != third_hash
                        and first_hash != second_hash)


if __name__ == '__main__':
    unittest.main()