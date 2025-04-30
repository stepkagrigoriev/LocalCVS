import os
from Core.repository import Repository
def init(repo_name):
    repo = Repository(repo_name)
    repo.init()