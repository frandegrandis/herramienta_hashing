import hashlib


# Puede recibir un archivo o un string y retorna el hash

class Hasher:

    def __init__(self):
        self.hasher = hashlib.md5()

    def hash(self, elemento):
        if isinstance(elemento, str): #es string
            self.hasher.update(self.bytes_de(elemento))
        else: #es archivo
            self._hash_archivo(elemento)
        return self.hasher.hexdigest()

    def _hash_archivo(self, archivo):
        for line in iter(lambda: archivo.read(4096), b""):
            self.hasher.update(line)

    def bytes_de(self, elemento):
        return bytes(elemento, 'utf-8')
