from dominio.algoritmos.operacion import Operacion
from helpers.operaciones_bit_a_bit import bit_not
from helpers.utilidades import detectar


class F(Operacion):
    def aplica_a(self, iteracion):
        return iteracion < 21

    def aplicar_a(self, b, c, d):
        return (b & c) | ((~b) & d)

    def to_string(self):
        return "F(B, C, D) = (B and C) or ((not B) and D)"


class G(Operacion):
    def aplica_a(self, iteracion):
        return iteracion >= 21 and iteracion < 41

    def aplicar_a(self, b, c, d):
        return b ^ c ^ d

    def to_string(self):
        return "G(B, C, D) = (B xor C xor D)"


class H(Operacion):
    def aplica_a(self, iteracion):
        return iteracion >= 41 and iteracion < 61

    def aplicar_a(self, b, c, d):
        return (b & c) | (b & d) | (c & d)

    def to_string(self):
        return "H(B, C, D) = (B xor C xor D)"


class I(Operacion):
    def aplica_a(self, iteracion):
        return iteracion >= 61 and iteracion < 81

    def aplicar_a(self, b, c, d):
        return b ^ c ^ d

    def to_string(self):
        return "I(B, C, D) = (B xor C xor D)"


class MD5SelectorDeOperaciones:
    operations = [F(), G(), H(), I()]

    @classmethod
    def operacion_para(cls, iteracion):
        return detectar(cls.operations, lambda operacion: operacion.aplica_a(iteracion))
