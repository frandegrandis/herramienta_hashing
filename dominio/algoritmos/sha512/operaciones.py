from helpers.operaciones_bit_a_bit import rotar_derecha


def gamma0(a):
    return rotar_derecha(a, 28, cantidad_de_bits=64) ^ rotar_derecha(a, 34, cantidad_de_bits=64) ^ rotar_derecha(
        a, 39, cantidad_de_bits=64)


def gamma1(e):
    return rotar_derecha(e, 14, cantidad_de_bits=64) ^ rotar_derecha(e, 18, cantidad_de_bits=64) ^ rotar_derecha(
        e, 41, cantidad_de_bits=64)


def sigma1(x):
    return rotar_derecha(x, 19, cantidad_de_bits=64) ^ rotar_derecha(x, 61, cantidad_de_bits=64) ^ (x >> 6)


def sigma0(x):
    return rotar_derecha(x, 1, cantidad_de_bits=64) ^ rotar_derecha(x, 8, cantidad_de_bits=64) ^ (x >> 7)


def maj(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)


def ch(e, f, g):
    return (e & f) ^ (~e & g)
