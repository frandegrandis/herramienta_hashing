from dominio.algoritmos.iteracion import Iteracion
from dominio.algoritmos.sha512.operaciones import gamma1, ch, gamma0, maj
from helpers.utilidades import suma_modular


class IteracionSHA512(Iteracion):
    def __init__(self, a, b, c, d, e, f, g, h, constante_a_usar, palabra_a_sumar):
        self.palabra_a_sumar = palabra_a_sumar
        self.constante_a_usar = constante_a_usar
        self.h = h
        self.g = g
        self.f = f
        self.e = e
        self.d = d
        self.c = c
        self.b = b
        self.a = a

    def ejecutar(self):
        temp1 = self.t1()
        temp2 = self.t2()

        h = self.g
        g = self.f
        f = self.e
        e = suma_modular(self.d, temp1, modulo=2 ** 64)
        d = self.c
        c = self.b
        b = self.a
        a = suma_modular(temp1, temp2, modulo=2 ** 64)

        return a, b, c, d, e, f, g, h

    def t2(self):
        return gamma0(self.a) + maj(self.a, self.b, self.c)

    def t1(self):
        return self.h + gamma1(self.e) + ch(self.e, self.f, self.g) + self.constante_a_usar + self.palabra_a_sumar

    def valores_iniciales(self):
        return [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]

    def valores_finales(self):
        return self.ejecutar()
