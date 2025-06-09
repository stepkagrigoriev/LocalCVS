import os
import zlib
import hashlib


class ObjectStore:
    def __init__(self, repo):
        self.objects_dir = os.path.join(repo.cvsdir, 'objects')

    def hash_object(self, obj, obj_type):
        name = f'{obj_type} {len(obj)}\0'.encode() + obj
        sha = hashlib.sha1(name).hexdigest()
        path = os.path.join(self.objects_dir, sha[:2])
        os.makedirs(path, exist_ok=True)
        compressed = zlib.compress(name   )
        with open(os.path.join(path, sha[2:]), 'wb') as f:
            f.write(compressed)
        return sha
