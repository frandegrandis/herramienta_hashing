def mostrar_32_bits_centrados_con_espacio(B):
    return f"{bit_string_de(B):^40}"


def nombre_clase_de(objeto):
    return objeto.__class__.__name__


def bit_string_de(numero):
    a = bin(abs(numero))[2::]
    if len(a) >= 32:
        return a
    else:
        while len(a) < 32:
            a = "0" + a
        return a


def hex_string_de(numero):
    return hex(numero)[2::].upper()
