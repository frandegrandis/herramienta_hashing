from bitarray import bitarray
from bitarray.util import ba2int, ba2hex

from helpers.operaciones_bit_a_bit import bitarray_de_numero, bitarray_de_string, fill_zeros
from helpers.utilidades import suma_modular

h_hex = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4,
     0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe,
     0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f,
     0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
     0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc,
     0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
     0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116,
     0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
     0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7,
     0xc67178f2]


def chunker(bits, chunk_length=8):
    chunked = []
    for b in range(0, len(bits), chunk_length):
        chunked.append(bits[b:b + chunk_length])
    return chunked


def preprocessMessage(message):
    bits = bitarray_de_string(message)
    length = len(bits)
    message_len = bitarray([int(b) for b in bin(length)[2:].zfill(64)])
    if length < 448:
        bits.append(1)
        bits = fill_zeros(bits, 448, 'LE')
        bits = bits + message_len
        return [bits]
    elif 448 <= length <= 512:
        bits.append(1)
        bits = fill_zeros(bits, 1024, 'LE')
        bits[-64:] = message_len
        return chunker(bits, 512)
    else:
        bits.append(1)
        while (len(bits) + 64) % 512 != 0:
            bits.append(0)
        bits = bits + message_len
        return chunker(bits, 512)


def initializer(values):
    binaries = [bitarray_de_numero(v) for v in values]
    words = []
    for binary in binaries:
        word = binary
        words.append(fill_zeros(word, 32, 'BE'))
    return words


def hex_de_bitarray(value):
    return ba2hex(value)


def rotar_derecha(x, n): return x[-n:] + x[:-n]


def add(i, j):
    a = ba2int(i)
    b = ba2int(j)
    return bitarray_de_numero(suma_modular(a, b))


def ch2(x, y, z):
    return (x & y) ^ (~x & z)


def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


def sha256(message):
    k = initializer(K)
    h0, h1, h2, h3, h4, h5, h6, h7 = initializer(h_hex)
    chunks = preprocessMessage(message)
    for chunk in chunks:
        w = chunker(chunk, 32)
        for _ in range(48):
            w.append(32 * [0])
        for i in range(16, 64):
            i3 = rotar_derecha(w[i - 15], 7)
            j2 = rotar_derecha(w[i - 15], 18)
            x = w[i - 15]
            l = x >> 3
            s0 = i3 ^ j2 ^ l
            i4 = rotar_derecha(w[i - 2], 17)
            j3 = rotar_derecha(w[i - 2], 19)
            x1 = w[i - 2]
            l1 = x1 >> 10
            s1 = i4 ^ j3 ^ l1
            w[i] = add(add(add(w[i - 16], s0), w[i - 7]), s1)
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7
        for j in range(64):
            i5 = rotar_derecha(e, 6)
            j4 = rotar_derecha(e, 11)
            l2 = rotar_derecha(e, 25)
            S1 = i5 ^ j4 ^ l2
            temp1 = add(add(add(add(h, S1), ch2(e, f, g)), k[j]), w[j])
            i6 = rotar_derecha(a, 2)
            j5 = rotar_derecha(a, 13)
            l3 = rotar_derecha(a, 22)
            S0 = i6 ^ j5 ^ l3
            temp2 = add(S0, maj(a, b, c))
            h = g
            g = f
            f = e
            e = add(d, temp1)
            d = c
            c = b
            b = a
            a = add(temp1, temp2)
        h0 = add(h0, a)
        h1 = add(h1, b)
        h2 = add(h2, c)
        h3 = add(h3, d)
        h4 = add(h4, e)
        h5 = add(h5, f)
        h6 = add(h6, g)
        h7 = add(h7, h)
    digest = ''
    for val in [h0, h1, h2, h3, h4, h5, h6, h7]:
        digest += hex_de_bitarray(val)
    return digest


if __name__ == '__main__':
    verdict = 'y'
    while verdict == 'y':
        input_message = input('Type or copy your message here: ')
        print('Your message: ', input_message)
        print('Hash: ', sha256(input_message))
        verdict = input('Do you want to tryte another text? (y/n): ').lower()
