from bitarray import bitarray
from bitarray.util import ba2hex

from helpers.utilidades import bytes_de_string


def rotar_izquierda(x: int, cantidad_bits_a_rotar: int) -> int:
    """
    Rota los bits de x en y posiciones, ver tests para ejemplos
    pensado unicamente para 32 bits
    """
    bits_de_x = bitarray_de_numero(x)
    primeros_y_bits = bits_de_x[0:cantidad_bits_a_rotar]
    # agrego los primeros bits al final
    aux = bits_de_x + primeros_y_bits
    # remuevo los primeros bits.
    aux = aux[len(aux) - len(bits_de_x)::]
    # lo convierto en numero
    # TODO: cambiar implementacion a : ((x << cantidad_bits_a_rotar) | (x >> (32 - cantidad_bits_a_rotar))) % 2**32
    return bitarray_a_numero(aux)


def bitarray_a_numero(aux):
    return int.from_bytes(aux.tobytes(), 'big')


def bit_not(x: int) -> int:
    """
    El complemento bit a bit,  ver tests para ejemplos
    pensado para 32 bits.
    """
    return bitarray_a_numero(~bitarray_de_numero(x))


def bitarray_de_numero(numero, cantidad_de_bytes=4, endianess='big'):
    bytes_de_numero = numero.to_bytes(cantidad_de_bytes, endianess)
    return bitsarray_de_bytes(bytes_de_numero)


def bitsarray_de_bytes(bytes_de_numero):
    bits_de_x = bitarray(endian="big")
    bits_de_x.frombytes(bytes_de_numero)
    return bits_de_x


def bitarray_de_string(string):
    return bitsarray_de_bytes(bytes_de_string(string))


def rotar_derecha(x, n, cantidad_de_bits=32):
    return (x >> n) | (x << (cantidad_de_bits - n)) & ((2 ** cantidad_de_bits) - 1)


def hex_de_bitarray(value):
    return ba2hex(value)
