from dominio.algoritmos.sha1.sha1_clase import SHA1
from dominio.algoritmos.md5.md5 import MD5
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

    def cantidad_bloques(self):
        return self.hasher.cantidad_bloques()

    @classmethod
    def md5(cls, elemento_a_hashear):
        if isinstance(elemento_a_hashear, str):
            elemento_a_hashear = bytes_de_string(elemento_a_hashear)
        else:
            elemento_a_hashear = elemento_a_hashear.read()
        hasher = MD5()
        hasher.update(elemento_a_hashear)
        return cls(hasher)

    @classmethod
    def sha1(cls, elemento_a_hashear):
        if isinstance(elemento_a_hashear, str):
            elemento_a_hashear = bytes_de_string(elemento_a_hashear)
        else:
            elemento_a_hashear = elemento_a_hashear.read()
        hasher = SHA1()
        hasher.update(elemento_a_hashear)
        return cls(hasher)

    def palabra_a_sumar_en(self, paso, bloque):
        return self.obtener_iteracion(paso=paso,bloque=bloque).palabra_a_sumar

    def cantidad_pasos(self):
        return len(self.hasher.iteraciones_por_bloque()[0])
