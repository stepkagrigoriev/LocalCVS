import unittest
import os
import shutil
from Core.repository import Repository

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
        vcs = os.path.join(self.dir, '.cvs')
        self.assertTrue(os.path.isdir(vcs))
        self.assertTrue(os.path.isdir(os.path.join(vcs, 'objects')))
        self.assertTrue(os.path.isdir(os.path.join(vcs, 'references', 'heads')))
        HEAD= os.path.join(vcs, 'HEAD')
        self.assertTrue(os.path.isfile(HEAD))
        with open(HEAD, 'r', encoding='utf-8') as f:
            self.assertEqual(f.read(), 'references/heads/master')

if __name__ == "__main__":
    unittest.main()