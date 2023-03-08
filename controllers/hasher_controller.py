from dominio.hasher.hasher import Hasher
from helpers.debugger import Debugger


class HasherController:
    def __init__(self, hasher_class=Hasher, debugger_md5=Debugger.md5, debugger_sha1=Debugger.sha1, debugger_sha256 = Debugger.sha256):
        self.debugger_sha1 = debugger_sha1
        self.hasher = hasher_class
        self.debugger_md5 = debugger_md5
        self.debugger_sha256 = debugger_sha256

    def calcular_hash_md5(self, valor_a_hashear):
        hasher = self.hasher.md5()
        return hasher.hash(valor_a_hashear)

    def calcular_hash_sha1(self, valor_a_hashear):
        hasher = self.hasher.sha1()
        return hasher.hash(valor_a_hashear)

    def calcular_hash_sha256(self, valor_a_hashear):
        hasher = self.hasher.sha256()
        return hasher.hash(valor_a_hashear)

    def debugguear_md5(self, string_a_hashear):
        return self.debugger_md5(string_a_hashear)

    def debugguear_sha1(self, string_a_hashear):
        return self.debugger_sha1(string_a_hashear)

    def debugguear_sha256(self, string_a_hashear):
        return self.debugger_sha256(string_a_hashear)

    def calcular_hash_sha512(self, valor_a_hashear):
        hasher = self.hasher.sha512()
        return hasher.hash(valor_a_hashear)
