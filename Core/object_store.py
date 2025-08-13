import os
import zlib
import hashlib


class ObjectStore:
    def __init__(self, repo):
        self.objects_dir = os.path.join(repo.cvsdir, 'objects')

    def write_object(self, obj, obj_type) -> str:
        name = f'{obj_type} {len(obj)}\0'.encode() + obj
        sha = hashlib.sha1(name).hexdigest()
        path = os.path.join(self.objects_dir, sha[:2], sha[2:])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        compressed = zlib.compress(name)
        with open(path, 'wb') as f:
            f.write(compressed)
        return sha
    
    
    def read_object(self, sha) -> (str | bytes):
        path = os.path.join(self.objects_dir, sha[:2], sha[2:])
        with open(path, 'rb') as f:
            raw = zlib.decompress(f.read())
        sep_ind = raw.index(b'\n')
        obj_type = raw[:sep_ind].decode('utf-8')
        data = raw[sep_ind + 1:]
        return obj_type, data

