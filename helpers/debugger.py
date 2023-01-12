from helpers.md5 import MD5
from helpers.utilidades import bytes_de_string


class Debugger:
    def __init__(self, hasher_a_serializar):
        self.hasher = hasher_a_serializar

    def palabras(self, bloque):
        return self.hasher.palabras_del_bloque(bloque)

    def valores_iniciales(self, paso, bloque):
        return self.hasher.iteraciones_por_bloque()[bloque - 1][paso - 1].valores_iniciales()

    def valores_finales(self, paso, bloque):
        return self.hasher.iteraciones_por_bloque()[bloque - 1][paso - 1].valores_finales()

    def resultado_final(self):
        return self.hasher.hexdigest()

    @classmethod
    def md5(cls, string_a_hashear):
        hasher = MD5()
        hasher.update(bytes_de_string(string_a_hashear))
        return cls(hasher)
