from helpers.operaciones_bit_a_bit import rotar_derecha


def ch(x, y, z):
    return (x & y) ^ (~x & z)


def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


def gamma0(x):
    return rotar_derecha(x, 2) ^ rotar_derecha(x, 13) ^ rotar_derecha(x, 22)


def gamma1(x):
    return rotar_derecha(x, 6) ^ rotar_derecha(x, 11) ^ rotar_derecha(x, 25)


def sigma0(x):
    return rotar_derecha(x, 7) ^ rotar_derecha(x, 18) ^ (x >> 3)


def sigma1(x):
    return rotar_derecha(x, 17) ^ rotar_derecha(x, 19) ^ (x >> 10)
