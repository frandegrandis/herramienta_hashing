from helpers.operaciones_bit_a_bit import rotar_derecha


def gamma0(a):
    return rotar_derecha(a, 28) ^ rotar_derecha(a, 34) ^ rotar_derecha(a, 39)


def gamma1(e):
    return rotar_derecha(e, 14) ^ rotar_derecha(e, 18) ^ rotar_derecha(e, 41)


def sigma1(x):
    return rotar_derecha(x, 19) ^ rotar_derecha(x, 61) ^ (x >> 6)


def sigma0(x):
    return rotar_derecha(x, 1) ^ rotar_derecha(x, 8) ^ (x >> 7)


def maj(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)


def ch(e, f, g):
    return (e & f) ^ (~e & g)
