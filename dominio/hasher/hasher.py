import hashlib

from helpers.utilidades import bytes_de_string


# Puede recibir un archivo o un string y retorna el hash


class Hasher:

    def __init__(self, hasher_creator):
        self.hasher = hasher_creator()
        self.new_hasher = hasher_creator

    def hash(self, elemento):
        self.hasher = self.new_hasher()
        if isinstance(elemento, str):  # es string
            self.hasher.update(bytes_de_string(elemento))
        else:  # es archivo
            self._hash_archivo(elemento)
        return self.hasher.hexdigest()

    def _hash_archivo(self, archivo):
        for line in iter(lambda: archivo.read(4096), b""):
            self.hasher.update(line)

    @classmethod
    def sha1(cls):
        return cls(hashlib.sha1)

    @classmethod
    def md5(cls):
        return cls(hashlib.md5)

    @classmethod
    def sha256(cls):
        return cls(hashlib.sha256)
