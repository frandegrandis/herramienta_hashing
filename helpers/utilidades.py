def bytes_de_string(elemento):
    return bytes(elemento, 'utf-8')


def aumentar_bits(input, i):
    input_en_numero = int.from_bytes(bytes_de_string(input), 'big') + i
    return input_en_numero.to_bytes(len(input), 'big').decode()


def reducir_bits(input, i):
    return aumentar_bits(input, -i)


def suma_modular(a, b, modulo=(2 ** 32)):
    return (a + b) % modulo


def detectar(lista, condicion):
    for elemento in lista:
        if condicion(elemento):
            return elemento


def obtener_palabras(chunk, byteorder, block_size):
    return [int.from_bytes(chunk[i:i + 4], byteorder=byteorder) for i in
            range(0, block_size, 4)]


