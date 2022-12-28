from sys import getsizeof


def bytes_de_string(elemento):
    return bytes(elemento, 'utf-8')


def aumentar_bits(input, i):
    a = int.from_bytes(bytes(input, 'utf-8'), 'big') + i
    value = a.to_bytes(getsizeof(a) // 8, 'big').decode()
    return value

def reducir_bits(input, i):
    return aumentar_bits(input, -i)