from dominio.algoritmos.iteracion import Iteracion
from helpers.operaciones_bit_a_bit import rotar_izquierda
from helpers.utilidades import suma_modular


class IteracionMD5(Iteracion):
    def __init__(self, a, b, c, d, bits_a_rotar, s, operacion, palabra_a_sumar):
        self.palabra_a_sumar = palabra_a_sumar
        self.operacion = operacion
        self.constante_s = s
        self.d_inicial = d
        self.c_inicial = c
        self.b_inicial = b
        self.a_inicial = a
        self.bits_a_rotar = bits_a_rotar

    def ejecutar(self):
        a = self.suma_final()
        self.a_final, self.b_final, self.c_final, self.d_final = self.d_inicial, a, self.b_inicial, self.c_inicial
        return self.a_final, self.b_final, self.c_final, self.d_final

    def suma_final(self):
        a = self.rotacion()
        a = suma_modular(a, self.b_inicial)
        return a

    def rotacion(self):
        a = self.suma_inicial()
        a = rotar_izquierda(a, self.bits_a_rotar)
        return a

    def suma_inicial(self):
        return suma_modular(self.a_inicial + self.operacion.aplicar_a(self.b_inicial, self.c_inicial,
                                                                      self.d_inicial) + self.palabra_a_sumar,
                            self.constante_s)

    def valores_iniciales(self):
        return [self.a_inicial, self.b_inicial, self.c_inicial, self.d_inicial]

    def valores_finales(self):
        return list(self.ejecutar())
