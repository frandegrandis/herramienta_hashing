from helpers.md5 import MD5
from helpers.utilidades import bytes_de_string


class Debugger:
    def __init__(self, hasher_a_serializar):
        self.hasher = hasher_a_serializar

    def palabras(self, bloque):
        return self.hasher.palabras_del_bloque(bloque)

    def valores_iniciales(self, paso, bloque):
        return self.obtener_iteracion(bloque, paso).valores_iniciales()

    def obtener_iteracion(self, bloque, paso):
        return self.hasher.iteraciones_por_bloque()[bloque - 1][paso - 1]

    def valores_finales(self, paso, bloque):
        return self.obtener_iteracion(bloque, paso).valores_finales()

    def resultado_final(self):
        return self.hasher.hexdigest()

    def operacion(self, paso, bloque):
        return self.obtener_iteracion(paso, bloque).operacion

    def numero_de_palabra_a_sumar_en_paso(self, paso):
        return self.hasher.numero_de_palabra_a_sumar_en_paso(paso - 1)

    @classmethod
    def md5(cls, string_a_hashear):
        hasher = MD5()
        hasher.update(bytes_de_string(string_a_hashear))
        return cls(hasher)
