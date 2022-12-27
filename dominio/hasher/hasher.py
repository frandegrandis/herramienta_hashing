import hashlib


# Puede recibir un archivo o un string y retorna el hash

class Hasher:
    def hash(self, element):
        hasher = hashlib.md5()
        if isinstance(element, str):
            hasher.update(self.get_bytes_of(element))
        else:
            for line in iter(lambda: element.read(4096), b""):
                hasher.update(line)
        return hasher.hexdigest()

    def get_bytes_of(self, element):
        return bytes(element, 'utf-8')
