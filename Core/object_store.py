import os, zlib, hashlib

class ObjectStore:
    def __init__(self, repo):
        self.objects_dir = os.path.join(repo.cvsdir, 'objects')

    def hash_object(self, data, type):
        name = f'{type} {len(data)}\0'.encode() + data
        sha = hashlib.sha1(name).hexdigest()
        path = os.path.join(self.objects_dir, sha[:2])
        os.makedirs(path, exist_ok=True)
        object_path = os.path.join(path, sha[2:])
        compressed = zlib.compress(name)

        with open(object_path, 'wb') as f:
            f.write(compressed)
        return sha