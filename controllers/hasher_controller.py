from dominio.hasher.hasher import Hasher


class HasherController:
    def __init__(self, hasher_class = Hasher):
        self.hasher = hasher_class
    def calcular_hash_md5(self, valor_a_hashear):
        hasher = self.hasher.md5()
        return hasher.hash(valor_a_hashear)

    def calcular_hash_sha1(self, valor_a_hashear):
        hasher = self.hasher.sha1()
        return hasher.hash(valor_a_hashear)

    def calcular_hash_sha256(self, valor_a_hashear):
        hasher = self.hasher.sha256()
        return hasher.hash(valor_a_hashear)