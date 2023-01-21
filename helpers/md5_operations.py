from helpers.operaciones_bit_a_bit import bit_not


def detectar(lista, condicion):
    for elemento in lista:
        if condicion(elemento):
            return elemento


class F:
    def aplica_a(self, iteracion):
        return iteracion < 16

    def aplicar_a(self, b, c, d):
        return (b & c) | ((~b) & d)
        # return d ^ (b & (c ^ d))

    def to_string(self):
        return "F(B, C, D) = (B and C) or ((not B) and D)"


class G:
    def aplica_a(self, iteracion):
        return iteracion >= 16 and iteracion < 32

    def aplicar_a(self, b, c, d):
        return c ^ (d & (b ^ c))

    def to_string(self):
        return "G(B, C, D) = (B and D) or (C and (not D))"


class H:
    def aplica_a(self, iteracion):
        return iteracion >= 32 and iteracion < 48

    def aplicar_a(self, b, c, d):
        return b ^ c ^ d

    def to_string(self):
        return "H(B, C, D) = (B xor C xor D)"


class I:
    def aplica_a(self, iteracion):
        return iteracion >= 48 and iteracion < 64

    def aplicar_a(self, b, c, d):
        return c ^ (b | bit_not(d))

    def to_string(self):
        return "I(B, C, D) = C xor (B or (not D))"


class MD5SelectorDeOperaciones:
    operations = [F(), G(), H(), I()]

    @classmethod
    def operacion_para(cls, iteracion):
        return detectar(cls.operations, lambda operacion: operacion.aplica_a(iteracion))
