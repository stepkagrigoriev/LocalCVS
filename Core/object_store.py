import os
import zlib
import hashlib


class ObjectStore:
    def __init__(self, repo):
        self.objects_dir = os.path.join(repo.cvsdir, 'objects')

    def write_object(self, obj, obj_type) -> str:
        if isinstance(obj, str):
            obj = obj.encode('utf-8')
        name = f'{obj_type} {len(obj)}\n'.encode() + obj
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
        sep = raw.index(b'\n')
        obj_type = raw[:sep].decode('utf-8')
        data = raw[sep + 1:]
        return obj_type, data

