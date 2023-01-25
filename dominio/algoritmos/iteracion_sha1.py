from dominio.algoritmos.iteracion import Iteracion
from helpers.operaciones_bit_a_bit import rotar_izquierda
from helpers.utilidades import suma_modular


class IteracionSHA1(Iteracion):
    def __init__(self, constante_k, A, B, C, D, E, operacion, palabra_a_sumar):
        self.palabra_a_sumar = palabra_a_sumar
        self.operacion = operacion
        self.E = E
        self.D = D
        self.C = C
        self.B = B
        self.A = A
        self.constante_k = constante_k

    def ejecutar(self):
        a = self.operacion.aplicar_a(self.B, self.C, self.D)
        a += self.E
        a += rotar_izquierda(self.A, 5)
        a += self.palabra_a_sumar
        a = suma_modular(a, self.constante_k)
        b = rotar_izquierda(self.B, 30)
        return a, self.A, b, self.C, self.D
