import os
from .branch import Branch
from .repository import RepositoryError


class Tag:
    @staticmethod
    def create_tag(repo, tag, sha=None):
        tag_path = os.path.join(repo.cvsdir, 'refs', 'tags', tag)
        if os.path.exists(tag_path):
            raise RepositoryError
        if not sha:
            sha = Branch.get_head(repo)
        os.makedirs(os.path.dirname(tag_path), exist_ok=True)
        with open(tag_path, 'w') as f:
            f.write(sha)

    @staticmethod
    def list_tags(repo):
        tag_dir = os.path.join(repo.cvsdir, 'refs', 'tags')
        if not os.path.exists(tag_dir):
            return []
        return os.listdir(tag_dir)

    @staticmethod
    def delete_tag(repo, tag):
        path = os.path.join(repo.cvsdir, 'refs', 'tags', tag)
        if not os.path.exists(path):
            raise RepositoryError('No such tag')
        os.remove(path)

    @staticmethod
    def get_tag_commit(repo, tag):
        tag_path = os.path.join(repo.cvsdir, 'refs', 'tags', tag)
        if not os.path.exists(tag_path):
            raise RepositoryError
        with open(tag_path, 'r') as f:
            return f.read().strip()
