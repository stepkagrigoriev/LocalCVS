import os, zlib, hashlib
from Core.repository import Repository

class ObjectStore:
    def __init__(self, repo : Repository):
        self.objects_dir = os.path.join(repo.cvsdir, 'objects')

    def hash_object(self, data : bytes, obj_type : str):
        name = f'{obj_type} {len(data)}\0'.encode() + data
        sha = hashlib.sha1(name).hexdigest()
        path = os.path.join(self.objects_dir, sha[:2])
        os.makedirs(path, exist_ok=True)
        object_path = os.path.join(path, sha[2:])
        compressed = zlib.compress(name)

        with open(object_path, 'wb') as f:
            f.write(compressed)
        return sha