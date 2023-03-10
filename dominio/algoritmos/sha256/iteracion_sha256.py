from dominio.algoritmos.sha256.operaciones import ch2, maj, gamma0, gamma1
from helpers.operaciones_bit_a_bit import suma_modular_de_bitarrays


class IteracionSHA256:
    def __init__(self, a, b, c, d, e, f, g, h, constante_a_usar, palabra_a_sumar):
        self.palabra_a_sumar = palabra_a_sumar
        self.g = g
        self.f = f
        self.e = e
        self.d = d
        self.c = c
        self.b = b
        self.a = a
        self.h = h
        self.constante_a_usar = constante_a_usar

    def valores_finales(self):
        a, b, c, d, e, f, g, h = self.ejecutar()

        return [a,b,c,d,e,f,g,h]

    def ejecutar(self):
        temp1 = suma_modular_de_bitarrays(suma_modular_de_bitarrays(
            suma_modular_de_bitarrays(suma_modular_de_bitarrays(self.h, gamma1(self.e)), ch2(self.e, self.f, self.g)),
            self.constante_a_usar),
            self.palabra_a_sumar)
        temp2 = suma_modular_de_bitarrays(gamma0(self.a), maj(self.a, self.b, self.c))
        h = self.g
        g = self.f
        f = self.e
        e = suma_modular_de_bitarrays(self.d, temp1)
        d = self.c
        c = self.b
        b = self.a
        a = suma_modular_de_bitarrays(temp1, temp2)
        return a, b, c, d, e, f, g, h
