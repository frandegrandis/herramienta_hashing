import bitarray

from helpers.operaciones_bit_a_bit import bitarray_a_numero


def mostrar_32_bits_centrados_con_espacio(B):
    return f"{bit_string_de(B):^40}"


def nombre_clase_de(objeto):
    return objeto.__class__.__name__


def bit_string_de(numero):
    if isinstance(numero, bitarray.bitarray):
        numero = bitarray_a_numero(numero)
    return completar_con_ceros_hasta(32, bin(abs(numero))[2::])


def completar_con_ceros_hasta(i, palabra_a_completar):
    if len(palabra_a_completar) < i:
        while len(palabra_a_completar) < i:
            palabra_a_completar = "0" + palabra_a_completar
    return palabra_a_completar


def hex_string_de(numero):
    if isinstance(numero, bitarray.bitarray):
        numero = bitarray_a_numero(numero)
    return completar_con_ceros_hasta(8, hex(numero)[2::].upper())


def crear_linea():
    return "\n------------------------------------------------------------------------"
