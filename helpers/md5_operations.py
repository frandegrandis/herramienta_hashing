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

    def short_string(self):
        return "F(B, C, D)"


class G:
    def aplica_a(self, iteracion):
        return iteracion >= 16 and iteracion < 32

    def aplicar_a(self, b, c, d):
        return c ^ (d & (b ^ c))


class H:
    def aplica_a(self, iteracion):
        return iteracion >= 32 and iteracion < 48

    def aplicar_a(self, b, c, d):
        return b ^ c ^ d


class I:
    def aplica_a(self, iteracion):
        return iteracion >= 48 and iteracion < 64

    def aplicar_a(self, b, c, d):
        return c ^ (b | bit_not(d))


class MD5SelectorDeOperaciones:
    operations = [F(), G(), H(), I()]

    @classmethod
    def operacion_para(cls, iteracion):
        return detectar(cls.operations, lambda operacion: operacion.aplica_a(iteracion))
