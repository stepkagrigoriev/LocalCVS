import unittest
import os
import shutil
from Core.repository import Repository
from Core.tag import Tag

class TagTest(unittest.TestCase):
    def setUp(self):
        self.initial_dir = os.getcwd()
        self.test_dir = os.path.join(self.initial_dir, 'test_repo')
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        self.repo = Repository(self.test_dir)
        self.repo.init()
        os.chdir(self.test_dir)
        with open('.cvs/refs/heads/master', 'w') as f:
            f.write('sha_to_some_commit1')
            f.write('sha_to_some_commit2')  # будто уже есть коммит, у которого мы точно знаем sha
        with open('.cvs/HEAD', 'w') as f:
            f.write('refs/heads/master')    # и HEAD как раз указывает на этот коммит

    def tearDown(self):
        os.chdir(self.initial_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    '''
    Тестим, что базово всё правильно проектируется при заданном sha
    '''
    def test_create_tag_to_sha(self):
        Tag.create_tag(self.repo, 'TAG', 'sha_to_some_commit1')
        tag_path =  os.path.join(self.repo.cvsdir, 'refs', 'tags', 'TAG')
        self.assertTrue(os.path.exists(tag_path))
        with open(tag_path, 'r') as f:
            self.assertEqual(f.read().strip(), 'sha_to_some_commit1')

    '''
    Тестим, что без задания sha, тэг вешается на указатель HEAD
    '''
    def test_create_tag_to_head(self):
        Tag.create_tag(self.repo, 'TAG')
        tag_path =  os.path.join(self.repo.cvsdir, 'refs', 'tags', 'TAG')
        self.assertTrue(os.path.exists(tag_path))
        with open(tag_path, 'r') as f:
            self.assertEqual(f.read().strip(), 'sha_to_some_commit1sha_to_some_commit2')

    '''
    Тестим, что -d правильно работает
    '''
    def test_delete_tag(self):
        Tag.create_tag(self.repo, 'TAG', 'sha_to_some_commit1')
        Tag.delete_tag(self.repo, 'TAG')
        tag_path = os.path.join(self.repo.cvsdir, 'refs', 'tags', 'TAG')
        self.assertFalse(os.path.exists(tag_path))

    '''
    Тестим, что по названию тэга находит коммит
    '''
    def test_get_tag_commit(self):
        Tag.create_tag(self.repo, 'AGAKANESHNO', 'sha_to_some_commit1')
        sha = Tag.get_tag_commit(self.repo, 'AGAKANESHNO')
        self.assertEqual(sha, 'sha_to_some_commit1')

    '''
    Тест на показ всех коммитов
    '''
    def test_list_tags(self):
        Tag.create_tag(self.repo, 'tag1', 'sha_to_some_commit1')
        Tag.create_tag(self.repo, 'tag2', 'sha_to_some_commit2')
        tags = Tag.list_tags(self.repo)
        self.assertIn('tag1', tags)
        self.assertIn('tag2', tags)


if __name__ == '__main__':
    unittest.main()