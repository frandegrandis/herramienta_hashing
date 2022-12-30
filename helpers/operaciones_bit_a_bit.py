from bitarray import bitarray


def rotar_izquierda(x: int, y: int) -> int:
    """
    Rota los bits de x en y posiciones, ver test para ejemplos
    pensado unicamente para 32 bits
    """
    bits_de_x = bitarray_de_numero(x)
    primeros_y_bits = bits_de_x[0:y]
    # agrego los primeros bits al final
    aux = bits_de_x + primeros_y_bits
    # remuevo los primeros bits.
    aux = aux[len(aux) - len(bits_de_x)::]
    # lo convierto en numero
    return bitarray_a_numero(aux)


def bitarray_a_numero(aux):
    return int.from_bytes(aux.tobytes(), 'big')


def bit_not(x: int) -> int:
    """
    El complemento bit a bit,  ver test para ejemplos
    pensado para 32 bits.
    """
    return bitarray_a_numero(~bitarray_de_numero(x))


def bitarray_de_numero(numero):
    bits_de_x = bitarray(endian="big")
    bits_de_x.frombytes(numero.to_bytes(4, 'big'))
    return bits_de_x
